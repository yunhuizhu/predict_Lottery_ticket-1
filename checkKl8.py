from collections import Counter
# 假设你的数字组如下：
ck3 = [1,8,28,29,33,38,40,41,43,45,47,48,54,61,63,69,71,74,75,78]  # 请用实际数字替换
ck4 = [1,6,10,14,19,22,23,37,43,46,48,51,52,54,57,59,71,74,75,78]  # 请用实际数字替换
ck5 = [15,16,17,62,68,6,19,27,29,36,43,51,53,54,60,63,64,67,70,74]  # 请用实际数字替换
ck7 = [3,4,5,7,11,13,14,23,25,27,41,48,49,54,57,58,71,75,77,79]  # 请用实际数字替换
ck9 = [1,4,5,21,24,31,32,34,38,40,47,48,51,55,56,57,58,62,63,69]  # 请用实际数字替换
ck10 = [30,37,38,46,49,10,16,17,32,35,41,46,48,55,58,60,62,68,73,74]  # 请用实际数字替换
ck11 = [1,2,13,14,16,20,24,25,32,35,39,41,45,47,51,54,59,71,72,73]  # 请用实际数字替换
ck12 = [1,2,6,10,17,20,31,37,38,40,41,44,48,54,55,56,64,71,73,75]  # 请用实际数字替换
ck13 = [6,19,20,24,30,32,43,44,46,51,52,54,56,63,64,65,68,70,71,76]  # 请用实际数字替换
ck14 = [1,2,3,12,15,21,24,25,30,31,36,37,45,59,61,65,67,70,71,76]  # 请用实际数字替换
ck15 = [3,5,14,17,20,21,25,26,34,38,41,46,48,49,50,51,63,65,72,74]  # 请用实际数字替换
ck20 = [1,3,12,22,25,28,31,34,35,37,38,40,41,44,49,50,61,73,74,76]  # 请用实际数字替换
re = [24,25,44,53,57,58,72]  # 请用实际数字替换
wen = [2,5,23,27,29,31,38,40,42,51,54,59,60,61,65,71,73,77,79]  # 请用实际数字替换
leng = [4,13,19,33,37,56]  # 请用实际数字替换
cj = [3,4,8,18,20,23,24,26,29,37,42,43,48,54,67,69,71,72,76,78]  # 请用实际数字替换
ckMap = {'3':ck3,'4':ck4,'5':ck5,'7':ck7,'9':ck9,'10':ck10,'11':ck11,'12':ck12,'13':ck13,'14':ck14,'15':ck15,'20':ck20}
groups = []
for count, numbers in ckMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
# print("ck3 ", ck3)
# print("ck4 ", ck4)
# print("ck5 ", ck5)
# print("ck7 ", ck7)
# print("ck9 ", ck9)
# print("ck10 ", ck10)
# print("ck11 ", ck11)
# print("ck12 ", ck12)
# print("ck13 ", ck13)
# print("ck14 ", ck14)
# print("ck15 ", ck15)
# print("ck20 ", ck20)
# 统计数字出现的次数
counter = Counter(groups)
# 创建一个空字典来存储出现次数相同的数字
ckcommons = {}
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
all_numbers = set(range(81)) # 创建一个包含0到80的集合
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
    print(f"ckcommon{count}: {numbers}")


for count, numbers in ckcommons.items():
    temp = set(numbers) & set(re)
    # print(f"re_ckcommons {count}:",temp)
    temp = set(numbers) & set(wen)
    # print(f"wen_ckcommons {count}:",temp)
    temp = set(numbers) & set(leng)
    # print(f"leng_ckcommons {count}:",temp)
ck_re_map={}
groups =[]
# print("re", re)
for key, value in ckMap.items():
    tempName = 'ck'+str(key) + '_re'
    tempSet = set(value)&set(re)
    ck_re_map[tempName]=tempSet
    groups=groups+list(tempSet)
    # print(f"{tempName}:",tempSet)
# ck3_re=set(ck3) & set(re)
# ck4_re=set(ck4) & set(re)
# ck5_re=set(ck5) & set(re)
# ck7_re=set(ck7) & set(re)
# ck9_re=set(ck9) & set(re)
# ck10_re=set(ck10) & set(re)
# ck11_re=set(ck11) & set(re)
# ck12_re=set(ck12) & set(re)
# ck13_re=set(ck13) & set(re)
# ck14_re=set(ck14) & set(re)
# ck15_re=set(ck15) & set(re)
# ck20_re=set(ck20) & set(re)
# noNum_re=set(noNum) & set(re)
# groups = groups+noNum_re
# print("re",re)
# print("ck3_re",ck3_re)
# print("ck4_re",ck4_re)
# print("ck5_re",ck5_re)
# print("ck7_re",ck7_re)
# print("ck9_re",ck9_re)
# print("ck10_re",ck10_re)
# print("ck11_re",ck11_re)
# print("ck12_re",ck12_re)
# print("ck13_re",ck13_re)
# print("ck14_re",ck14_re)
# print("ck15_re",ck15_re)
# print("ck20_re",ck20_re)
# print("noNum_re",noNum_re)
# groups = [ ck3_re,  ck4_re,ck5_re, ck7_re, ck9_re, ck10_re,  ck11_re, ck12_re, ck13_re, ck14_re, ck15_re,ck20_re,noNum_re]
# 统计数字出现的次数
counter = Counter(groups)
# 创建一个空字典来存储出现次数相同的数字
ck_recommons = {}
for number, count in counter.items():
    if count not in ck_recommons:
        ck_recommons[count] = [number]
    else:
        ck_recommons[count].append(number)
