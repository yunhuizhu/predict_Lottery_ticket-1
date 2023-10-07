from collections import Counter
import csv
filename = "./zip/gdfc36x7_20231006.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
cj =[1,10,11,22,29,31,35]
# 统计数字出现的次数
groups = []
for count, numbers in ckMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
counter = Counter(groups)
# 创建一个空字典来存储出现次数相同的数字
ckcommons = {}
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
all_numbers = set(range(1,37)) # 创建一个包含0到80的集合
# numbers_in_groups = set(ck3 + ck4 + ck5 + ck7+ck9+ck10+c
numbers_in_groups =[] # 创建一个包含四组所有数字的集合
for count, numbers in ckMap.items():
    numbers_in_groups = numbers_in_groups+numbers
noNum = sorted(list(all_numbers - set(numbers_in_groups)))
print("noNum ", noNum)
ckMap['noNum']=noNum
ckcommons[0]=noNum
# 打印出现次数相同的数字
for count, numbers in ckcommons.items():
    if numbers:
     print(f"ckcommon{count}: {sorted(numbers)}")
     temp = set(numbers)&set(cj)
     if temp:
         print(f"cj_ckcommon{count}: {sorted(temp)}")
# 初始化结果字典
result = {}

# 遍历数字列表
for i, number in enumerate(cj):
    # 遍历集合
    for set_id, set in ckMap.items():
        if number in set:
            position = set.index(number)
            if i not in result:
                result[i] = {}
            result[i][set_id] = position

# 打印结果

print(f"checkMap={result}")
cjMap = {}
for i in range(7):
    for ck_key, ck_value in ckMap.items():
        if i < len(ck_value):
            if i not in cjMap:
                cjMap[i] = {ck_value[i]: ["ck_"+ck_key]}
            else:
                if ck_value[i] in cjMap[i]:
                    cjMap[i][ck_value[i]].append("ck_"+ck_key)
                else:
                    cjMap[i][ck_value[i]] = ["ck_"+ck_key]
for  cjkey,cjvalue in cjMap.items():
    print(f"{cjkey}: {cjvalue}")
