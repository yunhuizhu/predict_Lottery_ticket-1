from collections import Counter
import csv
import data_analysis

filename = "./zip/kl8_20240426.csv"  # 替换为你的CSV文件名

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

cj = [3,11,19,23,25,26,27,31,41,45,46,50,54,57,59,62,65,66,74,75]  # 请用实际数字替换
# cj = [1,4,7,8,10,15,21,27,31,33,35,37,43,44,49,51,63,64,66,74]  # 请用实际数字替换
# checkMap=checkMap={1: {'3': 2}, 2: {'1': 1}, 3: {'3': 3, '4': 1}, 4: {'3': 4, '5': 5, '6': 6}, 5: {'1': 4, '6': 9}, 6: {'2': 8}, 7: {'5': 10}, 8: {'3': 9}, 9: {'5': 12}, 10: {'3': 11, '5': 14}, 12: {'3': 13}, 13: {'5': 16, '6': 16}, 14: {'3': 14, '4': 11}, 15: {'3': 17, '4': 14, '5': 19}, 16: {'1': 15, '6': 18}, 17: {'1': 16, '3': 18}, 18: {'2': 17}, 19: {'4': 19}}
# 初始化结果字典
result = {}

for count, numbers in ckMap.items():
    print("ck"+count, numbers)
# 查看对应数字有多少个，大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
groups = []
for count, numbers in ckMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
counter = Counter(groups)
# 从1到80，如果不在groups中，就放到noNum列表中
noNum = []
for i in range(1, 81):
    if i not in groups:
        noNum.append(i)
print("noNum:", noNum)
shahao =[]
xiaoyu3=[]
ckcommons = {}
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
#大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
for count, numbers in ckcommons.items():
    if count<3:
        xiaoyu3+= numbers
    if count > 4:
        #numbers是一个列表，里面是数字，sh是一个列表，里面是数字，把numbers放到sh中
        shahao+= numbers
        print("ckcommons > 4:", count, numbers)
    else:
        print("ckcommons <= 4:", count, numbers)
#遍历cj，使用数字作为key，数字跟数字的加减1的值的列表作为value，之后遍历ckcommons,如果数字在value中，且count小于4，就打印出来,并且打印出来ckcommons的count值
cjMap = {}
#小于3的数字，放到列表，之后去重打印
xuanze = []

for number in cj:
    cjMap[number] = [number-1, number+1,number]
for count, numbers in ckcommons.items():
    for number in numbers:
       for key, value in cjMap.items():
           if number in value and number not in shahao and count<3:
               print("cjMap:", number, value, count,key)
               xuanze.append(number);
#cjMap noNum中存在则打印出来
for key, value in cjMap.items():
    for number in noNum:
      if number in value:
        print("nonum:", number, value, key)

#xz去重打印
print("xuanze:", list(set(xuanze)))
print("nonum:", list(set(noNum)))
#打印顺序排序打印

print("shahao:", list(set(shahao)))
print("xiaoyu3:", list(set(xiaoyu3)))
#xy3跟xz的
print("xiaoyu3_xuanze:", list(set(xiaoyu3) & set(xuanze)))
df = data_analysis.read_and_clean_data(filename)
data_analysis.remove_and_count(df, shahao,4)