# 打印出现次数相同的数字
# for count, numbers in ck_recommons.items():
#      print(f"ck_recommon{count}: {numbers}")
ck_wen_map={}
groups =[]
# print("wen", wen)
for key, value in ckMap.items():
    tempName = 'ck'+str(key) + '_wen'
    tempSet = set(value)&set(wen)
    ck_wen_map[tempName]=tempSet
    groups=groups+list(tempSet)
    # print(f"{tempName}:",tempSet)
# ck3_wen=set(ck3) & set(wen)
# ck4_wen=set(ck4) & set(wen)
# ck5_wen=set(ck5) & set(wen)
# ck7_wen=set(ck7) & set(wen)
# ck9_wen=set(ck9) & set(wen)
# ck10_wen=set(ck10) & set(wen)
# ck11_wen=set(ck11) & set(wen)
# ck12_wen=set(ck10) & set(wen)
# ck10_wen=set(ck10) & set(wen)
# ck10_wen=set(ck10) & set(wen)
# ck20_wen=set(ck20) & set(wen)
# print("ck3_wen",ck3_wen)
# print("ck4_wen",ck4_wen)
# print("ck5_wen",ck5_wen)
# print("ck7_wen",ck7_wen)
# print("ck9_wen",ck9_wen)
# print("ck10_wen",ck10_wen)
# print("ck20_wen",ck20_wen)
# groups = [ ck3_wen,  ck4_wen,ck5_wen, ck7_wen, ck9_wen, ck10_wen, ck20_wen,noNum_wen]
# 统计数字出现的次数
counter = Counter(groups)
# 创建一个空字典来存储出现次数相同的数字
ck_wencommons = {}
for number, count in counter.items():
    if count not in ck_wencommons:
        ck_wencommons[count] = [number]
    else:
        ck_wencommons[count].append(number)
# 打印出现次数相同的数字
# for count, numbers in ck_wencommons.items():
    # print(f"ck_wencommon{count}: {numbers}")

ck_leng_map={}
groups =[]
# print("leng",leng)
for key, value in ckMap.items():
    tempName = 'ck'+str(key) + '_leng'
    tempSet = set(value)&set(leng)
    ck_leng_map[tempName]=tempSet
    groups=groups+list(tempSet)
    # print(f"{tempName}:",tempSet)
# ck3_leng=set(ck3) & set(leng)
# ck4_leng=set(ck4) & set(leng)
# ck5_leng=set(ck5) & set(leng)
# ck7_leng=set(ck7) & set(leng)
# ck9_leng=set(ck9) & set(leng)
# ck10_leng=set(ck10) & set(leng)
# ck20_leng=set(ck20) & set(leng)
# noNum_leng=set(noNum) & set(leng)
# print("leng",leng)
# print("ck3_leng",ck3_leng)
# print("ck4_leng",ck4_leng)
# print("ck5_leng",ck5_leng)
# print("ck7_leng",ck7_leng)
# print("ck9_leng",ck9_leng)
# print("ck10_leng",ck10_leng)
# print("ck20_leng",ck20_leng)
# print("noNum_leng",noNum_leng)
# groups = [ ck3_leng,  ck4_leng,ck5_leng, ck7_leng, ck9_leng, ck10_leng, ck20_leng,noNum_leng]
# 统计数字出现的次数
counter = Counter(groups)
# 创建一个空字典来存储出现次数相同的数字
ck_lengcommons = {}
for number, count in counter.items():
    if count not in ck_lengcommons:
        ck_lengcommons[count] = [number]
    else:
        ck_lengcommons[count].append(number)
# 打印出现次数相同的数字
# for count, numbers in ck_lengcommons.items():
    # print(f"ck_lengcommon{count}: {numbers}")
