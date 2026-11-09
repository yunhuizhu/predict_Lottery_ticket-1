from collections import Counter
import csv
filename = "./zip/kl8_20231005.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
yl_fqn_1= [22, 51, 65, 16, 35, 38, 39, 40]
yl_fqn_2= [47, 10, 30, 71, 42, 45, 50, 64]
yl_fqn_3= [72, 32, 41, 43, 56, 66, 75, 2]
yl_fqn_4= [3, 5, 20, 37, 69, 73, 7, 8]
yl_fqn_5= [9, 17, 24, 25, 31, 34, 44, 46]
yl_fqn_6= [49, 52, 78, 1, 4, 6, 12, 15]
yl_fqn_7= [19, 26, 27, 48, 60, 62, 63, 67]
yl_fqn_8= [68, 76, 79, 80, 11, 13, 14, 18]
yl_fqn_9= [21, 23, 28, 29, 33, 36, 53, 54]
yl_fqn_10= [55, 57, 58, 59, 61, 70, 74, 77]
lh=[10,20,22,24,30,32,35,62,69,71,73,75,76]
re = [20,24,62,67,69,76]  # 请用实际数字替换
wen = [4,25,30,32,64,72,73]  # 请用实际数字替换
leng = [5,10,16,22,35,38,39,50,51,65,71,75]  # 请用实际数字替换
# zx = [4,12,16,20,21,30,32,35,40,47,54,55,56,62,66,69,70,72,76,79]  # 请用实际数字替换
cj =[1,5,9,11,14,15,16,32,34,39,42,43,45,52,63,67,69,70,76,78]
ylMap={'1':yl_fqn_1,'2':yl_fqn_2,'3':yl_fqn_3,'4':yl_fqn_4,'5':yl_fqn_5,'6':yl_fqn_6,'7':yl_fqn_7,'8':yl_fqn_8,'9':yl_fqn_9,'10':yl_fqn_10}
# 初始化结果字典
result = {}

# 遍历集合
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
# groups = []
# for count, numbers in ckMap.items():
#     # print("ck"+count, numbers)
#     groups+= numbers
# # 统计数字出现的次数
# counter = Counter(groups)
# # 创建一个空字典来存储出现次数相同的数字
# ckcommons = {}
# for number, count in counter.items():
#     if count not in ckcommons:
#         ckcommons[count] = [number]
#     else:
#         ckcommons[count].append(number)
# all_numbers = set(range(81)) # 创建一个包含0到80的集合
# # numbers_in_groups = set(ck3 + ck4 + ck5 + ck7+ck9+ck10+ck11+ck12+ck13+ck14+ck15+ck20) # 创建一个包含四组所有数字的集合
# numbers_in_groups =[] # 创建一个包含四组所有数字的集合
# for count, numbers in ckMap.items():
#     numbers_in_groups = numbers_in_groups+numbers
# noNum = all_numbers - set(numbers_in_groups)
# print("noNum ", noNum)
# ckMap['noNum']=noNum
# ckcommons[0]=noNum
# # 打印出现次数相同的数字
# for count, numbers in ckcommons.items():
#     if numbers:
#      print(f"ckcommon{count}: {sorted(numbers)}")
#      temp = set(numbers)&set(cj)
#      if temp:
#          print(f"cj_ckcommon{count}: {sorted(temp)}")
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
