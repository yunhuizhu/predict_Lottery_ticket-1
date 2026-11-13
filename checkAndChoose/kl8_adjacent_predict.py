"""
快乐8 相邻号预测

思路:
  1. 分别读取 zip/kl8_<日期>.csv 和 zip/kl8_<日期>_h.csv 预测文件, 各自统计号码出现次数
     - csv 文件取 ckcommons2、ckcommons3 两个数组
     - _h  文件取 ckcommons2、ckcommons3、ckcommons4 三个数组
     在每个数组内找相邻号段(如 23,24,25), 认为每个号段大概率会开出其中一个。
  规则2(开奖号连号):
     a. 上两期开奖号合起来找连号, 连号里属于上一期的号, 下一期可能再出其中一个        -> "两期连号重出"
        例: 上上期开 15, 上期开 16 -> 合起来 15,16 连号 -> 上期的 16 下期可能再出
            (上期自己开出的连号也包含在内)
     b. 对上期全部20个开奖号逐个看: 号码 n 往前回看最近20期, 找最近一期里 n-1,n 或 n,n+1
        一起开出(连号)的期, 那一期和 n 相连的邻号(n-1 或 n+1)下一期可能出, 越近权重越高 -> "历史相邻号"
        例: 2026287 开出 16, 往前找到最近一期 2026283 开过 15,16 -> 预测 15
  3. 用已有的开奖数据回测上面每类规则的实际命中率, 作为权重(每期开奖后自动更新)。
  4. 输出 11码、7码、6码 各三注:
     - 第1注 总分:   按号码总分从高到低选, 同一号段最多取 1~2 个
     - 第2注 共用核心: 与第1注共用总分最高的前一半号码, 后一半避开第1注再选
     - 第3注 频次居中: 合并 csv 和 _h 的出现次数, 优先选次数接近 5 的号, 次数相同按相邻号总分排
       (出现次数太少或太多的号历史表现都不好, 回测里居中的号命中更高)
  5. 独有号选十 3 注: 取不带后缀的 kl8_<日期>.csv 第 3、5、10 行(ck3、ck5、ck10),
     去掉在其中任意两行都出现的号, 剩下每行独有的号;
     第1注从 ck3 独有号里选、第2注从 ck5 独有号里选、第3注从 ck10 独有号里选, 各按总分取前 10 个,
     某行独有号不足 10 个时, 用其他两行的独有号按总分补齐

开奖数据来自 https://www.17500.cn/chart/kl8-gzm.html (页面只有最近30期),
每次运行增量合并到 data/kl8/kjh_17500.csv, 历史会越攒越多。

用法:
  python kl8_adjacent_predict.py              # 默认取 zip 中最新日期的预测文件
  python kl8_adjacent_predict.py 20261012     # 指定预测文件日期(即预测当天那期)
  python kl8_adjacent_predict.py 20261012 --offline   # 不联网, 只用本地开奖数据
  python kl8_adjacent_predict.py --compare    # 所有已开奖日期逐期回测, 输出三注方案的累计成绩
  python kl8_adjacent_predict.py --compare --last=30  # 只看最近30期
"""

import csv
import os
import re
import sys
from collections import Counter
from math import comb

import requests

BASE = os.path.dirname(os.path.abspath(__file__))
ZIP_DIR = os.path.join(BASE, "zip")
KJH_FILE = os.path.join(BASE, "..", "data", "kl8", "kjh_17500.csv")
OUT_DIR = os.path.join(BASE, "predict_out")
URL = "https://www.17500.cn/chart/kl8-gzm.html"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
}

LOOKBACK = 20              # 相邻号回看期数
CSV_GROUPS = (2, 3)        # csv 文件取的 ckcommons
H_GROUPS = (2, 3, 4)       # _h 文件取的 ckcommons
BET_SIZES = (11, 7, 6)     # 每种各三注
MID_FREQ = 5               # 第3注: 优先选合并出现次数接近此值的号
UNIQUE_ROWS = (3, 5, 10)   # 独有号选十: 取不带后缀 csv 的第几行
UNIQUE_SIZE = 10


