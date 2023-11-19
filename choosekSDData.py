import pandas as pd
from collections import Counter
from itertools import combinations

#读取csv文件的前100行，假设文件名为data.csv，且包含表头
df = pd.read_csv('data/sd/data.csv', header=0)

# 去掉前两列
df = df.iloc[:,2:]

# 初始化一个Counter对象来统计数字对出现的次数
counter_pairs = Counter()

# 遍历每一行
for index, row in df.iterrows():
    # 对每一行的数据进行两两组合
    for pair in combinations(enumerate(row.values),2):
        # 更新计数器
        counter_pairs[pair] +=1

# 找出出现次数最多的10个数字对
most_common_pairs = counter_pairs.most_common(10)

# 打印结果
for pair, count in most_common_pairs:
    print(f'第{pair[0][0]+1}列的{pair[0][1]}和第{pair[1][0]+1}列的{pair[1][1]}一起出现的次数最多，次数为{count}')