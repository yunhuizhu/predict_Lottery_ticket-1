#!/usr/bin/env python3
"""预测文件的开奖回测、来源评分和加权候选生成。

用法:
  python checkAndChoose/online_optimize.py --fetch
  python checkAndChoose/online_optimize.py --date 20261011 --fetch
  python checkAndChoose/online_optimize.py --date 20261011 --with-1   # 开奖后复盘, 加读 _1 文件

预测文件日期表示预测当天。开奖页面仅用于回填已经开奖的日期；未来日期会保留为待评估。

预测文件来源按文件名后缀区分: xx_日期.csv=normal, xx_日期_h.csv=h, xx_日期_1.csv=1,
三种来源分别回测、分别算权重。_1 文件通常开奖后才有, 默认不读, 加 --with-1 才读。每次运行会把 zip 里的预测文件复制到
data/online_optimizer/pred_archive/, zip 清理后历史回测仍然可用。

来源权重 = 1 + (提升倍数 - 1) × n/(n+10), 提升倍数 = 该来源每行平均命中 / 随机选号期望命中,
n 为已开奖的文件数; 样本少时权重接近 1, 长期打不过随机的来源权重会低于 1。
"""
from __future__ import annotations

import argparse
import csv
from html.parser import HTMLParser
import re
import shutil
import random
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from itertools import combinations
from pathlib import Path
from typing import Iterable

import requests

ROOT = Path(__file__).resolve().parent
PRED_DIR = ROOT / "zip"
DATA_DIR = ROOT / "data" / "online_optimizer"
ARCHIVE_DIR = DATA_DIR / "pred_archive"
INCLUDE_H = True
# _1 文件通常开奖后才出来, 默认不读; 开奖后复盘时用 --with-1
INCLUDE_1 = False
# 预测文件名: 前缀_日期[_h|_1].csv
NAME_RE = re.compile(r'(sd|ssq|kl8)_(20\d{6})(?:_(h|1))?')


def parse_name(path: Path) -> tuple[str, str] | None:
    """返回 (日期, 来源)；来源为 normal / h / 1，文件名不符合规则时返回 None"""
    match = NAME_RE.fullmatch(path.stem)
    if not match:
        return None
    return match[2], match[3] or 'normal'


def allowed_prediction(path: Path) -> bool:
    parsed = parse_name(path)
    return (parsed is not None and (INCLUDE_H or parsed[1] != 'h')
            and (INCLUDE_1 or parsed[1] != '1'))


