import pandas as pd
from collections import Counter

# 读取csv文件，假设文件名为data.csv，且包含表头
# df = pd.read_csv('data/kl8/data.csv', header=0)
# 读取csv文件的前100行，假设文件名为data.csv，且包含表头
df = pd.read_csv('data/kl8/data.csv', header=0, nrows=20)
# 去掉前两列
df = df.iloc[:,2:]

# 统计19和其他数字一起出现的次数
searchNum = 16
counter_19 = Counter()
for index, row in df.iterrows():
    if searchNum in row.values:
        counter_19.update(row.values)

# 找出与19一起出现次数最多的数字
# most_common_19 = counter_19.most_common(2)[1] # 排除19自身
# print(f'19与{most_common_19[0]}一起出现的次数最多，次数为{most_common_19[1]}')

# 找出与19一起出现次数最多的数字
most_common_19 = counter_19.most_common(10) # 排除19自身，取前5个
for num, count in most_common_19[1:]: # 排除19自身
    print(f'{searchNum}与{num}一起出现的次数最多，次数为{count}')

# 统计所有数字对出现的次数
counter_pairs = Counter()
for index, row in df.iterrows():
    sorted_row = sorted(row.values)
    for i in range(len(sorted_row) -1):
        for j in range(i +1, len(sorted_row)):
            counter_pairs[(sorted_row[i], sorted_row[j])] +=1

# 找出出现次数最多的数字对
most_common_pairs = counter_pairs.most_common(10)
for pair, count in most_common_pairs:
    print(f'{pair[0]}和{pair[1]}一起出现的次数最多，次数为{count}')
