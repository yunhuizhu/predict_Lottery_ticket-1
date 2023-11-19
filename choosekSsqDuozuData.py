import pandas as pd
from collections import Counter

from itertools import combinations

# 读取csv文件，假设文件名为data.csv，且包含表头
df = pd.read_csv('data/ssq/data.csv', header=0)
# 读取csv文件的前100行，假设文件名为data.csv，且包含表头
# df = pd.read_csv('data/kl8/data.csv', header=0, nrows=100)
# 去掉前两列
df = df.iloc[:,2:-1]

# 统计19和其他数字一起出现的次数
r =3
# 统计19和其他数字一起出现的次数
searchNum =  26
# 统计所有数字对出现的次数
counter_pairs = Counter()
for index, row in df.iterrows():
    sorted_row = sorted(row.values)
    for pair in combinations(sorted_row, r):
            counter_pairs[pair] += 1

# 找出出现次数最多的10个数字对
most_common_pairs = counter_pairs.most_common(10)
for pair, count in most_common_pairs:
    print(f'{pair}一起出现的次数最多，次数为{count}')

counter_19 = Counter()
for index, row in df.iterrows():
    # if searchNum in row.values:
        sorted_row = sorted(row.values)
        for pair in combinations(sorted_row, r):
                if searchNum in pair:
                    counter_19[pair] += 1

# 找出与19一起出现次数最多的数字
most_common_19 = counter_19.most_common(6)  # 排除19自身，取前5个
for num, count in most_common_19[1:]:  # 排除19自身
    print(f'{searchNum}与{num}一起出现的次数最多，次数为{count}')
