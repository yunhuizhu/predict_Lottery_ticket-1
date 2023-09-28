from collections import Counter
# 假设你的数字组如下：
ck3 = [1,11,17,23,24,26,27,35,38,40,44,46,51,52,55,59,64,71,73,77]  # 请用实际数字替换
ck4 = [1,6,7,8,11,14,17,21,30,40,43,47,51,53,56,60,62,63,72,74]  # 请用实际数字替换
ck5 = [2,12,24,32,33,34,36,12,26,27,31,35,39,41,42,48,54,57,60,69]  # 请用实际数字替换
ck7 = [27,28,30,31,33,36,37,39,40,42,44,48,61,62,65,74,75,76,77,79]  # 请用实际数字替换
ck9 = [1,2,3,13,19,20,23,25,31,35,38,41,46,47,48,52,56,71,72,79]  # 请用实际数字替换
ck10 = [1,4,12,18,26,28,34,38,39,43,47,50,57,58,62,66,69,70,74,76]  # 请用实际数字替换
ck11 = [4,6,17,20,21,22,25,26,31,37,46,58,60,62,63,65,69,75,78,80]  # 请用实际数字替换
ck12 = [1,2,5,8,12,27,32,39,42,47,49,50,53,54,60,61,63,64,66,69]  # 请用实际数字替换
ck13 = [4,11,12,14,16,18,21,24,26,27,36,38,41,45,51,53,64,70,74,75]  # 请用实际数字替换
ck14 = [5,8,17,18,19,24,25,29,31,35,36,47,51,59,61,65,70,72,73,75]  # 请用实际数字替换
ck15 = [1,2,3,4,9,18,26,27,45,47,48,52,53,54,57,59,62,66,69,78]  # 请用实际数字替换
ck20 = [2,3,12,15,16,23,24,26,32,34,39,41,43,44,53,56,61,69,76,80]  # 请用实际数字替换
yl_fqn_1= [19, 53, 57, 44, 26, 48, 78, 18]
yl_fqn_2= [22, 49, 51, 52, 65, 15, 16, 35]
yl_fqn_3= [59, 34, 38, 39, 40, 47, 63, 70]
yl_fqn_4= [76, 10, 17, 31, 74, 8, 9, 30]
yl_fqn_5= [60, 71, 77, 4, 7, 28, 36, 42]
yl_fqn_6= [45, 46, 50, 61, 62, 64, 67, 72]
yl_fqn_7= [1, 6, 12, 21, 32, 41, 43, 55]
yl_fqn_8= [56, 66, 75, 79, 2, 3, 5, 11]
yl_fqn_9= [13, 14, 20, 23, 24, 25, 27, 29]
yl_fqn_10= [33, 37, 54, 58, 68, 69, 73, 80]
lh=[12,15,19,26,28,30,34,38,55,59,67,70,72,74]
re = [7,12,30,62,67,72]  # 请用实际数字替换
wen = [8,16,18,28,34,35,55,61,65,70,74,76]  # 请用实际数字替换
leng = [15,19,26,38,39,44,48,49,51,52,59,60,63,78]  # 请用实际数字替换
zx = [6,11,20,25,26,29,35,43,46,47,52,54,63,64,69,72,73,76]  # 请用实际数字替换
ckMap = {'3':ck3,'4':ck4,'5':ck5,'7':ck7,'9':ck9,'10':ck10,'11':ck11,'12':ck12,'13':ck13,'14':ck14,'15':ck15,'20':ck20}
ylMap={'1':yl_fqn_1,'2':yl_fqn_2,'3':yl_fqn_3,'4':yl_fqn_4,'5':yl_fqn_5,'6':yl_fqn_6,'7':yl_fqn_7,'8':yl_fqn_8,'9':yl_fqn_9,'10':yl_fqn_10}
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
# for i, value in enumerate(zx):
#     keys = set()
#     for key in ylMap:
#         if value in ylMap[key]:
#             keys.add("yl"+key)
#     if keys:
#         print(f"zx_{i+1}: {keys}:value:{value}")
for key in ylMap:
    keys = set()
    for i, value in enumerate(zx):
        if value in ylMap[key]:
            keys.add("yl" + key+":"+str(value))
    if keys:
        print(f"{keys}")
zx_lh=set(zx)&set(lh)
print(f"zx_lh:{zx_lh}")
zx_re=set(zx)&set(re)
print(f"zx_re:{zx_re}")
zx_wen=set(zx)&set(wen)
print(f"zx_wen:{zx_wen}")
zx_leng=set(zx)&set(leng)
print(f"zx_leng:{zx_leng}")

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
    if numbers:
     print(f"ckcommon{count}: {sorted(numbers)}")
     temp = set(numbers)&set(zx)
     if temp:
         print(f"zx_ckcommon{count}: {sorted(temp)}")
