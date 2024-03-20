import csv
from collections import Counter

# 读取CSV文件
with open('./zip/sd_20240320.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过第一行
    columns = [[] for _ in range(3)]  # 创建三个数组，分别用于存储每列的值

    # 循环遍历每一行，将每列的值放入对应的数组中
    for row in reader:
        for i in range(3):
            columns[i].append(int(row[i]))

    # 打印出每列数组中不包含0到9的数字
    for i, col in enumerate(columns):
        missing_numbers = [num for num in range(10) if num not in col]
        print(f"列{i + 1}中不包含的数字: {missing_numbers}")

    # 打印出每列数组中各个数字的次数
    for i, col in enumerate(columns):
        counts = Counter(col)
        print(f"列{i + 1}中各个数字的次数: {counts}")
    # 统计所有数字的出现次数
    all_numbers = [num for col in columns for num in col]
    number_counts = Counter(all_numbers)

    # 打印出各个数字出现的次数
    for num, count in number_counts.items():
        print(f"数字{num}出现了{count}次")