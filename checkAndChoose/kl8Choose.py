from collections import Counter
import csv

filename = "./zip/kl8_20231007.csv"  # 替换为你的CSV文件名

ckMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
# 假设你的数字组如下：
# ck3 = [5,6,24,25,26,31,33,34,37,41,43,45,47,54,56,62,64,67,74,80]  # 请用实际数字替换
# ck4 = [3,9,10,12,16,17,19,25,27,30,36,44,48,53,55,58,61,68,74,78]  # 请用实际数字替换
# ck5 = [1,8,21,23,25,28,29,31,44,45,54,56,57,58,62,64,68,73,76,79]  # 请用实际数字替换
# ck7 = [27,28,30,31,33,36,37,39,40,42,44,48,61,62,65,74,75,76,77,79]  # 请用实际数字替换
# ck9 = [1,2,3,13,19,20,23,25,31,35,38,41,46,47,48,52,56,71,72,79]  # 请用实际数字替换
# ck10 = [1,4,12,18,26,28,34,38,39,43,47,50,57,58,62,66,69,70,74,76]  # 请用实际数字替换
# ck11 = [4,6,17,20,21,22,25,26,31,37,46,58,60,62,63,65,69,75,78,80]  # 请用实际数字替换
# ck12 = [1,2,5,8,12,27,32,39,42,47,49,50,53,54,60,61,63,64,66,69]  # 请用实际数字替换
# ck13 = [4,11,12,14,16,18,21,24,26,27,36,38,41,45,51,53,64,70,74,75]  # 请用实际数字替换
# ck14 = [5,8,17,18,19,24,25,29,31,35,36,47,51,59,61,65,70,72,73,75]  # 请用实际数字替换
# ck15 = [1,2,3,4,9,18,26,27,45,47,48,52,53,54,57,59,62,66,69,78]  # 请用实际数字替换
# ck20 = [2,3,12,15,16,23,24,26,32,34,39,41,43,44,53,56,61,69,76,80]  # 请用实际数字替换
yl_fqn_1= [22, 65, 38, 47, 10, 30, 50, 64]
yl_fqn_2= [72, 41, 56, 2, 3, 20, 37, 73]
yl_fqn_3= [7, 8, 17, 24, 25, 31, 44, 46]
yl_fqn_4= [4, 6, 12, 19, 26, 27, 48, 60]
yl_fqn_5= [68, 79, 18, 23, 28, 29, 53, 54]
yl_fqn_6= [55, 57, 58, 59, 74, 77, 1, 5]
yl_fqn_7= [9, 14, 32, 34, 39, 42, 43, 45]
yl_fqn_8= [52, 67, 69, 76, 11, 13, 15, 16]
yl_fqn_9= [21, 33, 35, 36, 40, 49, 51, 61]
yl_fqn_10= [62, 63, 66, 70, 71, 75, 78, 80]
lh=[4,8,12,35,38,46,51,62,64,68,71,75]
re = [20,24,27,54,62,68]  # 请用实际数字替换
wen = [3,4,7,8,12,25,30,59,72,73,80]  # 请用实际数字替换
leng = [22,35,38,46,50,51,64,65,71,75]  # 请用实际数字替换
# zx = [2,8,12,13,19,22,25,31,38,40,42,44,48,52,65,68,71,72,77,78]  # 请用实际数字替换
zx = [1,6,14,18,22,26,31,35,40,53,56,61]  # 请用实际数字替换
# ckMap = {'3':ck3,'4':ck4,'5':ck5,'7':ck7,'9':ck9,'10':ck10,'11':ck11,'12':ck12,'13':ck13,'14':ck14,'15':ck15,'20':ck20}
ylMap={'1':yl_fqn_1,'2':yl_fqn_2,'3':yl_fqn_3,'4':yl_fqn_4,'5':yl_fqn_5,'6':yl_fqn_6,'7':yl_fqn_7,'8':yl_fqn_8,'9':yl_fqn_9,'10':yl_fqn_10}
checkMap={0: {'8': 0, '9': 0, '10': 0}, 1: {'5': 2, '11': 1}, 2: {'3': 3, '4': 2, '11': 3}, 3: {'11': 4}, 4: {'1': 2, '9': 3, '10': 4, '12': 0}, 5: {'1': 3, '8': 4, '11': 5, '12': 1}, 6: {'1': 4, '3': 5, '4': 4, '7': 1}, 7: {'1': 8, '7': 8, '12': 8}, 8: {'6': 7, '7': 9, '12': 9}, 9: {'1': 10, '2': 9, '3': 12, '6': 8, '12': 12}, 10: {'4': 11, '10': 6}, 11: {'3': 14, '4': 12, '5': 9, '6': 9, '11': 13}, 12: {'10': 7}, 13: {'2': 11, '3': 15, '8': 9, '12': 15}, 14: {'2': 13, '4': 15, '6': 13, '7': 14, '8': 14, '11': 16}, 15: {'1': 19, '2': 15, '6': 15, '9': 15}, 16: {'2': 16, '5': 15, '8': 16}, 17: {'5': 16, '8': 17, '10': 16}, 18: {'6': 18, '7': 17, '11': 18}, 19: {'10': 19}}
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
# cjMap = {}
# for i in range(20):
#     for ck_key, ck_value in ckMap.items():
#         if i < len(ck_value):
#             if i not in cjMap:
#                 cjMap[i] = {ck_value[i]: ["ck_"+ck_key]}
#             else:
#                 if ck_value[i] in cjMap[i]:
#                     cjMap[i][ck_value[i]].append("ck_"+ck_key)
#                 else:
#                     cjMap[i][ck_value[i]] = ["ck_"+ck_key]
# for  cjkey,cjvalue in cjMap.items():
#     print(f"{cjkey}: {cjvalue}")
# # for i, value in enumerate(zx):
# #     keys = set()
# #     for key in ylMap:
# #         if value in ylMap[key]:
# #             keys.add("yl"+key)
# #     if keys:
# #         print(f"zx_{i+1}: {keys}:value:{value}")
for key in ylMap:
    keys = set()
    for i, value in enumerate(zx):
        if value in ylMap[key]:
            keys.add("yl" + key+":"+str(value))
    if keys:
        print(f"{keys}")