def archive_predictions() -> int:
    """把 zip 里的预测文件复制到归档目录(新文件或 zip 中更新过的才复制)，返回复制个数"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    copied = 0
    for path in PRED_DIR.glob('*.csv'):
        if parse_name(path) is None:
            continue
        target = ARCHIVE_DIR / path.name
        if not target.exists() or target.stat().st_mtime < path.stat().st_mtime:
            shutil.copy2(path, target)
            copied += 1
    return copied


def prediction_paths(prefix: str) -> list[Path]:
    """zip 与归档目录合并，同名文件优先用 zip 里的"""
    files = {p.name: p for p in ARCHIVE_DIR.glob(f'{prefix}_*.csv')}
    files.update({p.name: p for p in PRED_DIR.glob(f'{prefix}_*.csv')})
    return sorted((p for p in files.values() if allowed_prediction(p)), key=lambda p: p.name)


def prediction_dates(prefix: str, until: str | None = None) -> list[str]:
    dates = {parse_name(p)[0] for p in prediction_paths(prefix)}
    return sorted(d for d in dates if until is None or d <= until)
URLS = {
    "3d": "https://www.17500.cn/chart/3d-kjh.html",
    "ssq": "https://www.17500.cn/chart/ssq-gzm.html",
    "kl8": "https://www.17500.cn/chart/kl8-gzm.html",
}
SPECS = {"3d": (3, 10), "ssq": (7, 33), "kl8": (20, 80)}
FILE_PREFIX = {"3d": "sd", "ssq": "ssq", "kl8": "kl8"}
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"}


def nums(text: str) -> list[int]:
    return [int(x) for x in re.findall(r"(?<!\d)\d{1,2}(?!\d)", text)]


class TableParser(HTMLParser):
    """只提取 tr/td 文本，避免依赖 BeautifulSoup。"""
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._row is not None and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None


def parse_page(kind: str, html: str) -> dict[str, list[int]]:
    """从开奖图页面的表格行中提取日期/期号和开奖号码，兼容页面表格调整。"""
    width, maximum = SPECS[kind]
    parser = TableParser()
    parser.feed(html)
    result: dict[str, list[int]] = {}
    for cells in parser.rows:
        if len(cells) < 5:
            continue
        date_match = re.search(r"20\d{2}[-/]\d{1,2}[-/]\d{1,2}", cells[1])
        if not date_match:
            continue
        date = date_match.group(0).replace("-", "").replace("/", "")
        if kind == "3d":
            # 3D 奖号如 002，不能用 int/通用数字正则，否则会丢掉前导 0。
            digits = re.sub(r"\D", "", cells[4])
            values = [int(x) for x in digits] if len(digits) == 3 else []
        else:
            values = nums(cells[4])
        if len(values) == width and all(0 <= n <= maximum for n in values):
            if kind == "ssq" and (len(set(values[:6])) != 6 or min(values) < 1 or values[6] > 16):
                continue
            if kind == "kl8" and (len(set(values)) != 20 or min(values) < 1):
                continue
            result[date] = values
    return result


def fetch_results() -> dict[str, dict[str, list[int]]]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    all_results = load_results()
    for kind, url in URLS.items():
        response = session.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        parsed = parse_page(kind, response.text)
        # 页面偶发超时/改版时不要用空结果覆盖上一次成功抓取的数据。
        if not parsed:
            print(f"{kind}: 未解析到开奖数据，保留旧缓存")
            continue
        # 旧 SSQ/KL8 缓存来自错误列，首次修复时必须重新抓取，不能用于评分。
        all_results[kind].update(parsed)
        parsed = all_results[kind]
        with (DATA_DIR / f"{kind}_results.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "numbers"])
            for date, values in sorted(parsed.items()):
                writer.writerow([date, ",".join(map(str, values))])
        print(f"{kind}: 抓取 {len(parsed)} 期")
        time.sleep(0.5)
    return all_results


def load_results() -> dict[str, dict[str, list[int]]]:
    output = {}
    for kind in URLS:
        path = DATA_DIR / f"{kind}_results.csv"
        values = {}
        if path.exists():
            with path.open(encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    values[row["date"]] = [int(x) for x in row["numbers"].split(",")]
        output[kind] = values
    return output


def prediction_files(kind: str, date: str) -> list[tuple[str, Path]]:
    """某日期的全部预测文件 [(来源, 路径)]，包括 normal、_h、_1"""
    result = []
    for path in prediction_paths(FILE_PREFIX[kind]):
        file_date, source = parse_name(path)
        if file_date == date:
            result.append((source, path))
    return result


def ssq_period_files(target: str, results: dict[str, list[int]]) -> list[tuple[str, Path]]:
    """上一期开奖日之后到目标日；_h 的有效日期为文件日期加一天。"""
    previous = max((date for date in results if date < target), default=None)
    if previous is None:
        # 没有开奖边界时不猜测周期，要求先更新开奖缓存。
        return []
    selected = []
    for path in prediction_paths('ssq'):
        file_date, source = parse_name(path)
        effective = datetime.strptime(file_date, '%Y%m%d')
        # 只有 _h 顺延一天；normal 和 _1 按文件日期
        if source == 'h':
            effective += timedelta(days=1)
        if previous < effective.strftime('%Y%m%d') <= target:
            selected.append((source, path))
    return selected


def read_predictions(path: Path, width: int, maximum: int) -> list[list[int]]:
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            try:
                values = [int(x.strip()) for x in row]
            except (ValueError, TypeError):
                continue
            if len(values) == width and all(0 <= x <= maximum for x in values):
                if width != 3 and (min(values) < 1 or len(set(values[:6] if width == 7 else values)) != (6 if width == 7 else width)):
                    continue
                if width == 7 and values[6] > 16:
                    continue
                rows.append(values)
    return rows


def score(kind: str, pred: list[int], actual: list[int]) -> tuple[int, int, int]:
    if kind == "3d":
        positional = sum(a == b for a, b in zip(pred, actual))
        unordered = sum((Counter(pred) & Counter(actual)).values())
        return positional, unordered, int(positional == 3)
    if kind == "ssq":
        red = len(set(pred[:6]) & set(actual[:6]))
        blue = int(pred[6] == actual[6])
        return red, blue, int(red == 6 and blue)
    hit = len(set(pred) & set(actual))
    return hit, 0, int(hit == 20)


def row_metric(kind: str, pred: list[int], actual: list[int]) -> float:
    """单行预测的命中指标: 3D=定位命中+0.5×不定位命中, 双色球=红球命中+0.5×蓝球, 快乐8=命中个数"""
    primary, secondary, _ = score(kind, pred, actual)
    return primary + (0.5 * secondary if kind != 'kl8' else 0)


_RANDOM_3D: dict[tuple, float] = {}


def random_metric(kind: str, actual: list[int]) -> float:
    """随机选一行时 row_metric 的期望值，用来判断来源是否强于随机"""
    if kind == '3d':
        key = tuple(actual)
        if key not in _RANDOM_3D:
            _RANDOM_3D[key] = sum(row_metric('3d', [a, b, c], actual)
                                  for a in range(10) for b in range(10) for c in range(10)) / 1000
        return _RANDOM_3D[key]
    if kind == 'ssq':
        return 6 * 6 / 33 + 0.5 / 16
    return 20 * 20 / 80


def evaluate(kind: str, results: dict[str, list[int]]) -> list[dict[str, object]]:
    width, maximum = SPECS[kind]
    rows = []
    prefix = FILE_PREFIX[kind]
    dates = sorted(results) if kind == 'ssq' else prediction_dates(prefix)
    for date in dates:
        actual = results.get(date)
        if not actual:
            continue
        files = ssq_period_files(date, results) if kind == 'ssq' else prediction_files(kind, date)
        for source, path in files:
            predictions = read_predictions(path, width, maximum)
            if not predictions:
                continue
            scores = [score(kind, p, actual) for p in predictions]
            best = tuple(max(x[i] for x in scores) for i in range(3))
            avg = sum(row_metric(kind, p, actual) for p in predictions) / len(predictions)
            rows.append({"kind": kind, "date": date, "source": source, "file": path.name,
                         "rows": len(predictions), "best_primary": best[0], "best_secondary": best[1], "jackpot": best[2],
                         "avg_metric": round(avg, 4), "random_metric": round(random_metric(kind, actual), 4)})
    return rows


def source_weights(kind: str, results: dict[str, list[int]], target: str):
    """用 target 之前已开奖的文件算各来源权重。
    返回 (权重 {来源: w}, 统计 {来源: (文件数, 平均命中, 随机期望)})"""
    stats = defaultdict(lambda: [0, 0.0, 0.0])
    for row in evaluate(kind, {d: v for d, v in results.items() if d < target}):
        s = stats[row['source']]
        s[0] += 1
        s[1] += row['avg_metric']
        s[2] += row['random_metric']
    weights, summary = {}, {}
    for source, (n, actual_sum, random_sum) in stats.items():
        lift = actual_sum / random_sum if random_sum else 1.0
        weights[source] = max(0.1, 1 + (lift - 1) * n / (n + 10))
        summary[source] = (n, actual_sum / n, random_sum / n)
    return weights, summary


def pick_diverse(ranked: Iterable[list[int]], limit: int, too_close) -> list[list[int]]:
    """按分数顺序挑选候选，和已选候选 too_close 的跳过，让候选分散；不够时放开限制补齐"""
    ranked = list(ranked)
    picked = []
    for candidate in ranked:
        if len(picked) >= limit:
            break
        if not any(too_close(candidate, other, picked) for other in picked):
            picked.append(candidate)
    for candidate in ranked:
        if len(picked) >= limit:
            break
        if candidate not in picked:
            picked.append(candidate)
    return picked


def generate_kl8_mix(target: str, results: dict[str, list[int]], limit: int = 10):
    """KL8 混合策略：前半核心组合，后半加权随机组合。"""
    core_limit = limit // 2
    width, maximum = SPECS['kl8']
    weights, _ = source_weights('kl8', results, target)
    dates = prediction_dates('kl8', target)[-30:]
    if not dates:
        return []
    # 有当天预测文件时只用当天的，和其他彩种保持一致
    if target in dates:
        dates = [target]
    frequency = Counter()
    raw = []
    for date in dates:
        recency = 1.0 + 0.25 * dates.index(date) / max(1, len(dates) - 1)
        for source, path in prediction_files('kl8', date):
            rows = read_predictions(path, width, maximum)
            file_weight = recency * weights.get(source, 1.0)
            for row in rows:
                frequency.update({n: file_weight for n in row})
                raw.append((row, file_weight))
    if not raw:
        return []
    core = {}
    for row, weight in raw:
        ticket = tuple(sorted(sorted(row, key=lambda n: (-frequency[n], n))[:10]))
        core[ticket] = max(core.get(ticket, 0), weight * sum(frequency[n] for n in ticket))
    # 核心组合之间最多共用 6 个号, 避免几注几乎一样
    core_ranked = [list(t) for t, _ in sorted(core.items(), key=lambda x: (-x[1], x[0]))]
    core_picks = pick_diverse(core_ranked, core_limit,
                              lambda a, b, _: len(set(a) & set(b)) > 6)
    rng = random.Random('kl8-random:' + target)
    ranked = sorted(frequency, key=lambda n: (-frequency[n], n))
    pool = ranked[:min(45, len(ranked))]
    random_picks, seen = [], {tuple(pick) for pick in core_picks}
    for _ in range(5000):
        row = tuple(sorted(sorted(pool, key=lambda n: rng.random() ** (1 / max(frequency[n], .01)))[:10]))
        if row in seen:
            continue
        odd = sum(n % 2 for n in row)
        high = sum(n >= 41 for n in row)
        if 3 <= odd <= 7 and 3 <= high <= 7:
            random_picks.append(list(row)); seen.add(row)
        if len(random_picks) >= limit - core_limit:
            break
    return [(p, '核心') for p in core_picks] + [(p, '随机') for p in random_picks]


def generate(kind: str, target: str, result: dict[str, list[int]], limit: int = 10, kl8_size: int = 10) -> list[list[int]]:
    width, maximum = SPECS[kind]
    weights, _ = source_weights(kind, result, target)
    position = [Counter() for _ in range(width)]
    sets = Counter()
    prefix = FILE_PREFIX[kind]
    dates = prediction_dates(prefix, target)[-30:]
    if not dates:
        return []
    groups = [ssq_period_files(target, result)] if kind == 'ssq' else [prediction_files(kind, date) for date in ([target] if target in dates else dates)]
    for files in groups:
        for source, path in files:
            weight = weights.get(source, 1.0)
            predictions = read_predictions(path, width, maximum)
            for prediction in predictions:
                weight_per_row = weight / max(1, len(predictions))
                for i, n in enumerate(prediction):
                    position[i][n] += weight_per_row
                sets[tuple(sorted(prediction))] += weight
    if not any(position[i] for i in range(width)):
        # 没有可用于评分的历史预测时，使用已有预测文件作为冷启动样本。
        # 不能让全零默认分数经过笛卡尔积排序后产生 000、001 这种假候选。
        return []
    if kind == "kl8":
        frequency = Counter()
        for counter in position:
            frequency.update(counter)
        if len(frequency) < kl8_size:
            return []
        rng = random.Random('kl8:' + target if kl8_size == 10 else f'kl8:{target}:select{kl8_size}')
        tickets = set()
        for _ in range(1000):
            ranked_numbers = sorted(frequency, key=lambda n: rng.random() ** (1 / frequency[n]), reverse=True)
            tickets.add(tuple(sorted(ranked_numbers[:kl8_size])))
            if len(tickets) >= limit:
                break
        return [list(ticket) for ticket in sorted(tickets)]
    if kind == "3d":
        candidates = ([a, b, c] for a in range(10) for b in range(10) for c in range(10))
    elif kind == "ssq":
        # 33选6×16 约 2300 万组，不能穷举。先取历史候选中评分最高的号码池。
        red_frequency = Counter()
        for counter in position[:6]:
            red_frequency.update(counter)
        red_pool = [n for n, _ in red_frequency.most_common(16)]
        blue_pool = [n for n, _ in position[6].most_common(8)]
        red_pool = red_pool or list(range(1, 34))
        blue_pool = blue_pool or list(range(1, 17))
        candidates = ([*combo, blue] for combo in combinations(sorted(red_pool), 6) for blue in blue_pool)
    else:
        # KL8预测文件本身已给出集合，取历史加权最常见的集合，避免穷举80选20。
        candidates = (list(k) for k, _ in sets.most_common())
    ranked = []
    for candidate in candidates:
        value = sum(position[i][n] for i, n in enumerate(candidate))
        if kind == "ssq":
            value = sum(red_frequency[n] for n in candidate[:6]) + position[6][candidate[6]]
        ranked.append((value, candidate))
    ranked.sort(key=lambda x: x[0], reverse=True)
    ranked = [x[1] for x in ranked]
    if kind == '3d':
        # 任意两注最多 1 个位置相同, 避免只换一位的近似号
        return pick_diverse(ranked, limit, lambda a, b, _: sum(x == y for x, y in zip(a, b)) > 1)
    if kind == 'ssq':
        # 任意两注红球最多共用 3 个, 同一个蓝球最多用 2 次
        def too_close(a, b, picked):
            blue_used = sum(p[6] == a[6] for p in picked)
            return len(set(a[:6]) & set(b[:6])) > 3 or blue_used >= 2
        return pick_diverse(ranked, limit, too_close)
    return ranked[:limit]


def span_of(row: list[int]) -> int:
    """3D 跨度 = 最大数字 - 最小数字, 范围 0~9"""
    return max(row) - min(row)


def ssq_frequency(target: str, results: dict[str, list[int]]) -> tuple[Counter, Counter]:
    """本期双色球参考文件按来源权重统计红球、蓝球得分(每个文件按行数平均), 返回 (红球得分, 蓝球得分)"""
    width, maximum = SPECS['ssq']
    weights, _ = source_weights('ssq', results, target)
    red, blue = Counter(), Counter()
    for source, path in ssq_period_files(target, results):
        predictions = read_predictions(path, width, maximum)
        for prediction in predictions:
            w = weights.get(source, 1.0) / len(predictions)
            for n in prediction[:6]:
                red[n] += w
            blue[prediction[6]] += w
    return red, blue


def generate_ssq_dantuo(target: str, results: dict[str, list[int]], dan: int = 5, tuo: int = 5, blues: int = 2):
    """双色球胆拖: 红球得分最高的 dan 个做胆码, 接下来 tuo 个做拖码, 蓝球取得分最高的 blues 个。
    红球固定选胆码, 再从拖码里选 6-dan 个; 5胆5拖2蓝 = 5 × 2 = 10 注(20元)。
    返回 (胆码, 拖码, 蓝球, 展开后的全部单式)；没有参考文件时返回 None"""
    red, blue = ssq_frequency(target, results)
    ranked_red = sorted(red, key=lambda n: (-red[n], n))
    ranked_blue = sorted(blue, key=lambda n: (-blue[n], n))
    if len(ranked_red) < dan + tuo or len(ranked_blue) < blues:
        return None
    dan_nums = sorted(ranked_red[:dan])
    tuo_nums = sorted(ranked_red[dan:dan + tuo])
    blue_nums = sorted(ranked_blue[:blues])
    tickets = [sorted(dan_nums + list(extra)) + [b]
               for extra in combinations(tuo_nums, 6 - dan) for b in blue_nums]
    return dan_nums, tuo_nums, blue_nums, tickets


def generate_feature(target: str, results: dict[str, list[int]], limit: int, feature, size: int) -> list[int]:
    """3D 独立特征模型(和值/跨度通用): 每个预测文件统计该特征的分布, 用历史 Brier 误差
    与理论分布比较给来源定权重, 再合并目标日期的文件, 取概率最高的 limit 个值。
    feature: 把一注号码映射成特征值的函数; size: 特征取值个数(和值28, 跨度10)"""
    # 三位数字完全随机时, 和值/跨度的理论分布都不是均匀分布
    prior = Counter(feature([a, b, c]) for a in range(10) for b in range(10) for c in range(10))
    prior = {s: prior[s] / 1000 for s in range(size)}
    files = []
    losses = defaultdict(list)          # 来源 -> [(该文件误差, 理论分布误差)]
    for path in prediction_paths('sd'):
        file_date, source = parse_name(path)
        if file_date > target:
            continue
        rows = read_predictions(path, 3, 10)
        if not rows:
            continue
        counts = Counter(feature(row) for row in rows)
        distribution = {s: (counts[s] + 5 * prior[s]) / (len(rows) + 5) for s in range(size)}
        files.append((file_date, source, distribution))
        if file_date < target and file_date in results:
            actual_value = feature(results[file_date])
            loss = sum((distribution[s] - int(s == actual_value)) ** 2 for s in range(size))
            base = sum((prior[s] - int(s == actual_value)) ** 2 for s in range(size))
            losses[source].append((loss, base))
    if not files:
        return []
    # 误差比理论分布小的来源权重 > 1，样本少时向 1 收缩
    weights = {}
    for source, values in losses.items():
        n = len(values)
        lift = sum(b for _, b in values) / sum(l for l, _ in values)
        weights[source] = max(0.1, 1 + (lift - 1) * n / (n + 10))
    latest = max(date for date, _, _ in files)
    selected = [entry for entry in files if entry[0] == latest]
    total_weight = sum(weights.get(source, 1) for _, source, _ in selected)
    scores = {s: sum(weights.get(source, 1) * distribution[s]
                     for _, source, distribution in selected) / total_weight for s in range(size)}
    return sorted(scores, key=lambda s: (-scores[s], s))[:limit]


def generate_sum(target: str, results: dict[str, list[int]], limit: int = 5) -> list[int]:
    """独立和值候选"""
    return generate_feature(target, results, limit, sum, 28)


def generate_span(target: str, results: dict[str, list[int]], limit: int = 6) -> list[int]:
    """独立跨度候选(跨度 = 最大数字 - 最小数字)"""
    return generate_feature(target, results, limit, span_of, 10)


def prize_label(kind: str, pick: list[int], actual: list[int]) -> str:
    if kind == '3d':
        positional, unordered, direct = score(kind, pick, actual)
        group = sorted(pick) == sorted(actual) and len(set(actual)) > 1
        label = '直选命中' if direct else ('组选命中' if group else '未中奖')
        return f'定位命中{positional}个，不定位命中{unordered}个；{label}（直选/组选分开判断）'
    if kind == 'ssq':
        red, blue, _ = score(kind, pick, actual)
        prizes = {(6, 1): '一等奖', (6, 0): '二等奖', (5, 1): '三等奖',
                  (5, 0): '四等奖', (4, 1): '四等奖', (4, 0): '五等奖',
                  (3, 1): '五等奖', (2, 1): '六等奖', (1, 1): '六等奖', (0, 1): '六等奖'}
        return f'红球{red}个，蓝球{blue}个；{prizes.get((red, blue), "未中奖")}'
    hit = len(set(pick) & set(actual))
    if len(pick) in (5, 6):
        prizes_by_size = {
            5: {5: '一等奖', 4: '二等奖', 3: '三等奖'},
            6: {6: '一等奖', 5: '二等奖', 4: '三等奖', 3: '四等奖'},
        }
        return f'选{len(pick)}命中{hit}个；{prizes_by_size[len(pick)].get(hit, "未中奖")}'
    if len(pick) != 10:
        return f'命中{hit}个；非选十号码，未判定奖级'
    prizes = {10: '一等奖', 9: '二等奖', 8: '三等奖', 7: '四等奖',
              6: '五等奖', 5: '六等奖', 0: '七等奖'}
    return f'选十命中{hit}个；{prizes.get(hit, "未中奖")}'


def main() -> None:
    global INCLUDE_H, INCLUDE_1
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y%m%d"), help="预测日期，文件日期就是当期")
    parser.add_argument("--fetch", action="store_true", help="抓取三种彩票开奖页")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--sum-limit", type=int, choices=range(1, 29), default=5, help="3D独立和值候选数，默认5个")
    parser.add_argument("--span-limit", type=int, choices=range(1, 11), default=6, help="3D独立跨度候选数，默认6个")
    h_options = parser.add_mutually_exclusive_group()
    h_options.add_argument('--no-h', dest='include_h', action='store_false', help='仅参考普通版，预测和历史评分都排除_h')
    h_options.add_argument('--with-h', dest='include_h', action='store_true', help='同时参考普通版和_h（默认）')
    parser.set_defaults(include_h=True)
    one_options = parser.add_mutually_exclusive_group()
    one_options.add_argument('--no-1', dest='include_1', action='store_false',
                             help='不读_1文件（默认，开奖前预测用），预测和历史评分都排除_1')
    one_options.add_argument('--with-1', dest='include_1', action='store_true',
                             help='同时读_1文件（开奖后复盘用）')
    parser.set_defaults(include_1=False)
    args = parser.parse_args()
    INCLUDE_H = args.include_h
    INCLUDE_1 = args.include_1
    parts = ['普通版'] + (['_h'] if INCLUDE_H else []) + (['_1'] if INCLUDE_1 else [])
    print('预测文件模式: ' + ' + '.join(parts) + ('' if INCLUDE_1 else '（不读_1）'))
    copied = archive_predictions()
    print(f'预测文件归档: 新复制 {copied} 个到 {ARCHIVE_DIR}')
    results = fetch_results() if args.fetch else load_results()
    report = []
    for kind in URLS:
        report.extend(evaluate(kind, results[kind]))
        if kind == 'kl8':
            labeled = generate_kl8_mix(args.date, results[kind], args.limit)
            picks = [p for p, _ in labeled]
            labels = [label for _, label in labeled]
        else:
            picks = generate(kind, args.date, results[kind], args.limit)
            labels = [''] * len(picks)
        samples = evaluate(kind, {d: v for d, v in results[kind].items() if d < args.date})
        if kind == 'ssq':
            used_files = ssq_period_files(args.date, results[kind])
            print('ssq 本期参考文件（_h 日期+1天）: ' + (', '.join(path.name for _, path in used_files) or '无；请检查开奖缓存与预测文件'))
        print(f"{kind}: 目标日期前已匹配 {len(samples)} 个预测文件；每次运行根据已有开奖重新计算权重")
        weights, summary = source_weights(kind, results[kind], args.date)
        for source in sorted(summary):
            n, avg, rnd = summary[source]
            print(f"  来源 {source:<6} 文件{n:>3}个  每行平均命中{avg:.3f}  随机期望{rnd:.3f}  权重{weights[source]:.3f}")
        if not summary:
            print("  暂无已开奖的历史文件，各来源权重均为 1.0")
        title = '选十建议候选（前半核心组合，后半加权随机）' if kind == 'kl8' else '建议候选'
        print(f"\n{kind} {args.date} {title}:")
        for i, pick in enumerate(picks, 1):
            formatted = ' '.join(str(n) if kind == '3d' else f'{n:02d}' for n in pick)
            print(f"{i:02d}: {formatted}" + (f"  [{labels[i - 1]}]" if labels[i - 1] else ''))
        if kind == "3d":
            sum_picks = generate_sum(args.date, results[kind], args.sum_limit)
            print("独立和值候选（按模型评分排序）: " + (' '.join(map(str, sum_picks)) or '没有有效预测文件'))
            span_picks = generate_span(args.date, results[kind], args.span_limit)
            print("独立跨度候选（按模型评分排序）: " + (' '.join(map(str, span_picks)) or '没有有效预测文件'))
        if not picks:
            print("没有有效预测文件，未生成候选。")
        actual = results[kind].get(args.date)
        draw_date = args.date
        if kind == 'ssq' and actual is None:
            # 非开奖日的预测对应下一次开奖，候选仍按原预测截止日期生成。
            next_draw = min((date for date in results[kind] if date > args.date), default=None)
            if next_draw:
                draw_date = next_draw
                actual = results[kind][next_draw]
                print(f'双色球预测截止日期 {args.date} 对应下一期开奖日期 {draw_date}')
        if actual:
            formatted_actual = ' '.join(str(n) if kind == '3d' else f'{n:02d}' for n in actual)
            print(f'开奖对比 {draw_date}（本次重新生成的历史回放候选）: {formatted_actual}')
            for i, pick in enumerate(picks, 1):
                print(f'{i:02d}: {prize_label(kind, pick, actual)}')
            if kind == '3d':
                actual_sum = sum(actual)
                print(f'实际和值: {actual_sum}；独立和值候选' + ('命中' if actual_sum in sum_picks else '未命中'))
                actual_span = span_of(actual)
                print(f'实际跨度: {actual_span}；独立跨度候选' + ('命中' if actual_span in span_picks else '未命中'))
        else:
            print('开奖对比: 缓存中没有该日期开奖结果；可用 --fetch 更新后查看。')
        if kind == 'ssq':
            dantuo = generate_ssq_dantuo(args.date, results[kind])
            print(f'\nssq {args.date} 胆拖建议（红球5胆5拖，蓝球2个）:')
            if dantuo is None:
                print('参考文件中的红球/蓝球不足，未生成胆拖。')
            else:
                dan_nums, tuo_nums, blue_nums, tickets = dantuo
                fmt = lambda xs: ' '.join(f'{n:02d}' for n in xs)
                print(f'  红胆: {fmt(dan_nums)}')
                print(f'  红拖: {fmt(tuo_nums)}')
                print(f'  蓝球: {fmt(blue_nums)}')
                print(f'  展开 {len(tickets)} 注，共 {len(tickets) * 2} 元')
                if actual:
                    red_set = set(actual[:6])
                    print(f'  开奖对比 {draw_date}: 红胆中{len(red_set & set(dan_nums))}个 {fmt(sorted(red_set & set(dan_nums)))}，'
                          f'红拖中{len(red_set & set(tuo_nums))}个 {fmt(sorted(red_set & set(tuo_nums)))}，'
                          f'蓝球{"中 " + f"{actual[6]:02d}" if actual[6] in blue_nums else "未中"}')
                    prizes = Counter(prize_label(kind, t, actual).split('；')[1] for t in tickets)
                    best = max(tickets, key=lambda t: score(kind, t, actual)[:2])
                    print(f'  展开中奖情况: ' + '，'.join(f'{k}{v}注' for k, v in sorted(prizes.items())))
                    print(f'  最好一注: {fmt(best[:6])} + {best[6]:02d}  {prize_label(kind, best, actual)}')
        if kind == 'kl8':
            for size in (5, 6):
                extra_picks = generate(kind, args.date, results[kind], args.limit, kl8_size=size)
                print(f'\nkl8 {args.date} 选{size}建议候选（{len(extra_picks)}注）:')
                for i, pick in enumerate(extra_picks, 1):
                    formatted = ' '.join(f'{n:02d}' for n in pick)
                    outcome = f'；{prize_label(kind, pick, actual)}' if actual else ''
                    print(f'{i:02d}: {formatted}{outcome}')
                if not extra_picks:
                    print('没有有效预测文件，未生成候选。')
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / "backtest.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["kind", "date", "source", "file", "rows", "best_primary", "best_secondary",
                                               "jackpot", "avg_metric", "random_metric"])
        writer.writeheader(); writer.writerows(report)
    print(f"\n已回测 {len(report)} 个预测文件，明细: {DATA_DIR / 'backtest.csv'}")


if __name__ == "__main__":
    main()
