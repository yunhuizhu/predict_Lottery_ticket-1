"""
双色球 规则预测

一期 = 上一次开奖日之后 ~ 本次开奖日 (双色球周二、四、日开奖)。
本期用到的预测文件 (与 online_optimize.py 口径一致):
  - ssq_<日期>_h.csv : 有效日期 = 文件日期 + 1 天, 例: 周四开奖用 周二_h、周三_h
  - ssq_<日期>.csv   : 有效日期 = 文件日期, 本期每个文件都用
  - ssq_<日期>_1.csv : 有效日期 = 文件日期, 本期每天的都用 (通常开奖后才出来, 没有就跳过)

规则:
  1. _h 红球杀号: 每天的 _h 文件单独统计每个红球出现次数,
     任何一天出现 >= 4 次(common4 以上)的红球杀掉;
     所有 _h 文件里一次都没出现(common0)的红球也杀掉
  2. _h 蓝球: 第一天 _h 的蓝球 - 后面所有天 _h 的蓝球 (第一天出现、之后每天都没出现的蓝球)
  3. _1 红球: 每天的 _1 文件单独统计每个红球出现次数, common0、common1、common2 (出现 0~2 次) 是当天出球范围;
     本期出球范围 = 每天出球范围的交集 (任何一天出现 >= 3 次就不要)
  4. 普通版红球: 本期每个普通版文件都取 ckred1、ckred3、ckred5、ckred10 (文件第 1、3、5、10 行), 合起来作为出球范围
  最终红球候选 = 普通版 ckred1/3/5/10 并集 ∩ _1 出球范围(有 _1 时) - _h 杀号

出号:
  - 红球候选按支持度排序。支持度 = 普通版次数 + _h 加分:
      普通版次数: 本期所有普通版文件的 ckred 行(CKRED_ROWS)里, 这个号一共出现在几行就是几分
                  例: 2 个普通版文件 × 3 行 = 6 行, 16 在其中 4 行出现 -> 4 分
      _h 加分:    这个号在某一天 _h 里的最大出现次数为 2 或 3 次时 +0.5
                  (出现 0 次或 >=4 次的已被杀号, 1 次不加分)
    支持度相同时按号码从小到大排
  - 输出候选复式(全部候选)、红球前 10 个、5 注单式(任意两注红球最多共用 3 个)
  - 胆拖: 红球候选前 5 个做胆, 第 6~10 个做拖, 蓝球 2 个; 展开 5 × 2 = 10 注(20元)
    红球不足 10 个时按补号规则补; 蓝球候选按第一天 _h 里出现次数排序取前 2, 不足 2 个时用第一天 _h 次数最多的蓝球补

开奖数据读 data/online_optimizer/ssq_results.csv (由 online_optimize.py --fetch 更新),
预测文件读 zip/ 和 data/online_optimizer/pred_archive/ (zip 优先)。

用法:
  python ssq_adjacent_predict.py                 # 默认预测 zip 中最新文件之后的下一个开奖日
  python ssq_adjacent_predict.py 20261112        # 指定开奖日期(已开奖的日期会直接对比中奖)
  python ssq_adjacent_predict.py 20261103 20261105 20261108   # 一次预测多个日期
  python ssq_adjacent_predict.py 20261103 --fetch # 先抓最新开奖再预测(缺开奖数据时会自动抓)
  python ssq_adjacent_predict.py 20261112 --no-1 # 不用 _1 文件
  python ssq_adjacent_predict.py --compare       # 用所有已开奖的期回测规则命中情况
"""

import csv
import os
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from itertools import combinations

BASE = os.path.dirname(os.path.abspath(__file__))
ZIP_DIR = os.path.join(BASE, "zip")
ARCHIVE_DIR = os.path.join(BASE, "data", "online_optimizer", "pred_archive")
RESULT_FILE = os.path.join(BASE, "data", "online_optimizer", "ssq_results.csv")
OUT_DIR = os.path.join(BASE, "predict_out")

NAME_RE = re.compile(r"ssq_(20\d{6})(?:_(h|1))?\.csv")
CKRED_ROWS = ( 3, 5, 10)       # 普通版取第几行
H_KILL_MAX = 4                   # _h 出现次数 >= 4 杀
ONE_KEEP_MAX = 2                 # _1 出现 0~2 次为出球范围
DRAW_WEEKDAYS = (1, 3, 6)        # 周二、周四、周日开奖
TICKETS = 5


