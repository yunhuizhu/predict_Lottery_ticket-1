from collections import Counter
import csv

filename = "./zip/sd_20231010.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
checkMap={0: {'11': 0}, 2: {'13': 1}}
# 统计数字出现的次数
# groups = []
# for count, numbers in ckMap.items():
#     # print("ck"+count, numbers)
#     groups+= numbers
# counter = Counter(groups)
# # 创建一个空字典来存储出现次数相同的数字
# ckcommons = {}
# for number, count in counter.items():
#     if count not in ckcommons:
#         ckcommons[count] = [number]
#     else:
#         ckcommons[count].append(number)
# all_numbers = set(range(1,37))
# # numbers_in_groups = set(ck3 + ck4 + ck5 + ck7+ck9+ck10+ck11+ck12+ck13+ck14+ck15+ck20) # 创建一个包含四组所有数字的集合
# numbers_in_groups =[] # 创建一个包含四组所有数字的集合
# for count, numbers in ckMap.items():
#     numbers_in_groups = numbers_in_groups+numbers
# noNum = sorted(list(all_numbers - set(numbers_in_groups)))
# print("noNum ", noNum)
# ckMap['noNum']=noNum
# ckcommons[0]=noNum
# # 打印出现次数相同的数字
# for count, numbers in ckcommons.items():
#     if numbers:
#      print(f"ckcommon{count}: {sorted(numbers)}")
#      # temp = set(numbers)&set(zx)
#      # if temp:
#      #     print(f"zx_ckcommon{count}: {sorted(temp)}")
# 初始化结果字典
result = {}
# 遍历map
for key, value in checkMap.items():
    for set_id, position in value.items():
        # 从集合中获取对应位置的数字
        number = ckMap[set_id][position]
        if key not in result:
            result[key] = {}
        result[key][set_id] = number

# 打印结果
print(result)
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
cjMap = {}
for i in range(4):
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
    all_numbers = set(range(10))
    temp =[]
    for cjValueKey in cjvalue.keys():
        temp.append(cjValueKey)
    remain_number=all_numbers -set(temp)
    if remain_number:
        print(f"{cjkey}_remain: {remain_number}")

# for count, numbers in ckMap.items():
#     print("ck"+count, numbers)
    # groups+= numbers

