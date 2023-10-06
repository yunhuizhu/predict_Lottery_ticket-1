from collections import Counter
import csv
filename = "/Users/zhuyunhui/PycharmProjects/predict_Lottery_ticket-1/checkAndChoose/zip/gdfc36x7_20231006.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        ckMap[str(line_number)] = list(map(int, row))
cj =[1,10,11,22,29,31,35]
for i, value in enumerate(cj):
    keys = set()
    for key in ckMap:
        if value in ckMap[key]:
            keys.add("ck"+key)
    if keys:
        print(f"cj_{i+1} : {value}: {keys}")
cjMap = {}
for i in range(7):
    cjIndexValue=cj[i]
    cj_ck_index_eq=[]
    for ck_key, ck_value in ckMap.items():
        if i < len(ck_value):
            if ck_value[i]==cjIndexValue:
                cj_ck_index_eq.append("ck_"+ck_key)
            if i not in cjMap:
                cjMap[i] = {ck_value[i]: ["ck_"+ck_key]}
            else:
                if ck_value[i] in cjMap[i]:
                    cjMap[i][ck_value[i]].append("ck_"+ck_key)
                else:
                    cjMap[i][ck_value[i]] = ["ck_"+ck_key]
    if cj_ck_index_eq:
        print(f"cjindex_{i}:{cjIndexValue}:{cj_ck_index_eq}")
for  cjkey,cjvalue in cjMap.items():
    print(f"{cjkey}: {cjvalue}")
groups = []
for count, numbers in ckMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
# 统计数字出现的次数
counter = Counter(groups)
# 创建一个空字典来存储出现次数相同的数字
ckcommons = {}
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
all_numbers = set(range(36)) # 创建一个包含0到80的集合
# numbers_in_groups = set(ck3 + ck4 + ck5 + ck7+ck9+ck10+ck11+ck12+ck13+ck14+ck15+ck20) # 创建一个包含四组所有数字的集合
numbers_in_groups =[] # 创建一个包含四组所有数字的集合
for count, numbers in ckMap.items():
    numbers_in_groups = numbers_in_groups+numbers
noNum = all_numbers - set(numbers_in_groups)
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
# for key in ylMap:
#     keys = set()
#     for i, value in enumerate(cj):
#         if value in ylMap[key]:
#             keys.add("yl" + key+":"+str(value))
#     if keys:
#         print(f"{keys}")
# cj_lh=set(cj)&set(lh)
# print(f"cj_lh:{cj_lh}")
# cj_re=set(cj)&set(re)
# print(f"cj_re:{cj_re}")
# cj_wen=set(cj)&set(wen)
# print(f"cj_wen:{cj_wen}")
# cj_leng=set(cj)&set(leng)
# print(f"cj_leng:{cj_leng}")