# ============================================================
# 数据读取
# ============================================================
def load_results():
    """{开奖日期: (红球列表, 蓝球)}"""
    data = {}
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                nums = [int(x) for x in row["numbers"].split(",")]
                data[row["date"]] = (sorted(nums[:6]), nums[6])
    return data


def fetch_results():
    """抓 17500 双色球开奖页并合并到 RESULT_FILE (与 online_optimize.py 共用缓存)"""
    import requests
    from online_optimize import URLS, HEADERS, parse_page
    resp = requests.get(URLS["ssq"], headers=HEADERS, timeout=30)
    resp.raise_for_status()
    parsed = parse_page("ssq", resp.text)
    if not parsed:
        print("未解析到双色球开奖数据, 保留旧缓存")
        return
    old = {}
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, encoding="utf-8") as f:
            old = {row["date"]: row["numbers"] for row in csv.DictReader(f)}
    old.update({d: ",".join(map(str, v)) for d, v in parsed.items()})
    os.makedirs(os.path.dirname(RESULT_FILE), exist_ok=True)
    with open(RESULT_FILE, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "numbers"])
        for d in sorted(old):
            w.writerow([d, old[d]])
    print(f"双色球开奖: 抓取 {len(parsed)} 期, 本地共 {len(old)} 期")


PRIZES = {(6, 1): "一等奖", (6, 0): "二等奖", (5, 1): "三等奖", (5, 0): "四等奖", (4, 1): "四等奖",
          (4, 0): "五等奖", (3, 1): "五等奖", (2, 1): "六等奖", (1, 1): "六等奖", (0, 1): "六等奖"}


def prize(red, blue, actual):
    r = len(set(red) & set(actual[0]))
    b = int(blue == actual[1])
    return r, b, PRIZES.get((r, b), "未中奖")


def all_files():
    """{(文件日期, 来源): 路径}, 来源 normal/h/1; zip 优先于归档"""
    files = {}
    for d in (ARCHIVE_DIR, ZIP_DIR):
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            m = NAME_RE.fullmatch(name)
            if m:
                files[(m[1], m[2] or "normal")] = os.path.join(d, name)
    return files


def read_rows(path):
    """返回 [(红球6个, 蓝球)], 跳过标题和不合法的行"""
    rows = []
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            try:
                nums = [int(x) for x in row]
            except ValueError:
                continue
            if len(nums) == 7 and len(set(nums[:6])) == 6 and all(1 <= n <= 33 for n in nums[:6]) \
                    and 1 <= nums[6] <= 16:
                rows.append((sorted(nums[:6]), nums[6]))
    return rows


def shift(date, days):
    return (datetime.strptime(date, "%Y%m%d") + timedelta(days=days)).strftime("%Y%m%d")


def is_draw_day(date):
    return datetime.strptime(date, "%Y%m%d").weekday() in DRAW_WEEKDAYS


def prev_draw(date):
    d = shift(date, -1)
    while not is_draw_day(d):
        d = shift(d, -1)
    return d


def next_draw(date):
    d = date
    while not is_draw_day(d):
        d = shift(d, 1)
    return d


def period_files(target, files):
    """本期文件: 上一开奖日 < 有效日期 <= target。返回 {来源: [(文件日期, 路径)]} 按日期排序"""
    start = prev_draw(target)
    result = {"normal": [], "h": [], "1": []}
    for (date, source), path in files.items():
        effective = shift(date, 1) if source == "h" else date
        if start < effective <= target:
            result[source].append((date, path))
    for v in result.values():
        v.sort()
    return result


# ============================================================
# 规则
# ============================================================
def red_counts(rows):
    """每个红球(1~33)出现次数, 没出现的为 0"""
    c = Counter(n for red, _ in rows for n in red)
    return {n: c.get(n, 0) for n in range(1, 34)}


def group_by_count(counts):
    """{次数: [号码]}, 即 common0、common1 ..."""
    groups = {}
    for n, c in counts.items():
        groups.setdefault(c, []).append(n)
    return dict(sorted(groups.items()))


