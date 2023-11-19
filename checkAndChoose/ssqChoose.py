from collections import Counter

import csv
filename = "./zip/ssq_20231110.csv"  # 替换为你的CSV文件名

ckRedMap = {}  # 创建一个空字典来存储行号和列表的映射
ckBlueMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        ckBlueMap[str(line_number)] = [int(row[-1])]  # 获取最后一个元素
        ckRedMap[str(line_number)] = list(map(int, row[:-1]))
# 假设你的数字组如下：
# ckRed3 = [8,21,22,25,28,32]  # 请用实际数字替换
# ckRed4 = [11,18,20,22,30,31]  # 请用实际数字替换
# ckRed5 = [1,7,15,27,30,31]  # 请用实际数字替换
# ckRed7 = [1,6,9,13,14,28]  # 请用实际数字替换
# ckRed9 = [1,3,6,14,27,28]  # 请用实际数字替换
# ckRed10 = [1,11,14,22,26,33]  # 请用实际数字替换
# ckRed11 = [1,7,9,11,13,20]  # 请用实际数字替换
# ckRed12 = [1,5,13,21,23,31]  # 请用实际数字替换
# ckRed13 = [3,12,23,24,29,33]  # 请用实际数字替换
# ckRed14 = [1,3,6,13,27,28]  # 请用实际数字替换
# ckRed15 = [9,14,31,3,16,18]  # 请用实际数字替换
# ckBlue3 = [10]  # 请用实际数字替换
# ckBlue4 = [7]  # 请用实际数字替换
# ckBlue5 = [2]  # 请用实际数字替换
# ckBlue7 = [1]  # 请用实际数字替换
# ckBlue9 = [10]  # 请用实际数字替换
# ckBlue10 = [10]  # 请用实际数字替换
# ckBlue11 = [8]  # 请用实际数字替换
# ckBlue12 = [14]  # 请用实际数字替换
# ckBlue13 = [9]  # 请用实际数字替换
# ckBlue14 = [4]  # 请用实际数字替换
# ckBlue15 = [1]  # 请用实际数字替换
rxRed=[4,10,21,26,29,31]
rxBlue=[8]
# ckRedMap = {'3':ckRed3,'4':ckRed4,'5':ckRed5,'7':ckRed7,'9':ckRed9,'10':ckRed10,'11':ckRed11,'12':ckRed12,'13':ckRed13,'14':ckRed14,'15':ckRed15}
# ckBlueMap = {'3':ckBlue3,'4':ckBlue4,'5':ckBlue5,'7':ckBlue7,'9':ckBlue9,'10':ckBlue10,'11':ckBlue11,'12':ckBlue12,'13':ckBlue13,'14':ckBlue14,'15':ckBlue15}

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
for count, numbers in ckRedMap.items():
    remain_red = remain_red-set(numbers)
    temp = set(numbers) & set(rxRed)
    print("rx_ckRed"+count, temp)
for count, numbers in ckBlueMap.items():
    remain_blue = remain_blue-set(numbers)
    temp = set(numbers) & set(rxBlue)
    print("rx_ckBlue"+count, temp)
print("remain_red:",remain_red)
temp = set(remain_red) & set(rxRed)
print("rx_remain_red:",temp)
print("remain_blue:",remain_blue)
temp = set(remain_blue) & set(rxBlue)
print("rx_remain_red:",temp)