from collections import Counter
import csv
import data_analysis

filename = "./zip/kl8_20241128.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
result = {}
# 使用示例
df = data_analysis.read_and_clean_data(filename)
# counter_pairs = data_analysis.count_pairs(df)
# data_analysis.print_common_pairs(counter_pairs)

searchNums = [3,5,14,22,23,24,25,28,33,34,44,45,53,55,61,68,69,75,76,79]
r=3
counter_searchNums = data_analysis.search_pairs2(df, searchNums,r)
# data_analysis.print_common_pairs(counter_searchNums)

data_analysis.print_common_pairs2(counter_searchNums,searchNums)