# zx_lh=set(zx)&set(lh)
# print(f"zx_lh:{zx_lh}")
# zx_re=set(zx)&set(re)
# print(f"zx_re:{zx_re}")
# zx_wen=set(zx)&set(wen)
# print(f"zx_wen:{zx_wen}")
# zx_leng=set(zx)&set(leng)
# print(f"zx_leng:{zx_leng}")
#
# # 统计数字出现的次数
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
#      temp = set(numbers)&set(zx)
#      if temp:
#          print(f"zx_ckcommon{count}: {sorted(temp)}")
# zxMap = {}
# for i in range(20):
#     zxIndexValue=zx[i]
#     zx_ck_index_eq=[]
#     for ck_key, ck_value in ckMap.items():
#         ck_value = list(ck_value)
#         if i < len(ck_value):
#             if ck_value[i] == zxIndexValue:
#                 zx_ck_index_eq.append("ck_"+ck_key)
#             if i not in zxMap:
#                 zxMap[i] = {ck_value[i]: ["ck_"+ck_key]}
#             else:
#                 if ck_value[i] in zxMap[i]:
#                     zxMap[i][ck_value[i]].append("ck_"+ck_key)
#                 else:
#                     zxMap[i][ck_value[i]] = ["ck_"+ck_key]
#     if zx_ck_index_eq:
#         print(f"zxindex_{i}:{zxIndexValue}:{zx_ck_index_eq}")
# for  cjkey,cjvalue in zxMap.items():
#     print(f"{cjkey}: {cjvalue}")
