from collections import Counter
# 假设你的数字组如下：
ck3 = [5,9,11,18,19,22,23,26,42,44,45,49,54,57,61,65,68,76,78,80]  # 请用实际数字替换
ck4 = [4,5,8,9,11,22,28,32,33,36,39,40,41,43,47,53,54,68,78,80]  # 请用实际数字替换
ck5 = [6,19,25,31,33,34,41,42,44,49,51,53,57,58,59,61,67,68,72,76]  # 请用实际数字替换
ck7 = [7,11,13,15,16,22,26,27,28,30,36,39,47,49,50,52,54,58,62,78]  # 请用实际数字替换
ck9 = [1,4,7,8,10,14,23,24,43,47,51,54,55,62,68,73,74,75,79,80]  # 请用实际数字替换
ck10 = [1,14,17,19,26,27,28,29,39,42,45,52,53,57,59,61,64,70,77,78]  # 请用实际数字替换
ck11 = [2,4,16,19,25,27,32,34,38,42,44,50,51,52,64,65,68,69,73,76]  # 请用实际数字替换
ck12 = [5,7,9,12,15,16,17,20,24,28,30,32,36,37,48,52,57,67,73,78]  # 请用实际数字替换
ck13 = [3,6,7,16,25,29,32,36,39,40,41,42,58,60,64,69,70,75,76,78]  # 请用实际数字替换
ck14 = [2,3,6,9,13,25,26,30,31,35,41,44,47,53,54,61,65,67,71,72]  # 请用实际数字替换
ck15 = [3,10,11,14,16,23,26,27,41,47,48,53,54,61,64,68,71,72,74,75]  # 请用实际数字替换
ck20 = [6,7,12,16,21,25,28,41,43,47,48,49,50,61,67,69,73,77,79,80]  # 请用实际数字替换
yl_fqn_1= [19, 53, 57, 44, 26, 48, 78, 18]
yl_fqn_2= [22, 49, 51, 52, 65, 2, 15, 16]
yl_fqn_3= [35, 59, 34, 37, 38, 39, 40, 47]
yl_fqn_4= [63, 70, 76, 3, 10, 17, 23, 25]
yl_fqn_5= [31, 74, 8, 9, 11, 13, 20, 30]
yl_fqn_6= [58, 60, 71, 77, 4, 7, 27, 28]
yl_fqn_7= [36, 42, 45, 46, 50, 61, 62, 64]
yl_fqn_8= [67, 72, 73, 80, 1, 5, 6, 12]
yl_fqn_9= [14, 21, 24, 29, 32, 33, 41, 43]
yl_fqn_10= [54, 55, 56, 66, 68, 69, 75, 79]
lh=[20,23,25,34,44,57,65,67,70,74,76,78]
re = [20,62,67,76]  # 请用实际数字替换
wen = [8,16,18,23,25,26,27,34,35,39,51,59,61,65,70,74]  # 请用实际数字替换
leng = [19,37,38,44,48,49,52,57,78]  # 请用实际数字替换
zx = [2,7,12,15,17,20,27,33,36,37,42,49,56,57,59,63,67,70,74,77]  # 请用实际数字替换
cj =[2,3,5,11,13,14,20,23,24,25,27,29,33,37,54,58,68,69,73,80]
ckMap = {'3':ck3,'4':ck4,'5':ck5,'7':ck7,'9':ck9,'10':ck10,'11':ck11,'12':ck12,'13':ck13,'14':ck14,'15':ck15,'20':ck20}
ylMap={'1':yl_fqn_1,'2':yl_fqn_2,'3':yl_fqn_3,'4':yl_fqn_4,'5':yl_fqn_5,'6':yl_fqn_6,'7':yl_fqn_7,'8':yl_fqn_8,'9':yl_fqn_9,'10':yl_fqn_10}
for i, value in enumerate(cj):
    keys = set()
    for key in ckMap:
        if value in ckMap[key]:
            keys.add("ck"+key)
    if keys:
        print(f"cj_{i+1}: {keys}")
cjMap = {}
for i in range(20):
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
     temp = set(numbers)&set(cj)
     if temp:
         print(f"cj_ckcommon{count}: {sorted(temp)}")
