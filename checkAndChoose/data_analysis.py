import pandas as pd
from collections import Counter
from itertools import combinations
from collections import defaultdict

def build_conflict_graph(remaining_numbers_list):
    """
    构建冲突图：如果两个数字出现在同一个 remaining_numbers 队列中，
    就认为它们冲突，在图中添加一条边。

    :param remaining_numbers_list: List[List[int]] 所有 remaining_numbers 的列表
    :return: 冲突图 (dict of sets)
    """
    conflict_graph = defaultdict(set)

    for group in remaining_numbers_list:
        nums = list(group)
        # 对该组中的每一对数字建立冲突关系
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                a, b = nums[i], nums[j]
                conflict_graph[a].add(b)
                conflict_graph[b].add(a)

    return conflict_graph


def is_valid_combination(candidate_set, conflict_graph):
    """
    判断当前候选集合是否是有效的互斥组合

    :param candidate_set: 当前候选集合（set）
    :param conflict_graph: 冲突图 {num: set of conflicting nums}
    :return: True if valid, False otherwise
    """
    for num in candidate_set:
        conflicts = conflict_graph.get(num, set())
        if any(other in candidate_set for other in conflicts):
            return False
    return True


def find_all_valid_combinations(conflict_graph, all_candidates, required_size=None):
    """
    使用回溯法找出所有有效的互斥组合

    :param conflict_graph: 冲突图
    :param all_candidates: 所有可能候选数字的集合
    :param required_size: 可选参数，要求组合大小
    :return: 所有有效组合的列表
    """
    result = []
    all_candidates = sorted(all_candidates)

    def backtrack(start, path):
        if required_size is None or len(path) == required_size:
            result.append(list(path))
            return

        for i in range(start, len(all_candidates)):
            num = all_candidates[i]
            # 如果当前数字与路径中的数字冲突，则跳过
            if any(num in conflict_graph[n] for n in path):
                continue

            # 选择当前数字
            path.append(num)
            backtrack(i + 1, path)
            path.pop()  # 回溯

    backtrack(0, [])
    return result


def read_and_clean_data(file_path):
    df = pd.read_csv(file_path, header=0)
    # df = df.iloc[:,2:]
    return df

def read_and_clean_data_ssq_red(file_path):
    df = pd.read_csv(file_path, header=0)
    # 去除最后一列
    df = df.iloc[:, :-1]
    return df

def count_pairs(df, r=2):
    counter_pairs = Counter()

    for index, row in df.iterrows():
        sorted_row = sorted(row.values)
        for pair in combinations(sorted_row, r):
            counter_pairs[pair] += 1
    return counter_pairs

def search_pairs(df, searchNums, r=2):
    counter_searchNums = Counter()

    for searchNum in searchNums:
        for index, row in df.iterrows():
            if searchNum in row.values:
                sorted_row = sorted(row.values)
                for pair in combinations(sorted_row, r):
                    if searchNum in pair:
                        counter_searchNums[pair] += 1
    return counter_searchNums

def print_common_pairs(counter_pairs, count=10):
    most_common_pairs = counter_pairs.most_common(count)
    for pair, count in most_common_pairs:
        print(f'{pair} 一起出现的次数最多，次数为 {count}')
def search_pairs2(df, searchNums, r=2):
    counter_searchNums = Counter()
    set_searchNums = set(searchNums)  # 转换为集合，为了下一步操作

    for index, row in df.iterrows():
        sorted_row = sorted([val for val in row.values if val in set_searchNums])  # 在生成组合之前，先过滤掉不在searchNums内的数字
        for pair in combinations(sorted_row, r):
            counter_searchNums[pair] += 1
    return counter_searchNums
def print_common_pairs2(counter_searchNums, searchNums):
    # 转换searchNums为集合
    searchNums_set = set(searchNums)

    for pair, count in counter_searchNums.most_common():
        # 使用集合的交集来检查pair与searchNums中是否有共同的元素
        if searchNums_set & set(pair):
            print(f'Pair: {pair}, Count: {count}')


