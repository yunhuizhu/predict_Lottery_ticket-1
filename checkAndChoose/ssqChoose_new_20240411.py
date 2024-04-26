from collections import Counter
import csv
import os

# 假定的文件路径列表
file_paths = ["./zip/ssq_20240416.csv", "./zip/ssq_20240417.csv"]  # 示例文件路径

def process_file(file_path):
    ckRedMap = {}  # 存储红球数字
    ckBlueMap = {}  # 存储蓝球数字

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # 跳过标题行

        for line_number, row in enumerate(csv_reader, start=1):
            ckBlueMap[str(line_number)] = [int(row[-1])]  # 获取最后一个元素（蓝球）
            ckRedMap[str(line_number)] = list(map(int, row[:-1]))  # 获取前面的元素（红球）

    red_groups = []
    for numbers in ckRedMap.values():
        red_groups += numbers
    red_counter = Counter(red_groups)

    blue_groups = []
    for numbers in ckBlueMap.values():
        blue_groups += numbers
    blue_counter = Counter(blue_groups)

    # 计算红球和蓝球的杀号和非杀号
    red_shahao, red_feishahao = compute_shahao_red_feishahao(red_counter, 1, 33)
    blue_shahao, blue_feishahao = compute_shahao_blue_feishahao(blue_counter, 1, 16)

    return red_shahao, red_feishahao, blue_shahao, blue_feishahao

def compute_shahao_red_feishahao(counter, start, end):
    shahao = [number for number, count in counter.items() if count == 1]
    feishahao = [number for number, count in counter.items() if count >= 2]
    noNum = [i for i in range(start, end + 1) if i not in counter]
    #nonum放到shahao中
    shahao += noNum
    return shahao, feishahao

def compute_shahao_blue_feishahao(counter, start, end):
    shahao = [number for number, count in counter.items() if count > 1]
    feishahao = [number for number, count in counter.items() if count == 1]
    noNum = [i for i in range(start, end + 1) if i not in counter]
    #nonum放到feishahao中
    feishahao += noNum

    return shahao, feishahao

# 处理每个文件
results = [process_file(file_path) for file_path in file_paths]

# 计算每个文件的杀号和非杀号
final_red_shahao = set()
final_blue_shahao = set()

for index, (red_shahao, red_feishahao, blue_shahao, blue_feishahao) in enumerate(results):
    other_files_red_feishahao = set()
    other_files_blue_feishahao = set()

    for j, (other_red_shahao, other_red_feishahao, other_blue_shahao, other_blue_feishahao) in enumerate(results):
        if j != index:
            other_files_red_feishahao.update(other_red_feishahao)
            other_files_blue_feishahao.update(other_blue_feishahao)

    # 从当前文件的杀号中移除其他文件中存在的非杀号
    current_file_final_red_shahao = set(red_shahao) - other_files_red_feishahao
    current_file_final_blue_shahao = set(blue_shahao) - other_files_blue_feishahao

    # 更新最终的杀号
    final_red_shahao.update(current_file_final_red_shahao)
    final_blue_shahao.update(current_file_final_blue_shahao)

    print(f"File {file_paths[index]}: Red Shahao Removed: {set(red_shahao) - current_file_final_red_shahao}")
    print(f"File {file_paths[index]}: Red Shahao : {set(red_shahao)}")
    print(f"File {file_paths[index]}: Red feishahao : {set(red_feishahao)}")
    print(f"File {file_paths[index]}: Blue Shahao Removed: {set(blue_shahao) - current_file_final_blue_shahao}")
    print(f"File {file_paths[index]}: Blue Shahao : {set(blue_shahao) }")
    print(f"File {file_paths[index]}: Blue feishahao : {set(blue_feishahao)}")

# 打印最终合并的杀号
print("Final Combined Red Shahao:", list(final_red_shahao))
print("Final Combined Blue Shahao:", list(final_blue_shahao))