from collections import Counter

import csv
filename = "./zip/ssq_20240424.csv"  # 替换为你的CSV文件名

ckRedMap = {}  # 创建一个空字典来存储行号和列表的映射
ckBlueMap = {}  # 创建一个空字典来存储行号和列表的映射

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        ckBlueMap[str(line_number)] = [int(row[-1])]  # 获取最后一个元素
        ckRedMap[str(line_number)] = list(map(int, row[:-1]))
# 假设你的数字组如下：
for count, numbers in ckRedMap.items():
    print("ck"+count, numbers)
# 查看对应数字有多少个，大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
groups = []
for count, numbers in ckRedMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
counter = Counter(groups)
# 从1到80，如果不在groups中，就放到noNum列表中
noNum = []
for i in range(1, 34):
    if i not in groups:
        noNum.append(i)
shahao =[]
feishahao=[]
ckcommons = {}
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
#大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
for count, numbers in ckcommons.items():
    if count==1:
        shahao += numbers
        print("red ckcommons ==1 :", count, numbers)
    if count >= 2:
        feishahao+= numbers
        #numbers是一个列表，里面是数字，sh是一个列表，里面是数字，把numbers放到sh中
        print("red ckcommons > 2:", count, numbers)

print("red noNum:", noNum)
print("red shahao:", list(set(shahao)))
print("red feishahao:", list(set(feishahao)))

# 查看对应数字有多少个，大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
groups = []
for count, numbers in ckBlueMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
counter = Counter(groups)

print("groups:", list(set(groups)))
# 从1到80，如果不在groups中，就放到noNum列表中
noNum = []
for i in range(1, 17):
    if i not in groups:
        noNum.append(i)
shahao =[]
feishahao=[]
ckcommons = {}
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
#大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
for count, numbers in ckcommons.items():
    if count<2:
        feishahao+= numbers
        print("blue ckcommons < 2:", count, numbers)
    if count >= 2:
        #numbers是一个列表，里面是数字，sh是一个列表，里面是数字，把numbers放到sh中
        shahao+= numbers
        print("blue ckcommons > 2:", count, numbers)
print("blue shahao:", list(set(shahao)))
print("blue feishahao:", list(set(feishahao)))
print("blue noNum:", noNum)
