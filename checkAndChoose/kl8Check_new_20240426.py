from collections import Counter
import csv
import data_analysis

filename = "./zip/kl8_20240425.csv"  # 替换为你的CSV文件名

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

searchNums = [8,9,10,13,14,15,16,17,18,21,35,38,45,50,52,58,64,71,72,75]
r=3
counter_searchNums = data_analysis.search_pairs2(df, searchNums,r)
# data_analysis.print_common_pairs(counter_searchNums)

data_analysis.print_common_pairs2(counter_searchNums,searchNums)