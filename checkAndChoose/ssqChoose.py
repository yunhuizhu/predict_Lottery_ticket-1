from collections import Counter

import csv
filename = "./zip/ssq_20240203.csv"  # 替换为你的CSV文件名

ckRedMap = {}  # 创建一个空字典来存储行号和列表的映射
ckBlueMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        ckBlueMap[str(line_number)] = [int(row[-1])]  # 获取最后一个元素
        ckRedMap[str(line_number)] = list(map(int, row[:-1]))
# 假设你的数字组如下：

for count, numbers in ckRedMap.items():
    print("ckRed"+count, numbers)
for count, numbers in ckBlueMap.items():
    print("ckBlue"+count, numbers)
remain_red = set(range(1, 34))
remain_blue = set(range(1, 17))
cjRedMap = {}
for i in range(6):
    for ck_key, ck_value in ckRedMap.items():
        if i < len(ck_value):
            if i not in cjRedMap:
                cjRedMap[i] = {ck_value[i]: ["ckRed_"+ck_key]}
            else:
                if ck_value[i] in cjRedMap[i]:
                    cjRedMap[i][ck_value[i]].append("ckRed_"+ck_key)
                else:
                    cjRedMap[i][ck_value[i]] = ["ckRed_"+ck_key]
for  cjkey,cjvalue in cjRedMap.items():
    print(f"{cjkey}: {cjvalue}")
# for count, numbers in ckRedMap.items():
#     remain_red = remain_red-set(numbers)
#     temp = set(numbers) & set(rxRed)
#     print("rx_ckRed"+count, temp)
# for count, numbers in ckBlueMap.items():
#     remain_blue = remain_blue-set(numbers)
#     temp = set(numbers) & set(rxBlue)
#     print("rx_ckBlue"+count, temp)
print("remain_red:",remain_red)
# temp = set(remain_red) & set(rxRed)
# print("rx_remain_red:",temp)
# print("remain_blue:",remain_blue)
# temp = set(remain_blue) & set(rxBlue)
# print("rx_remain_red:",temp)