def apply_rules(target, files, use_1=True):
    """计算本期各规则结果, 返回 dict; 没有普通版文件时返回 None"""
    pf = period_files(target, files)
    info = {"target": target, "files": pf}
    if not pf["normal"]:
        return None

    # 规则1: _h 红球杀号
    # 每天单独统计; 任何一天 >= H_KILL_MAX 次杀, 所有天合计 0 次杀
    day_counts = [(date, red_counts(read_rows(p))) for date, p in pf["h"]]
    info["h_days"] = [(date, group_by_count(c)) for date, c in day_counts]
    h_counts = {n: sum(c[n] for _, c in day_counts) for n in range(1, 34)} if day_counts else {}
    kill = set()
    for _, c in day_counts:
        kill |= {n for n, v in c.items() if v >= H_KILL_MAX}
    kill |= {n for n, v in h_counts.items() if v == 0}
    info["kill"] = sorted(kill)
    # 打分/补号用: 每天的最大次数(没被杀的号都在 1~3 次)
    info["h_counts"] = {n: max(c[n] for _, c in day_counts) for n in range(1, 34)} if day_counts else {}
    h_counts = info["h_counts"]

    # 规则2: _h 蓝球 第一天 - 后面所有天
    info["first_blue_count"] = Counter(b for _, b in read_rows(pf["h"][0][1])) if pf["h"] else Counter()
    if len(pf["h"]) >= 2:
        first = {b for _, b in read_rows(pf["h"][0][1])}
        later = {}
        for date, path in pf["h"][1:]:
            later[date] = {b for _, b in read_rows(path)}
        rest = set().union(*later.values())
        info["blue"] = sorted(first - rest)
        info["blue_note"] = (f"{pf['h'][0][0]}_h 蓝球 {fmt(sorted(first))} 减去 "
                             + "、".join(f"{d}_h {fmt(sorted(v))}" for d, v in later.items()))
    elif pf["h"]:
        info["blue"] = sorted({b for _, b in read_rows(pf["h"][0][1])})
        info["blue_note"] = f"只有一天 _h({pf['h'][0][0]}), 暂用它的全部蓝球"
    else:
        info["blue"] = []
        info["blue_note"] = "本期没有 _h 文件"

    # 规则3: _1 红球 每天单独统计, 当天 common0~2 出球, 多天取交集
    info["one_pool"] = None
    if use_1 and pf["1"]:
        info["one_days"] = []
        pool1 = set(range(1, 34))
        for date, path in pf["1"]:
            counts = red_counts(read_rows(path))
            keep = {n for n, c in counts.items() if c <= ONE_KEEP_MAX}
            info["one_days"].append((date, group_by_count(counts), sorted(keep)))
            pool1 &= keep
        info["one_pool"] = sorted(pool1)

    # 规则4: 普通版 ckred1/3/5/10
    # 本期每个普通版文件都取第 3/5/10 行, key = (文件日期, 行号)
    info["ckred"] = {}
    for date, path in pf["normal"]:
        normal_rows = read_rows(path)
        for i in CKRED_ROWS:
            if i <= len(normal_rows):
                info["ckred"][(date, i)] = normal_rows[i - 1][0]
    support = Counter(n for red in info["ckred"].values() for n in red)
    normal_pool = set(support)

    pool = normal_pool
    if info["one_pool"] is not None:
        pool &= set(info["one_pool"])
    pool -= set(info["kill"])

    # 支持度 = 普通版 ckred 行中出现的行数 + (_h 单日最大次数为 2~3 时 +0.5)
    info["support"] = support
    score = {}
    for n in pool:
        sc = support[n]
        if 2 <= h_counts.get(n, 0) < H_KILL_MAX:
            sc += 0.5
        score[n] = sc
    info["score"] = score
    info["pool"] = sorted(pool, key=lambda n: (-score[n], n))
    return info


def fill_pool(info, size):
    """红球候选不足 size 个时补号: 先用 ckred 中没被杀的号(不看 _1, 按 ckred 出现行数), 再用 _h common1~3 的号。
    返回 (补齐后的候选, 补进来的号)"""
    pool = list(info["pool"])
    if len(pool) >= size:
        return pool, []
    h = info["h_counts"]
    support = Counter(n for red in info["ckred"].values() for n in red)
    extra = sorted(set(support) - set(pool) - set(info["kill"]), key=lambda n: (-support[n], -h.get(n, 0), n))
    extra += sorted((n for n in range(1, 34) if 1 <= h.get(n, 0) < H_KILL_MAX
                     and n not in pool and n not in extra), key=lambda n: (-h[n], n))
    added = extra[:size - len(pool)]
    for n in added:
        info["score"].setdefault(n, 0)
    return pool + added, added


