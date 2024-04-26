import pandas as pd
from collections import Counter
from itertools import combinations

def read_and_clean_data(file_path):
    df = pd.read_csv(file_path, header=0)
    # df = df.iloc[:,2:]
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
    for pair, count in counter.most_common(20):
        print(f'Combination: {pair}, Count: {count}')