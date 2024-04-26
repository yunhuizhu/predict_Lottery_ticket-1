import csv

# 读取CSV文件
with open('./zip/sd_20240416.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# 跳过第一行，从第二行开始读取
data = data[1:]
columns = []
count1 = {}
count2 = {}
count3 = {}
for row in data:
    #按照逗号分割每一行的数据，分成3列
    #之后分别给每一列放到count
    count1[row[0]] = count1.get(row[0], 0) + 1
    count2[row[1]] = count2.get(row[1], 0) + 1
    count3[row[2]] = count3.get(row[2], 0) + 1

# 打印出现次数为1的数字
print("第一列出现次数为1的数字:")
for num, freq in count1.items():
    if freq == 1:
        print(num)
print("第二列出现次数为1的数字:")
for num, freq in count2.items():
    if freq == 1:
        print(num)
print("第三列出现次数为1的数字:")
for num, freq in count3.items():
    if freq == 1:
        print(num)

# 打印一次都没有出现的数字
print("第一列一次都没有出现的数字:")
for i in range(10):
    if str(i) not in count1:
        print(i)
print("第二列一次都没有出现的数字:")
for i in range(10):
    if str(i) not in count2:
        print(i)
print("第三列一次都没有出现的数字:")
for i in range(10):
    if str(i) not in count3:
        print(i)