def make_dantuo(info, dan=5, tuo=5, blues=2):
    """5胆5拖2蓝: 候选前 dan 个做胆, 接下来 tuo 个做拖; 蓝球取 blues 个。
    返回 (胆, 拖, 蓝, 补进来的红球, 展开的单式); 红球不足 dan+tuo 个时返回 None"""
    pool, added = fill_pool(info, dan + tuo)
    if len(pool) < dan + tuo:
        return None
    first = info["first_blue_count"]
    blue_rank = sorted(info["blue"], key=lambda b: (-first[b], b))
    blue_rank += [b for b, _ in sorted(first.items(), key=lambda x: (-x[1], x[0])) if b not in blue_rank]
    blue_nums = sorted(blue_rank[:blues])
    dan_nums, tuo_nums = sorted(pool[:dan]), sorted(pool[dan:dan + tuo])
    tickets = [(sorted(dan_nums + [t]), b) for t in tuo_nums for b in blue_nums] if dan == 5 else \
              [(sorted(dan_nums + list(c)), b) for c in combinations(tuo_nums, 6 - dan) for b in blue_nums]
    return dan_nums, tuo_nums, blue_nums, added, tickets


def make_tickets(info, count=TICKETS):
    """从候选里出单式: 按支持度优先, 任意两注红球最多共用 3 个; 蓝球轮流使用"""
    pool, added = fill_pool(info, 8) if len(info["pool"]) < 6 else (list(info["pool"]), [])
    if added:
        info["fill"] = added
    if len(pool) < 6:
        return []
    info = dict(info, pool=pool)
    blues = info["blue"] or [None]
    tickets, used = [], Counter()
    # 每注从支持度高的号开始选, 已用次数多的号往后排, 让各注分散
    for k in range(count * 3):
        if len(tickets) >= count:
            break
        ranked = sorted(pool, key=lambda n: (used[n], -info["score"][n], (n * 7 + k) % 33))
        red = sorted(ranked[:6])
        if any(len(set(red) & set(t[0])) > 3 for t in tickets) or any(red == t[0] for t in tickets):
            for n in red[:2]:
                used[n] += 1
            continue
        tickets.append((red, blues[len(tickets) % len(blues)]))
        for n in red:
            used[n] += 1
    return tickets


# ============================================================
# 输出
# ============================================================
def fmt(nums):
    return " ".join(f"{n:02d}" for n in nums)