# ============================================================
# 开奖数据
# ============================================================
def crawl_kjh():
    """抓取 17500 快乐8 开奖页, 返回 {期号: {'date': 'YYYYMMDD', 'numbers': [...]}}"""
    resp = requests.get(URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    html = resp.text
    tbody = html[html.find("<tbody"):html.find("</tbody>")]
    data = {}
    for tr in re.findall(r"<tr>(.*?)</tr>", tbody, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 5:
            continue
        issue = re.sub(r"<[^>]+>", "", tds[0]).strip()
        date = re.sub(r"<[^>]+>", "", tds[1]).strip().replace("-", "")
        # 列顺序: 期号 / 开奖日期 / 星期 / 试机号 / 奖号 / 乐彩关注码
        nums = [int(x) for x in re.findall(r"\d+", re.sub(r"<[^>]+>", " ", tds[4]))]
        if issue.isdigit() and len(date) == 8 and len(nums) == 20:
            data[issue] = {"date": date, "numbers": sorted(nums)}
    return data


def load_kjh():
    data = {}
    if os.path.exists(KJH_FILE):
        with open(KJH_FILE, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                data[row["期号"]] = {"date": row["日期"],
                                    "numbers": sorted(int(x) for x in row["奖号"].split())}
    return data


def save_kjh(data):
    os.makedirs(os.path.dirname(KJH_FILE), exist_ok=True)
    with open(KJH_FILE, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["期号", "日期", "奖号"])
        for issue in sorted(data):
            w.writerow([issue, data[issue]["date"],
                        " ".join(f"{n:02d}" for n in data[issue]["numbers"])])


def update_kjh(offline=False):
    data = load_kjh()
    if not offline:
        try:
            new = crawl_kjh()
            added = len(set(new) - set(data))
            data.update(new)
            save_kjh(data)
            print(f"开奖数据: 抓取 {len(new)} 期, 新增 {added} 期, 本地共 {len(data)} 期")
        except Exception as e:
            print(f"抓取开奖数据失败({e}), 使用本地数据 {len(data)} 期")
    else:
        print(f"离线模式, 本地开奖数据 {len(data)} 期")
    # 按日期排序的列表 [(期号, 日期, set(号码))]
    return [(k, v["date"], set(v["numbers"])) for k, v in sorted(data.items())]


# ============================================================
# 预测文件 & 相邻号段
# ============================================================
def read_pred(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            nums = [int(x) for x in row if x.strip()]
            if nums:
                rows.append(nums)
    return rows


def get_ckcommons(rows):
    """统计每个号码出现次数(同一行内重复只算一次), 按次数分组"""
    counter = Counter()
    for row in rows:
        counter.update(set(row))
    ck = {}
    for n, c in counter.items():
        ck.setdefault(c, []).append(n)
    return {c: sorted(v) for c, v in ck.items()}, counter


def adjacent_runs(nums, min_len=2):
    """从有序号码中找出连续号段, 如 [3,4,5,9,10,20] -> [[3,4,5],[9,10]]"""
    nums = sorted(set(nums))
    runs, cur = [], []
    for n in nums:
        if cur and n == cur[-1] + 1:
            cur.append(n)
        else:
            if len(cur) >= min_len:
                runs.append(cur)
            cur = [n]
    if len(cur) >= min_len:
        runs.append(cur)
    return runs


def pred_runs(date):
    """返回该日期预测文件里的相邻号段 [(来源标签, 号段)]"""
    result = []
    for suffix, groups in (("", CSV_GROUPS), ("_h", H_GROUPS)):
        rows = read_pred(os.path.join(ZIP_DIR, f"kl8_{date}{suffix}.csv"))
        if not rows:
            continue
        ck, _ = get_ckcommons(rows)
        src = "csv" if suffix == "" else "h"
        for g in groups:
            for run in adjacent_runs(ck.get(g, [])):
                result.append((f"{src}_ck{g}", run))
    return result


def two_draw_runs(history):
    """规则2a: 把上两期(history 最后两期)的开奖号合起来找连号,
    返回 [(合并后的连号, 其中属于上一期的号)]; 连号里没有上一期号码的不返回"""
    if len(history) < 2:
        return []
    last, before = history[-1][2], history[-2][2]
    result = []
    for run in adjacent_runs(last | before):
        cand = [n for n in run if n in last]
        if cand:
            result.append((run, cand))
    return result


def history_adjacent_numbers(history):
    """规则2b: 取 history 最后一期(上期)的全部20个开奖号, 对每个号码 n,
    在上期之前的最近 LOOKBACK 期里, 找最近一期 n-1,n 或 n,n+1 一起开出的期,
    那一期里和 n 相连的邻号就是候选号(n-1 和 n+1 都连着时两个都算)。
    返回 [(上期号码n, 距上期几期, 那一期的期号, [候选邻号])], 没找到的号不返回。
    例: 上期 2026287 开出 16, 往前最近一期 2026283 开过 15,16 -> (16, 4, '2026283', [15])"""
    if len(history) < 2:
        return []
    last_nums = history[-1][2]
    prev = history[:-1][-LOOKBACK:]
    result = []
    for n in sorted(last_nums):
        for ago, (issue, _, nums) in enumerate(reversed(prev), start=1):
            if n not in nums:
                continue
            nbrs = [m for m in (n - 1, n + 1) if 1 <= m <= 80 and m in nums]
            if nbrs:
                result.append((n, ago, issue, nbrs))
                break
    return result


# ============================================================
# 回测: 统计各规则真实命中率
# ============================================================
def random_hit_rate(k):
    """随机 k 个号, 至少中 1 个的概率"""
    return 1 - comb(80 - k, 20) / comb(80, 20)


def backtest(kjh, before_date):
    """用 before_date 之前所有能对上开奖的预测文件做回测"""
    by_date = {d: nums for _, d, nums in kjh}
    dates = sorted({f[4:12] for f in os.listdir(ZIP_DIR)
                    if f.startswith("kl8_") and f.endswith(".csv")})
    stats = {}   # 标签 -> [号段数, 至少中1个, 随机期望, 中的号码数, 号码总数]

    def add(tag, run, nums):
        s = stats.setdefault(tag, [0, 0, 0.0, 0, 0])
        hit = len(set(run) & nums)
        s[0] += 1
        s[1] += hit > 0
        s[2] += random_hit_rate(len(run))
        s[3] += hit
        s[4] += len(run)

    for d in dates:
        if d >= before_date or d not in by_date:
            continue
        nums = by_date[d]
        hist = [x for x in kjh if x[1] < d]
        for tag, run in pred_runs(d):
            add(tag, run, nums)

    # 规则2: 用所有开奖数据, 第 i 期只用第 i 期之前的开奖来判断
    for i in range(1, len(kjh)):
        if kjh[i][1] >= before_date:
            break
        # 2a 上两期合起来的连号里属于上期的号, 本期是否再开其中一个
        for _, cand in two_draw_runs(kjh[:i]):
            add("两期连号重出", cand, kjh[i][2])
        # 2b 上期每个开奖号在最近20期里最近一次连号的邻号, 本期是否开出(每个邻号单独统计)
        for _, _, _, nbrs in history_adjacent_numbers(kjh[:i]):
            for m in nbrs:
                add("历史相邻号", [m], kjh[i][2])
    return stats


def rule_weight(stats, tag):
    """权重 = 实际命中率 / 随机命中率 (样本少时向1收缩)"""
    s = stats.get(tag)
    if not s or s[0] == 0:
        return 1.0
    lift = (s[1] / s[0]) / (s[2] / s[0])
    shrink = s[0] / (s[0] + 20)
    return 1 + (lift - 1) * shrink


# ============================================================
# 评分 & 出号
# ============================================================
def score_numbers(date, kjh, stats):
    hist = [x for x in kjh if x[1] < date]
    runs = pred_runs(date)
    scores = Counter()
    reasons = {}
    run_info = []

    for tag, run in runs:
        w = rule_weight(stats, tag)
        run_info.append((tag, run, w))
        # 号段大概率出一个 -> 每个号分到 1/len 的权重
        for n in run:
            scores[n] += w / len(run)
            reasons.setdefault(n, []).append(f"{tag}{run}")

    # 规则2a: 上两期合起来的连号, 其中属于上期的号下期可能再出一个
    w2 = rule_weight(stats, "两期连号重出")
    for run, cand in two_draw_runs(hist):
        for n in cand:
            scores[n] += w2 * 0.8 / len(cand)
            reasons.setdefault(n, []).append(f"两期连号{run}")

    # 规则2b: 上期每个开奖号, 最近20期里最近一次和它连着开出的邻号, 下期可能出, 越近权重越高
    w3 = rule_weight(stats, "历史相邻号")
    for n, ago, issue, nbrs in history_adjacent_numbers(hist):
        recency = 1 + (LOOKBACK - ago + 1) / LOOKBACK      # 1~2
        for m in nbrs:
            scores[m] += w3 * 0.5 * recency
            reasons.setdefault(m, []).append(f"上期{n:02d}在{issue}与{m:02d}连号")

    # 同时在 csv 与 _h 中出现 -> 已通过累加体现
    return scores, reasons, run_info, hist


def run_cap(run):
    """同一号段最多取几个: 2~3 个号的段取 1 个, 4 个及以上的段取 2 个"""
    return 1 if len(run) <= 3 else 2


def pick_by_score(scores, run_info, size, start=(), exclude=()):
    """按号码总分从高到低选号, 同一号段最多取 run_cap 个。
    start: 已经选好的号(会计入号段已取数量); exclude: 不能选的号。
    号段限制导致不够时, 放开限制按总分补齐。"""
    ranked = sorted(range(1, 81), key=lambda n: (-scores[n], n))
    runs = [run for _, run, *_ in run_info]
    chosen = list(start)
    used = [sum(n in r for n in chosen) for r in runs]   # 每个号段已取了几个
    for n in ranked:
        if len(chosen) >= size:
            break
        if n in chosen or n in exclude:
            continue
        idx = [i for i, r in enumerate(runs) if n in r]
        if any(used[i] >= run_cap(runs[i]) for i in idx):
            continue
        chosen.append(n)
        for i in idx:
            used[i] += 1
    for n in ranked:
        if len(chosen) >= size:
            break
        if n not in chosen and n not in exclude:
            chosen.append(n)
    return chosen


def pick_shared_core(scores, run_info, size, first):
    """共用核心: 取总分最高的前一半号(11码6个、7码4个、6码3个)作为核心,
    后一半避开第1注的后一半号, 再按总分规则补齐"""
    core = pick_by_score(scores, run_info, (size + 1) // 2)
    return pick_by_score(scores, run_info, size, start=core, exclude=set(first) - set(core))


def pick_mid_freq(date, scores, size):
    """频次居中: 合并 csv 和 _h 两个文件的出现次数, 按 |次数 - MID_FREQ| 从小到大选号。
    次数相同时按相邻号总分(scores)从高到低排, 总分也相同再按号码大小,
    避免同次数的号太多时只取到小号。"""
    counter = Counter()
    for suffix in ("", "_h"):
        _, cnt = get_ckcommons(read_pred(os.path.join(ZIP_DIR, f"kl8_{date}{suffix}.csv")))
        counter.update(cnt)
    ranked = sorted(counter, key=lambda n: (abs(counter[n] - MID_FREQ), -scores[n], n))
    return ranked[:size]


def make_bets(date, scores, run_info):
    """每种码数三注: [总分, 共用核心, 频次居中]"""
    bets = {}
    for size in BET_SIZES:
        first = pick_by_score(scores, run_info, size)
        bets[size] = [sorted(first),
                      sorted(pick_shared_core(scores, run_info, size, first)),
                      sorted(pick_mid_freq(date, scores, size))]
    return bets


BET_NAMES = ["总分", "共用核心", "频次居中"]


def unique_row_numbers(date):
    """不带后缀的 csv 取 UNIQUE_ROWS 各行, 返回 {行号: 该行独有的号(不在另外两行出现)};
    文件不存在或行数不够时返回 None"""
    rows = read_pred(os.path.join(ZIP_DIR, f"kl8_{date}.csv"))
    if len(rows) < max(UNIQUE_ROWS):
        return None
    sets = {i: set(rows[i - 1]) for i in UNIQUE_ROWS}
    return {i: sorted(sets[i] - set().union(*(sets[j] for j in UNIQUE_ROWS if j != i)))
            for i in UNIQUE_ROWS}


def make_unique_bets(date, scores, size=UNIQUE_SIZE):
    """独有号选十 3 注: 每行独有号按总分取前 size 个, 不足时用其他行的独有号按总分补齐。
    返回 ({行号: 独有号}, [(行号, 注)])；没有可用文件时返回 (None, [])"""
    uniq = unique_row_numbers(date)
    if uniq is None:
        return None, []
    rank = lambda nums: sorted(nums, key=lambda n: (-scores.get(n, 0), n))
    pool = rank(n for nums in uniq.values() for n in nums)
    bets = []
    for i in UNIQUE_ROWS:
        bet = rank(uniq[i])[:size]
        bet += [n for n in pool if n not in bet][:size - len(bet)]
        bets.append((i, sorted(bet)))
    return uniq, bets


def compare(kjh, last=None):
    """逐期回测三注方案: 每期只用当天之前的开奖数据出号, 再和当期开奖对比。
    输出逐期命中、各方案平均命中、达到中奖线的注数, 并与随机选号的期望对比。"""
    by_date = {d: nums for _, d, nums in kjh}
    dates = sorted({f[4:12] for f in os.listdir(ZIP_DIR)
                    if f.startswith("kl8_") and f.endswith(".csv")})
    dates = [d for d in dates if d in by_date and pred_runs(d)]
    if last:
        dates = dates[-last:]
    if not dates:
        print("没有可回测的日期(需要 zip 中有预测文件且已开奖)")
        return

    # 中奖线: 选6中3、选7中4、11码(按选十复式)中5
    prize_line = {11: 5, 7: 4, 6: 3}
    hits = {(size, i): [] for size in BET_SIZES for i in range(len(BET_NAMES))}
    uniq_hits = {i: [] for i in UNIQUE_ROWS}

    print(f"\n逐期命中 ({dates[0]} ~ {dates[-1]}, 共{len(dates)}期)")
    head = "".join(f"{f'{size}码':>12}" for size in BET_SIZES)
    print(f"  {'日期':<10}{head}")
    print(f"  {'':<10}" + "".join(f"{'总/核/居':>12}" for _ in BET_SIZES))
    for d in dates:
        stats = backtest(kjh, d)
        scores, _, run_info, _ = score_numbers(d, kjh, stats)
        bets = make_bets(d, scores, run_info)
        _, ubets = make_unique_bets(d, scores)
        for i, bet in ubets:
            uniq_hits[i].append(len(set(bet) & by_date[d]))
        line = f"  {d:<10}"
        for size in BET_SIZES:
            hs = [len(set(bet) & by_date[d]) for bet in bets[size]]
            for i, h in enumerate(hs):
                hits[(size, i)].append(h)
            line += f"{'/'.join(map(str, hs)):>12}"
        print(line)

    n = len(dates)
    print(f"\n累计成绩 (共{n}期, 中奖线: 11码中{prize_line[11]}、7码中{prize_line[7]}、6码中{prize_line[6]})")
    print(f"  {'码数':<6}{'方案':<8}{'平均中':>8}{'随机均中':>10}{'达线注数':>10}{'随机达线':>10}{'最好':>6}")
    for size in BET_SIZES:
        line_k = prize_line[size]
        rand_avg = size * 20 / 80
        rand_prize = sum(comb(20, h) * comb(60, size - h) for h in range(line_k, size + 1)) / comb(80, size) * n
        for i, name in enumerate(BET_NAMES):
            v = hits[(size, i)]
            print(f"  {f'{size}码':<6}{name:<8}{sum(v) / n:>8.2f}{rand_avg:>10.2f}"
                  f"{sum(h >= line_k for h in v):>10}{rand_prize:>10.1f}{max(v):>6}")
    m = len(uniq_hits[UNIQUE_ROWS[0]])
    if m:
        rand_prize = sum(comb(20, h) * comb(60, UNIQUE_SIZE - h)
                         for h in range(5, UNIQUE_SIZE + 1)) / comb(80, UNIQUE_SIZE) * m
        print(f"\n独有号选十 (共{m}期, 中奖线中5):")
        print(f"  {'注':<10}{'平均中':>8}{'随机均中':>10}{'达线注数':>10}{'随机达线':>10}{'最好':>6}  逐期")
        for i in UNIQUE_ROWS:
            v = uniq_hits[i]
            print(f"  {f'ck{i}独有':<10}{sum(v) / m:>8.2f}{UNIQUE_SIZE / 4:>10.2f}"
                  f"{sum(h >= 5 for h in v):>10}{rand_prize:>10.1f}{max(v):>6}  {v}")
    print("\n说明: 平均中和达线注数长期稳定高于随机期望, 方案才算有效; 期数少时差异多为运气。")


# ============================================================
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    kjh = update_kjh(offline)

    if "--compare" in sys.argv:
        last = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--last=")), None)
        compare(kjh, last)
        return

    if args:
        date = args[0]
    else:
        date = max(f[4:12] for f in os.listdir(ZIP_DIR) if f.startswith("kl8_") and f.endswith(".csv"))
    print(f"\n预测文件日期: {date}")
    if not pred_runs(date):
        exists = [f for f in (f"kl8_{date}.csv", f"kl8_{date}_h.csv") if os.path.exists(os.path.join(ZIP_DIR, f))]
        print(f"zip 下{'没有 ' + date + ' 的预测文件' if not exists else '的 ' + str(exists) + ' 没有相邻号段'}, 退出")
        return

    # ---- 各文件 ckcommons
    for suffix, groups in (("", CSV_GROUPS), ("_h", H_GROUPS)):
        rows = read_pred(os.path.join(ZIP_DIR, f"kl8_{date}{suffix}.csv"))
        if not rows:
            print(f"  kl8_{date}{suffix}.csv 不存在")
            continue
        ck, _ = get_ckcommons(rows)
        print(f"  kl8_{date}{suffix}.csv ({len(rows)}行)")
        for g in groups:
            print(f"    ckcommons{g}: {ck.get(g, [])}  相邻号段: {adjacent_runs(ck.get(g, []))}")

    # ---- 回测
    stats = backtest(kjh, date)
    print("\n规则回测(该日期之前的数据):")
    print(f"  {'规则':<10}{'号段数':>6}{'至少中1':>8}{'实际率':>8}{'随机率':>8}{'权重':>7}")
    for tag in sorted(stats):
        s = stats[tag]
        print(f"  {tag:<10}{s[0]:>6}{s[1]:>8}{s[1]/s[0]:>8.1%}{s[2]/s[0]:>8.1%}{rule_weight(stats, tag):>7.2f}")

    scores, reasons, run_info, hist = score_numbers(date, kjh, stats)
    if hist:
        print(f"\n上一期 {hist[-1][0]}({hist[-1][1]}) 连号: {adjacent_runs(hist[-1][2])}")
        if len(hist) >= 2:
            print(f"  上两期({hist[-2][0]}+{hist[-1][0]})合起来的连号 -> 上期号码:")
            for run, cand in two_draw_runs(hist):
                print(f"    {str(run):<20} -> {' '.join(f'{n:02d}' for n in cand)}")
        found = history_adjacent_numbers(hist)
        print(f"  上期开奖号在最近{LOOKBACK}期内最近一次连号的邻号(共{len(found)}个号找到):")
        for n, ago, issue, nbrs in found:
            print(f"    {n:02d} -> 往前{ago}期 {issue} 开过 "
                  f"{','.join(f'{x:02d}' for x in sorted(nbrs + [n]))}  候选: {' '.join(f'{m:02d}' for m in nbrs)}")
    print("\n本期预测文件号段:")
    for tag, run, w in sorted(run_info, key=lambda x: -x[2]):
        print(f"  {tag:<8} {str(run):<20} 权重{w:.2f}")

    actual = {d: nums for _, d, nums in kjh}.get(date)
    top20 = [n for n, _ in sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:20]]
    print("\n号码得分前20:")
    for n in top20:
        mark = " ★中" if actual and n in actual else ""
        print(f"  {n:02d}  {scores[n]:.2f}{mark}  {'; '.join(reasons[n])}")
    print(f"\n得分前20数组: {top20}")
    print(f"得分前20(排序): {sorted(top20)}")
    if actual:
        hit = sorted(set(top20) & actual)
        print(f"得分前20中奖数组: {hit}  (中{len(hit)}个, 随机期望5个)")

    bets = make_bets(date, scores, run_info)
    print(f"\n========== {date} 预测 ==========")
    lines = []
    for size in BET_SIZES:
        for i, bet in enumerate(bets[size], 1):
            s = " ".join(f"{n:02d}" for n in bet)
            hit = f"  -> 中{len(set(bet) & actual)}个 {sorted(set(bet) & actual)}" if actual else ""
            print(f"  {size:>2}码 第{i}注({BET_NAMES[i - 1]}): {s}{hit}")
            lines.append([size, i, BET_NAMES[i - 1], s])

    uniq, ubets = make_unique_bets(date, scores)
    print(f"\n========== {date} 独有号选十 (kl8_{date}.csv 第{'/'.join(map(str, UNIQUE_ROWS))}行) ==========")
    if uniq is None:
        print(f"  kl8_{date}.csv 不存在或不足 {max(UNIQUE_ROWS)} 行, 跳过")
    else:
        fmt = lambda xs: " ".join(f"{n:02d}" for n in xs)
        hit = (lambda xs: f"  中{len(set(xs) & actual)}个 {sorted(set(xs) & actual)}") if actual else (lambda xs: "")
        for i in UNIQUE_ROWS:
            print(f"  ck{i:<2} 独有({len(uniq[i])}个): {fmt(uniq[i])}{hit(uniq[i])}")
        all_u = sorted(n for nums in uniq.values() for n in nums)
        print(f"  独有号合计({len(all_u)}个): {fmt(all_u)}{hit(all_u)}")
        for k, (i, bet) in enumerate(ubets, 1):
            extra = [n for n in bet if n not in uniq[i]]
            note = f"  (补 {fmt(extra)})" if extra else ""
            print(f"  选十 第{k}注(ck{i}独有): {fmt(bet)}{hit(bet)}{note}")
            lines.append([UNIQUE_SIZE, k, f"ck{i}独有", fmt(bet)])
    if actual:
        print(f"  当期开奖: {' '.join(f'{n:02d}' for n in sorted(actual))}")

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"kl8_adjacent_{date}.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["码数", "注", "方案", "号码"])
        w.writerows(lines)
    print(f"\n已保存: {out}")


if __name__ == "__main__":
    main()