def remove_and_count(df, removeNums, r):
    set_removeNums = set(removeNums)  # 转化为集合，提高检查性能

    counter = Counter()
    for index, row in df.iterrows():
        sorted_row = sorted(val for val in row if val not in set_removeNums)  #在生成组合前，只考虑不在removeNums中的数字
        for combination in combinations(sorted_row, r):
            # 只计数不包含removeNums中任何元素的组合
            if not set(combination) & set_removeNums:
                counter[combination] += 1

    print(f"The top 20 most common combinations of {r} numbers:")
    #从最少次数的开始打印
    for pair, count in counter.most_common(40):
        print(f'Combination: {pair}, Count: {count}')
    # for pair, count in counter.most_common()[-40:]:
    #     print(f'Combination: {pair}, Count: {count}')
def remove_and_count_contain(df, removeNums, r,containNums):
    set_removeNums = set(removeNums)  # 转化为集合，提高检查性能

    counter = Counter()
    for index, row in df.iterrows():
        sorted_row = sorted(val for val in row if val not in set_removeNums)  #在生成组合前，只考虑不在removeNums中的数字
        for combination in combinations(sorted_row, r):
            # 只计数不包含removeNums中任何元素的组合
            if not set(combination) & set_removeNums:
                counter[combination] += 1

    print(f"The top 20 most common combinations of {r} numbers:")
    # for pair, count in counter.most_common(20):
    #     print(f'Combination: {pair}, Count: {count}')
    for pair, count in counter.items():
        if set(pair) & set(containNums):
            print(f'Combination: {pair}, Count: {count}')


def get_adjacent_numbers(draw,maxnum=80):
    """获取给定号码列表的邻码"""
    adjacent = set()
    for num in draw:
        if num > 1:
            adjacent.add(num - 1)
        if num < maxnum:
            adjacent.add(num + 1)
    return adjacent


def get_oblique_codes(last_draw, prev_draw,maxnum=80):
    """
    获取斜码：上上期奖号的邻码去掉上期奖号后剩余的号码

    参数:
    last_draw (list): 上期开奖号码 (20个数字)
    prev_draw (list): 上上期开奖号码 (20个数字)

    返回:
    list: 斜码列表
    """
    # 获取上上期的邻码
    adjacent_prev_draw = get_adjacent_numbers(prev_draw,maxnum)

    # 转换为集合便于操作
    last_draw_set = set(last_draw)
    prev_draw_set = set(prev_draw)

    # 去掉上期已有的号码
    oblique_codes = sorted(adjacent_prev_draw - last_draw_set)

    return oblique_codes


def get_jump_codes(last_draw, prev_draw,maxnum=80):
    """
    获取跳码：非重码也非斜码的号码

    参数:
    last_draw (list): 上期开奖号码 (20个数字)
    prev_draw (list): 上上期开奖号码 (20个数字)

    返回:
    list: 跳码列表
    """
    # 获取斜码
    oblique_codes = get_oblique_codes(last_draw, prev_draw,maxnum)

    # 转换为集合便于操作
    last_draw_set = set(last_draw)
    oblique_codes_set = set(oblique_codes)

    # 所有号码范围
    all_numbers = set(range(1, maxnum+1))

    # 跳码 = 所有号码 - 重码 - 斜码
    jump_codes = sorted(all_numbers - last_draw_set - oblique_codes_set)

    return jump_codes
# 对望码函数：将数字的个位和十位颠倒
def get_mirror_number(num):
    if num > 80 or num < 1:
        return None
    tens = num // 10
    ones = num % 10
    mirror = ones * 10 + tens
    # 确保对望码在1-80范围内
    return mirror if 1 <= mirror <= 80 else None

# 邻码函数：获取数字的前后相邻数字
def get_adjacent_numbersByNum(num):
    adjacents = []
    if num > 1:
        adjacents.append(num - 1)
    if num < 80:
        adjacents.append(num + 1)
    return adjacents