def show(info, actual):
    pf = info["files"]
    names = lambda src: ", ".join(os.path.basename(p) for _, p in pf[src]) or "无"
    print(f"\n本期参考文件: 普通版[{names('normal')}]  _h[{names('h')}]  _1[{names('1')}]")
    print("  普通版每个文件都取 ckred1/3/5/10" + ("，_1 每天单独统计" if info["one_pool"] is not None else ""))

    hit = (lambda xs: f"  中{len(set(xs) & set(actual[0]))}个 {fmt(sorted(set(xs) & set(actual[0])))}") \
        if actual else (lambda xs: "")

    print("\n规则1 _h 红球统计 (每天单独统计, 任何一天 common4 以上杀; 所有天都没出现的杀):")
    for date, groups in info["h_days"]:
        print(f"  {date}_h:")
        for c, nums in groups.items():
            print(f"    common{c}: {fmt(nums)}")
    print(f"  杀号({len(info['kill'])}个): {fmt(info['kill'])}{hit(info['kill'])}")

    print(f"\n规则2 _h 蓝球: {info['blue_note']}")
    print(f"  蓝球候选: {fmt(info['blue']) or '无'}"
          + (f"  -> 开奖蓝球 {actual[1]:02d} {'命中' if actual[1] in info['blue'] else '未中'}" if actual else ""))

    if info["one_pool"] is not None:
        print("\n规则3 _1 红球统计 (每天单独统计, 当天 common0~2 出球, 多天取交集):")
        for date, groups, keep in info["one_days"]:
            print(f"  {date}_1:")
            for c, nums in groups.items():
                print(f"    common{c}: {fmt(nums)}")
            print(f"    当天出球({len(keep)}个): {fmt(keep)}{hit(keep)}")
        print(f"  本期出球范围({len(info['one_pool'])}个): {fmt(info['one_pool'])}{hit(info['one_pool'])}")
    else:
        print("\n规则3 _1: 本期没有 _1 文件或已用 --no-1 关闭, 跳过")

    print("\n规则4 普通版红球:")
    for (date, i), red in info["ckred"].items():
        print(f"  {date} ckred{i:<2}: {fmt(red)}{hit(red)}")
    normal_all = sorted({n for red in info["ckred"].values() for n in red})
    print(f"  合并({len(normal_all)}个): {fmt(normal_all)}{hit(normal_all)}")
    support = info["support"]
    print(f"  出现次数(共 {len(info['ckred'])} 行):")
    for c in sorted(set(support.values()), reverse=True):
        nums = sorted(n for n in support if support[n] == c)
        print(f"    {c}次: {fmt(nums)}{hit(nums)}")

    pool = info["pool"]
    print(f"\n最终红球候选({len(pool)}个, 按支持度): {fmt(pool)}{hit(pool)}")
    h = info["h_counts"]
    print("  支持度 = 普通版次数 + _h加分(单日 _h 出现 2~3 次 +0.5):")
    for n in pool:
        bonus = 0.5 if 2 <= h.get(n, 0) < H_KILL_MAX else 0
        mark = " ★中" if actual and n in actual[0] else ""
        print(f"    {n:02d}: {info['score'][n]:g} = 普通版{support[n]}次 + _h加分{bonus:g}"
              f" (_h单日最多{h.get(n, 0)}次){mark}")
    if actual:
        rnd = len(pool) * 6 / 33
        print(f"  随机选 {len(pool)} 个红球期望中 {rnd:.2f} 个")
    print(f"候选复式(排序): {fmt(sorted(pool))}  蓝球: {fmt(info['blue']) or '无'}")
    print(f"红球前10: {fmt(sorted(pool[:10]))}{hit(pool[:10])}")

    tickets = make_tickets(info)
    print(f"\n========== {info['target']} 单式 {len(tickets)} 注 ==========")
    lines = []
    for i, (red, blue) in enumerate(tickets, 1):
        b = f"{blue:02d}" if blue else "--"
        res = ""
        if actual:
            r, bh, label = prize(red, blue, actual)
            res = f"  -> 红{r}个 蓝{'中' if bh else '未中'} {label}"
        print(f"  第{i}注: {fmt(red)} + {b}{res}")
        lines.append([i, fmt(red), b])
    if actual:
        print(f"  {info['target']} 开奖: {fmt(actual[0])} + {actual[1]:02d}")
    else:
        print(f"  {info['target']} 还没有开奖数据(未开奖, 或加 --fetch 更新)")
    if info.get("fill"):
        print(f"  红球候选不足 6 个, 补号: {fmt(info['fill'])} (ckred 未杀号优先, 其次 _h common1~3)")
    if not tickets:
        print("  补号后仍不足 6 个, 无法出单式")

    dantuo = make_dantuo(info)
    print(f"\n========== {info['target']} 胆拖 (红球5胆5拖, 蓝球2个) ==========")
    if dantuo is None:
        print("  红球候选补号后仍不足 10 个, 无法出胆拖")
    else:
        dan_nums, tuo_nums, blue_nums, added, dt_tickets = dantuo
        print(f"  红胆: {fmt(dan_nums)}{hit(dan_nums)}")
        print(f"  红拖: {fmt(tuo_nums)}{hit(tuo_nums)}")
        print(f"  蓝球: {fmt(blue_nums)}"
              + (f"  -> 开奖蓝球 {actual[1]:02d} {'命中' if actual[1] in blue_nums else '未中'}" if actual else ""))
        if added:
            print(f"  (红球候选不足 10 个, 补号: {fmt(added)})")
        print(f"  展开 {len(dt_tickets)} 注, 共 {len(dt_tickets) * 2} 元")
        if actual:
            labels = Counter(prize(r, b, actual)[2] for r, b in dt_tickets)
            best = max(dt_tickets, key=lambda t: prize(t[0], t[1], actual)[:2])
            print("  展开中奖情况: " + ", ".join(f"{k}{v}注" for k, v in sorted(labels.items())))
            r, bh, label = prize(best[0], best[1], actual)
            print(f"  最好一注: {fmt(best[0])} + {best[1]:02d}  红{r}个 蓝{'中' if bh else '未中'} {label}")
        lines.append(["胆", fmt(dan_nums), ""])
        lines.append(["拖", fmt(tuo_nums), fmt(blue_nums)])

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"ssq_rule_{info['target']}.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["注", "红球", "蓝球"])
        w.writerows(lines)
        w.writerow(["复式", fmt(sorted(pool)), fmt(info["blue"])])
    print(f"\n已保存: {out}")