# cj_ck3 = set(cj) & set(ck3)
# cj_ck4 = set(cj) & set(ck4)
# cj_ck5 = set(cj) & set(ck5)
# cj_ck7 = set(cj) & set(ck7)
# cj_ck9 = set(cj) & set(ck9)
# cj_ck10 = set(cj) & set(ck10)
# cj_ck20 = set(cj) & set(ck20)
# cj_noNum = set(cj) & set(noNum)
# print("cj",cj)
# print("cj_ck3",cj_ck3)
# print("cj_ck4",cj_ck4)
# print("cj_ck5",cj_ck5)
# print("cj_ck7",cj_ck7)
# print("cj_ck9",cj_ck9)
# print("cj_ck10",cj_ck10)
# print("cj_ck20",cj_ck20)
# print("cj_noNum",cj_noNum)
# for count, numbers in ck_lengcommons.items():
#     temp = set(numbers) & set(cj)
#     print(f"cj_cklengcommons {count}:",temp)
# for count, numbers in ck_recommons.items():
#     temp = set(numbers) & set(cj)
#     print(f"cj_ckrecommons {count}:",temp)
# for count, numbers in ck_wencommons.items():
#     temp = set(numbers) & set(cj)
#     print(f"cj_ckwencommons {count}:",temp)
for count, numbers in ckcommons.items():
    temp = set(numbers) & set(cj)
    print(f"cj_ckcommoncommons {count}:",temp)
cj_wen = set(cj) & set(wen)
cj_re = set(cj) & set(re)
cj_leng = set(cj) & set(leng)
print("cj_wen",cj_wen)
print("cj_re",cj_re)
print("cj_leng",cj_leng)
# cj_ck_re_map={}
# for count, numbers in ck_re_map.items():
#     tempName = 'cj_' +count
#     tempSet = set(numbers) & set(cj)
#     cj_ck_re_map[tempName] = tempSet
#     print(f"{tempName}:", tempSet)
# cj_ck_wen_map={}
# for count, numbers in ck_wen_map.items():
#     tempName = 'cj_' +count
#     tempSet = set(numbers) & set(cj)
#     cj_ck_wen_map[tempName] = tempSet
#     print(f"{tempName}:", tempSet)
# cj_ck_leng_map={}
# for count, numbers in ck_leng_map.items():
#     tempName = 'cj_' +count
#     tempSet = set(numbers) & set(cj)
#     cj_ck_leng_map[tempName] = tempSet
#     print(f"{tempName}:", tempSet)

#
# cj_ck3_re = set(cj) & set(ck3_re)
# cj_ck4_re = set(cj) & set(ck4_re)
# cj_ck5_re = set(cj) & set(ck5_re)
# cj_ck7_re = set(cj) & set(ck7_re)
# cj_ck9_re = set(cj) & set(ck9_re)
# cj_ck10_re = set(cj) & set(ck10_re)
# cj_ck20_re = set(cj) & set(ck20_re)
# cj_noNum_re = set(cj) & set(noNum_re)
# print("cj_ck3_re",cj_ck3_re)
# print("cj_ck4_re",cj_ck4_re)
# print("cj_ck5_re",cj_ck5_re)
# print("cj_ck7_re",cj_ck7_re)
# print("cj_ck9_re",cj_ck9_re)
# print("cj_ck10_re",cj_ck10_re)
# print("cj_ck20_re",cj_ck20_re)
# print("cj_noNum_re",cj_noNum_re)
# cj_ck3_wen = set(cj) & set(ck3_wen)
# cj_ck4_wen = set(cj) & set(ck4_wen)
# cj_ck5_wen = set(cj) & set(ck5_wen)
# cj_ck7_wen = set(cj) & set(ck7_wen)
# cj_ck9_wen = set(cj) & set(ck9_wen)
# cj_ck10_wen = set(cj) & set(ck10_wen)
# cj_ck20_wen = set(cj) & set(ck20_wen)
# cj_noNum_wen = set(cj) & set(noNum_wen)
# print("cj_ck3_wen",cj_ck3_wen)
# print("cj_ck4_wen",cj_ck4_wen)
# print("cj_ck5_wen",cj_ck5_wen)
# print("cj_ck7_wen",cj_ck7_wen)
# print("cj_ck9_wen",cj_ck9_wen)
# print("cj_ck10_wen",cj_ck10_wen)
# print("cj_ck20_wen",cj_ck20_wen)
# print("cj_noNum_wen",cj_noNum_wen)
# cj_ck3_leng = set(cj) & set(ck3_leng)
# cj_ck4_leng = set(cj) & set(ck4_leng)
# cj_ck5_leng = set(cj) & set(ck5_leng)
# cj_ck7_leng = set(cj) & set(ck7_leng)
# cj_ck9_leng = set(cj) & set(ck9_leng)
# cj_ck10_leng = set(cj) & set(ck10_leng)
# cj_ck20_leng = set(cj) & set(ck20_leng)
# cj_noNum_leng = set(cj) & set(noNum_leng)
# print("cj_ck3_leng",cj_ck3_leng)
# print("cj_ck4_leng",cj_ck4_leng)
# print("cj_ck5_leng",cj_ck5_leng)
# print("cj_ck7_leng",cj_ck7_leng)
# print("cj_ck9_leng",cj_ck9_leng)
# print("cj_ck10_leng",cj_ck10_leng)
# print("cj_ck20_leng",cj_ck20_leng)
# print("cj_noNum_leng",cj_noNum_leng)

