from collections import Counter
import csv
filename = "./zip/kl8_20231126.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典

yl_fqn_1= [10, 30, 50, 64, 41, 56, 2, 37]
yl_fqn_2= [31, 46, 4, 12, 19, 27, 48, 60]
yl_fqn_3= [79, 18, 23, 28, 29, 57, 59, 77]
yl_fqn_4= [1, 43, 45, 52, 67, 11, 15, 35]
yl_fqn_5= [63, 66, 71, 7, 17, 32, 39, 44]
yl_fqn_6= [68, 70, 72, 75, 76, 78, 5, 14]
yl_fqn_7= [20, 22, 24, 33, 36, 38, 40, 49]
yl_fqn_8= [51, 54, 58, 62, 3, 6, 8, 9]
yl_fqn_9= [13, 16, 21, 25, 26, 34, 42, 47]
yl_fqn_10= [53, 55, 61, 65, 69, 73, 74, 80]
lh=[2,4,10,12,15,27,33,46,52,60,62,64,70,75,79]
re = [11,29,33,58,62,67]  # 请用实际数字替换
wen = [1,4,12,15,23,27,28,32,49,51,59,63,70,75,76,78,79]  # 请用实际数字替换
leng = [2,10,30,31,37,39,46,50,52,60,64]  # 请用实际数字替换
# zx = [2,8,12,13,19,22,25,31,38,40,42,44,48,52,65,68,71,72,77,78]  # 请用实际数字替换
# zx = [6,11,15,17,26,29,32,34,37,40,41,46,50,54,57,59,62,63,65,75,34,40,46,50,17,32,62,12,21,65]  # 请用实际数字替换
cj =[2,12,15,16,18,25,27,36,42,46,49,54,55,57,58,63,64,65,74,77]
ylMap={'1':yl_fqn_1,'2':yl_fqn_2,'3':yl_fqn_3,'4':yl_fqn_4,'5':yl_fqn_5,'6':yl_fqn_6,'7':yl_fqn_7,'8':yl_fqn_8,'9':yl_fqn_9,'10':yl_fqn_10}
# 初始化结果字典
result = {}

# 遍历集合
# 初始化结果字典
result = {}

# 遍历数字列表
for i, number in enumerate(cj):
    # 遍历集合
    for keyId, values in ckMap.items():
        if number in values:
            position = values.index(number)
            if i not in result:
                result[i] = {}
            result[i][keyId] = position


# 打印结果
print(f"checkMap={result}")
cjMap = {}
for i in range(21):
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
# for i, value in enumerate(cj):
#     keys = set()
#     for key in ckMap:
#         if value in ckMap[key]:
#             keys.add("ck"+key)
#     if keys:
#         print(f"cj_{i+1} : {value}: {keys}")
# cjMap = {}
# for i in range(20):
#     cjIndexValue=cj[i]
#     cj_ck_index_eq=[]
#     for ck_key, ck_value in ckMap.items():
#         if i < len(ck_value):
#             if ck_value[i]==cjIndexValue:
#                 cj_ck_index_eq.append("ck_"+ck_key)
#             if i not in cjMap:
#                 cjMap[i] = {ck_value[i]: ["ck_"+ck_key]}
#             else:
#                 if ck_value[i] in cjMap[i]:
#                     cjMap[i][ck_value[i]].append("ck_"+ck_key)
#                 else:
#                     cjMap[i][ck_value[i]] = ["ck_"+ck_key]
#     if cj_ck_index_eq:
#         print(f"cjindex_{i}:{cjIndexValue}:{cj_ck_index_eq}")
# for  cjkey,cjvalue in cjMap.items():
#     print(f"{cjkey}: {cjvalue}")
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
# all_numbers = set(range(81)) # 创建一个包含0到80的集合
# # numbers_in_groups = set(ck3 + ck4 + ck5 + ck7+ck9+ck10+ck11+ck12+ck13+ck14+ck15+ck20) # 创建一个包含四组所有数字的集合
# numbers_in_groups =[] # 创建一个包含四组所有数字的集合
# for count, numbers in ckMap.items():
#     numbers_in_groups = numbers_in_groups+numbers
# noNum = all_numbers - set(numbers_in_groups)
# print("noNum ", noNum)
# ckMap['noNum']=noNum
# ckcommons[0]=noNum
# 打印出现次数相同的数字
for count, numbers in ckcommons.items():
    if numbers:
     print(f"ckcommon{count}: {sorted(numbers)}")
     # temp = set(numbers) & set(cj)
     # if temp:
     #     print(f"cj_ckcommon{count}: {sorted(temp)}")

for count, numbers in ckcommons.items():
    if numbers:
     # print(f"ckcommon{count}: {sorted(numbers)}")
     temp = set(numbers) & set(cj)
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