def compare(files, results, use_1):
    """逐期回测: 每个规则的命中个数和随机期望对比"""
    print(f"\n逐期回测 ({'含' if use_1 else '不含'} _1)")
    print(f"  {'开奖日':<10}{'杀号(中)':>10}{'_1范围(中)':>12}{'候选(中)':>10}{'随机':>7}{'蓝候选':>8}{'蓝中':>5}")
    tot = Counter()
    for date in sorted(results):
        info = apply_rules(date, files, use_1)
        if not info:
            continue
        red, blue = results[date]
        k, pool = info["kill"], info["pool"]
        kh = len(set(k) & set(red))
        ph = len(set(pool) & set(red))
        one = info["one_pool"]
        one_s = f"{len(one)}({len(set(one) & set(red))})" if one is not None else "-"
        bh = blue in info["blue"]
        print(f"  {date:<10}{f'{len(k)}({kh})':>10}{one_s:>12}{f'{len(pool)}({ph})':>10}"
              f"{len(pool) * 6 / 33:>7.2f}{len(info['blue']):>8}{'中' if bh else '-':>5}")
        tot["n"] += 1
        tot["kill"] += len(k); tot["kill_hit"] += kh
        tot["pool"] += len(pool); tot["pool_hit"] += ph
        tot["blue"] += len(info["blue"]); tot["blue_hit"] += bh
        dt = make_dantuo(info)
        if dt:
            dan_nums, tuo_nums, blue_nums, _, dt_tickets = dt
            tot["dt"] += 1
            tot["dan_hit"] += len(set(dan_nums) & set(red))
            tot["tuo_hit"] += len(set(tuo_nums) & set(red))
            tot["dt_blue"] += blue in blue_nums
            tot["dt_win"] += sum(prize(r, b, (red, blue))[2] != "未中奖" for r, b in dt_tickets)
            print(f"  {'':<10}胆拖: 胆中{len(set(dan_nums) & set(red))} 拖中{len(set(tuo_nums) & set(red))} "
                  f"蓝{'中' if blue in blue_nums else '未中'}")
    n = tot["n"]
    if not n:
        print("  没有可回测的期 (需要已开奖且有预测文件)")
        return
    print(f"\n累计 {n} 期:")
    print(f"  杀号: 共杀 {tot['kill']} 个, 误杀 {tot['kill_hit']} 个, 随机期望误杀 {tot['kill'] * 6 / 33:.1f} 个"
          f"  (误杀越少越好)")
    print(f"  红球候选: 共 {tot['pool']} 个, 中 {tot['pool_hit']} 个, 随机期望 {tot['pool'] * 6 / 33:.1f} 个")
    print(f"  蓝球: 共 {tot['blue']} 个候选, 中 {tot['blue_hit']} 期, 随机期望 {tot['blue'] / 16:.1f} 期")
    if tot["dt"]:
        k = tot["dt"]
        print(f"  胆拖 {k} 期: 胆共中 {tot['dan_hit']} 个(随机期望 {k * 5 * 6 / 33:.1f}), "
              f"拖共中 {tot['tuo_hit']} 个(随机期望 {k * 5 * 6 / 33:.1f}), "
              f"蓝中 {tot['dt_blue']} 期(随机期望 {k * 2 / 16:.1f}), 中奖 {tot['dt_win']} 注 / 共 {k * 10} 注")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    use_1 = "--no-1" not in sys.argv
    files = all_files()
    results = load_results()

    if "--compare" in sys.argv:
        compare(files, results, use_1)
        return

    if args:
        targets = args
    else:
        latest = max(d for d, _ in files) if files else datetime.now().strftime("%Y%m%d")
        targets = [next_draw(latest)]
    targets = [t if is_draw_day(t) else next_draw(t) for t in targets]

    # 指定 --fetch, 或要预测的已过去日期在本地没有开奖数据时, 抓一次开奖
    today = datetime.now().strftime("%Y%m%d")
    if "--fetch" in sys.argv or any(t <= today and t not in results for t in targets):
        try:
            fetch_results()
            results = load_results()
        except Exception as e:
            print(f"抓取开奖失败({e}), 使用本地数据")

    for i, target in enumerate(targets):
        if i:
            print("\n" + "#" * 60)
        print(f"预测开奖日: {target} (上一开奖日 {prev_draw(target)})")
        info = apply_rules(target, files, use_1)
        if info is None:
            print("本期没有普通版预测文件, 无法预测(zip 和归档里都没有这期的文件)")
            continue
        show(info, results.get(target))


if __name__ == "__main__":
    main()
