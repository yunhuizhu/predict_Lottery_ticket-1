import csv
from collections import Counter
filename = "zip/sd_20261112_h.csv"  # 替换为你的CSV文件名
# 读取CSV文件esx
with open(filename, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
ckMap = {}  # 创建一个空字典来存储行号和列表的映射
with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）
    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
cj = [6,6,6]  # 请用实际数字替换
cj_flag=False
#2026270,3,6,7,8,9,16,21,22,23,27,39,40,41,44,48,54,60,65,68,75
#26116,10,19,24,27,28,33,12
# 当cj_flag为True时，对比原始文件每组与cj对应位置的一致性
if cj_flag:
    print("\n=== 原始文件数据与cj位置一致性对比 ===")
    # 重新读取原始文件数据（不排序）
    original_data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # 跳过标题行
        for row in csv_reader:
            original_data.append(row)
    
    # 对比原始数据与cj的位置一致性
    for index, row in enumerate(original_data, start=1):
        print(f"第{index}组原始数据: {row}")
        match_positions = []
        for i in range(min(len(row), len(cj))):
            if i < len(row) and i < len(cj):
                if int(row[i]) == cj[i]:
                    match_positions.append(i+1)  # 位置从1开始计数
        if match_positions:
            print(f"  与cj在第{match_positions}位数字一致")
        else:
            print(f"  与cj无位置数字一致")
# 跳过第一行，从第二行开始读取
data = data[1:]
count1 = {}
count2 = {}
count3 = {}
for row in data:
    #按照逗号分割每一行的数据，分成3列
    #之后分别给每一列放到count
    count1[row[0]] = count1.get(row[0], 0) + 1
    count2[row[1]] = count2.get(row[1], 0) + 1
    count3[row[2]] = count3.get(row[2], 0) + 1
#ckmap相邻交集并打印
ckjiaock_map = {}
jiaojiset=[]
jiaojish_map ={}
for count, numbers in ckMap.items():
    ckjiaock_count ={}
    comparecount = int(count)+1
    for count1_temp,numbers1 in ckMap.items():
        if comparecount==int(count1_temp):
         common_numbers = [num for num in numbers if num in numbers1]
         ckjiaock_count[count1_temp] =common_numbers
         for commonnum in common_numbers:
            if commonnum not in jiaojiset:
              jiaojiset.append(commonnum)
         print(f"ck{count} 和 ck{count1_temp} 的交集有 {len(common_numbers)} 个值，分别是：{common_numbers}")
         if cj_flag:
             cj_jiaoji = [num for num in cj if num in common_numbers]
             print(f"ck{count} 和 ck{count1_temp} 的交集跟cj 的交集有 {len(cj_jiaoji)} 个 cj 的值，分别是：{cj_jiaoji}")
         # 处理当前 count 对应的项
         current_key = int(count)
         if current_key not in jiaojish_map:
             jiaojish_map[current_key] = list(common_numbers)
         else:
             jiaojish_map[current_key].extend(common_numbers)
         # 处理 comparecount 对应的项
         if comparecount not in jiaojish_map:
             jiaojish_map[comparecount] = list(common_numbers)  # 初始化为 common_numbers 的副本
         else:
             jiaojish_map[comparecount].extend(common_numbers)  # 使用 extend 追加每个数字

    ckjiaock_map[count]=ckjiaock_count
# 动态打印各列中不同出现次数的数字
print("第一列数字出现次数统计:")
frequency_dict_1 = {}
for num, freq in count1.items():
    if freq not in frequency_dict_1:
        frequency_dict_1[freq] = []
    frequency_dict_1[freq].append(num)

# 按出现次数排序输出
for freq in sorted(frequency_dict_1.keys()):
    print(f"出现{freq}次的数字: {sorted(frequency_dict_1[freq])}")

print("\n第二列数字出现次数统计:")
frequency_dict_2 = {}
for num, freq in count2.items():
    if freq not in frequency_dict_2:
        frequency_dict_2[freq] = []
    frequency_dict_2[freq].append(num)

# 按出现次数排序输出
for freq in sorted(frequency_dict_2.keys()):
    print(f"出现{freq}次的数字: {sorted(frequency_dict_2[freq])}")

print("\n第三列数字出现次数统计:")
frequency_dict_3 = {}
for num, freq in count3.items():
    if freq not in frequency_dict_3:
        frequency_dict_3[freq] = []
    frequency_dict_3[freq].append(num)

# 按出现次数排序输出
for freq in sorted(frequency_dict_3.keys()):
    print(f"出现{freq}次的数字: {sorted(frequency_dict_3[freq])}")
# 打印一次都没有出现的数字

columns = []
for i in range(10):
    if str(i) not in count1:
        columns.append(i)

print("第一列一次都没有出现的数字:",columns)

columns = []
for i in range(10):
    if str(i) not in count2:
        columns.append(i)
print("第二列一次都没有出现的数字:",columns)

columns = []
for i in range(10):
    if str(i) not in count3:
        columns.append(i)

print("第三列一次都没有出现的数字:",columns)
# 计算每行三个数最大跟最小值相减的绝对值并放到列表
abs_values = []
xiao_values=[]
same_values=[]
for row in data:
    nums = [int(row[0]), int(row[1]), int(row[2])]
    max_num = max(nums)
    min_num = min(nums)
    abs_values.append(abs(max_num - min_num))
    abs_value = float('inf')
    same_value=-1
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            abs_value2 = abs(int(nums[i]) - int(nums[j]))
            if abs_value2 == 0:
                same_values.append(int(nums[i]))
            if abs_value2 < abs_value:
                abs_value = abs_value2
    xiao_values.append(abs_value)

ckkd_map = {}
ckxiaokua_map = {}
ckoushu_map={}
for row in data:
    nums = [int(num) for num in row]  # 将行中的字符串转换为整数
    #nums数组里面的数字两两相减绝对值最小的放入ckxiaokua_map
    abs_value  = float('inf')
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            abs_value2 = abs(int(nums[i]) - int(nums[j]))
            if abs_value2 < abs_value:
                abs_value = abs_value2
    ckxiaokua_map[tuple(row)] = abs_value
    max_num = max(nums)
    min_num = min(nums)
    ckkd_map[tuple(row)] = max_num - min_num  # 使用元组作为键
    ckoushu_map[tuple(row)] = len([num for num in nums if num % 2 == 0])  # 使用元组作为键

#统计ckkd_map里面的value值的数量
print("ckkd_map:", ckkd_map)
ckkd_map_counter = Counter(v for v in ckkd_map.values())
print("ckkd_map_counter:", ckkd_map_counter)

print("ckoushu_map:", ckoushu_map)
ckoushu_map_counter = Counter(v for v in ckoushu_map.values())
print("ckoushu_map_counter:", ckoushu_map_counter)
# 对绝对值列表去重
print("每行三个数最大跟最小值相减的绝对值列表最大跨度：", abs_values)
print("每行三个数最小间隔的绝对值列表最小跨度：", xiao_values)
# 打印出same_values 数字并数量。3:2这样
same_value_counts = Counter(same_values)
print("相同数字和数量：", same_value_counts)
# 计算绝对值出现次数
abs_value_counts = {}
for abs_value in abs_values:
    abs_value_counts[abs_value] = abs_value_counts.get(abs_value, 0) + 1

# 对绝对值出现次数进行降序排序
sorted_abs_value_counts = sorted(abs_value_counts.items(), key=lambda item: item[1], reverse=True)
print("最大跨度绝对值出现次数（降序排序）：", sorted_abs_value_counts)

# 打印每个最大跨度值对应的具体数值对
print("\n=== 最大跨度值对应的数值对 ===")
for kuadu, count in sorted_abs_value_counts:
    value_pairs = []
    for combination, abs_val in zip(data, abs_values):
        if abs_val == kuadu:
            nums = [int(x) for x in combination]
            max_num = max(nums)
            min_num = min(nums)
            # 修改格式为(xy)而不是(x,y)
            value_pairs.append(f"({min_num}{max_num})")
    print(f"{kuadu}:{value_pairs}")
unique_abs_values = list(set(abs_values))
# 计算绝对值出现次数
xiao_value_counts = {}
for abs_value in xiao_values:
    xiao_value_counts[abs_value] = xiao_value_counts.get(abs_value, 0) + 1

# 对绝对值出现次数进行降序排序
sorted_xiao_value_counts = sorted(xiao_value_counts.items(), key=lambda item: item[1], reverse=True)
print("最小跨度绝对值出现次数（降序排序）：", sorted_xiao_value_counts)

# 打印每个最小跨度值对应的具体数值对
print("\n=== 最小跨度值对应的数值对 ===")
for kuadu, count in sorted_xiao_value_counts:
    value_pairs = []
    for combination, xiao_val in zip(data, xiao_values):
        if xiao_val == kuadu:
            nums = [int(x) for x in combination]
            # 找到最小差值对应的两个数
            min_diff = float('inf')
            pair_str = ""
            for i in range(len(nums)):
                for j in range(i + 1, len(nums)):
                    diff = abs(nums[i] - nums[j])
                    if diff == kuadu and diff < min_diff:
                        min_diff = diff
                        min_num = min(nums[i], nums[j])
                        max_num = max(nums[i], nums[j])
                        # 修改格式为(xy)而不是(x,y)
                        pair_str = f"({min_num}{max_num})"
            if pair_str:
                value_pairs.append(pair_str)
    # 去重
    value_pairs = list(set(value_pairs))
    print(f"{kuadu}:{value_pairs}")
# unique_abs_values = list(set(abs_values))
# print("每行三个数最大跟最小值相减的绝对值去重后列表：", unique_abs_values)

# 计算每行三个数相加的和值并放到列表
sum_values = []
for row in data:
    nums = [int(row[0]), int(row[1]), int(row[2])]
    sum_num = sum(nums)
    sum_values.append(sum_num)

# 对和值列表去重
print("每行三个数相加的和值列表：", sum_values)
# 计算和值出现次数
sum_value_counts = {}
for sum_value in sum_values:
    sum_value_counts[sum_value] = sum_value_counts.get(sum_value, 0) + 1

# 对和值出现次数进行降序排序
sorted_sum_value_counts = sorted(sum_value_counts.items(), key=lambda item: item[1], reverse=True)
print("和值出现次数（降序排序）：", sorted_sum_value_counts)
unique_sum_values = list(set(sum_values))
print("每行三个数相加的和值去重后列表：", unique_sum_values)
# 计算所有数字出现的次数
all_numbers = [int(item) for row in data for item in row]
all_counts = {}
for num in all_numbers:
    all_counts[num] = all_counts.get(num, 0) + 1
# 对所有数字出现的次数进行降序排序
sorted_counts = sorted(all_counts.items(), key=lambda item: item[1], reverse=True)

print("所有数字出现的次数（降序排序）：", sorted_counts)
# 找出 0 到 9 中未出现过的数字
missing_numbers = []
for i in range(10):
    found = False
    for num, freq in all_counts.items():
        if num == i:
            found = True
            break
    if not found:
        missing_numbers.append(i)

print("0 到 9 中未出现过的数字：", missing_numbers)
# 查询每行两个数字结合后的数字的出现次数（不区分顺序，保留前导零）
combined_counts = {}

for row in data:
    # 获取每行的数字组合（不区分顺序，保留前导零）
    combined_numbers = ["".join(sorted([row[i], row[j]])) for i in range(len(row)) for j in range(i + 1, len(row))]
    for number in combined_numbers:
        combined_counts[number] = combined_counts.get(number, 0) + 1

# 对组合出现次数进行降序排序
sorted_combined_counts = sorted(combined_counts.items(), key=lambda item: item[1], reverse=True)

print("每行两个数字结合后的数字出现次数（不区分顺序，保留前导零，降序排序）：", sorted_combined_counts)
# 生成0-9的数字数组
all_numbers = list(range(10))

# 遍历每个元组
for key, count in sorted_combined_counts:
    # 提取两个数字
    num1, num2 = int(key[0]), int(key[1])

    # 找出所有包含其中一个数字的其他数字
    related_numbers = set()
    for other_key, _ in sorted_combined_counts:
        if other_key != key:
            if key[0] in other_key:
                related_numbers.add(int(other_key.replace(key[0], '', 1)))
            if key[1] in other_key:
                related_numbers.add(int(other_key.replace(key[1], '', 1)))

    # 从0-9的数字数组中减去这个数组和元组的两个数字
    result = [num for num in all_numbers if num not in related_numbers and num not in (num1, num2)]

    # 打印结果
    print(f"Key: {key}, Result: {result}")
# 生成所有 0 到 9 的两两结合（不区分顺序）
all_combinations = set(["".join(sorted([str(i), str(j)])) for i in range(10) for j in range(i + 1, 10)])

# 获取数据中出现的两两结合
data_combinations = set()
for row in data:
    # 提取每行的数字组合（不区分顺序）
    combined_numbers = ["".join(sorted([row[i], row[j]])) for i in range(len(row)) for j in range(i + 1, len(row))]
    data_combinations.update(combined_numbers)

# 查找未出现在数据中的组合
missing_combinations = all_combinations - data_combinations

# 打印结果
print("0 到 9 的两两结合中，未出现在数据中的组合：", sorted(missing_combinations))
# Step 1: 生成所有 0 到 9 的两两结合（不区分顺序）
all_combinations = set(["".join(sorted([str(i), str(j)])) for i in range(10) for j in range(i + 1, 10)])

# 提取数据中出现的两两结合
data_combinations = set()
for row in data:
    # 提取每行的数字组合（不区分顺序）
    combined_numbers = ["".join(sorted([row[i], row[j]])) for i in range(len(row)) for j in range(i + 1, len(row))]
    data_combinations.update(combined_numbers)

# Step 2: 查找未出现在数据中的两两结合
missing_combinations = all_combinations - data_combinations

# Step 3: 将未出现在数据中的组合两两合在一起生成3个数字组合
missing_combinations_list = list(missing_combinations)
three_digit_combinations = set()
for i in range(len(missing_combinations_list)):
    for j in range(i + 1, len(missing_combinations_list)):
        # 合并两组两两组合，确保结果是3个不同的数字
        merged = set(missing_combinations_list[i] + missing_combinations_list[j])
        if len(merged) == 3:  # 必须是3个不同的数字
            three_digit_combinations.add("".join(sorted(merged)))

# Step 4: 拆分三数字组合为两个数字组合，并检查是否都不在数据中
not_in_data = []  # 两个数字组合都不在数据中的三数字组合
in_data = []  # 至少一个数字组合已存在的数据中的三数字组合
details = []  # 存储每个三数字组合的拆分详情

for three_digits in three_digit_combinations:
    # 拆分成两个数字组合
    digits = list(three_digits)
    pair1 = "".join(sorted([digits[0], digits[1]]))
    pair2 = "".join(sorted([digits[0], digits[2]]))
    pair3 = "".join(sorted([digits[1], digits[2]]))

    # 检查是否都不在原始数据中
    if pair1 not in data_combinations and pair2 not in data_combinations and pair3 not in data_combinations:
        not_in_data.append(three_digits)
    else:
        in_data.append(three_digits)
        details.append({
            "three_digits": three_digits,
            "pairs": [pair1, pair2, pair3],
            "existing_pairs": [pair for pair in [pair1, pair2, pair3] if pair in data_combinations],
            "missing_pairs": [pair for pair in [pair1, pair2, pair3] if pair not in data_combinations]
        })
data_combinations_list = list(data_combinations)
combined_indata = []
for i in range(len(data_combinations_list)):
    for j in range(i + 1, len(data_combinations_list)):
        # 合并两组两两组合，确保结果是3个不同的数字
        merged = set(data_combinations_list[i] + data_combinations_list[j])
        if len(merged) == 3:  # 必须是3个不同的数字
            combined_indata.append("".join(sorted(merged)))
combined_indata = list(set(combined_indata))
# 打印结果
print("未出现在数据中的两两组合：", sorted(missing_combinations))
print("由未出现在数据中的两两组合生成的三数字组合：", sorted(three_digit_combinations))
print("两个数字组合都不在数据中的三数字组合：", sorted(not_in_data))
print("至少一个数字组合在数据中的三数字组合：", sorted(in_data))
#对应两个数字都在在not_in_data跟in_data的打印出来
xuanze = [0]  # 假设要检查的两个数字组合是4和7
not_in_data_xuanze = []
for i in range(len(not_in_data)):
    # if xuanze[0] in not_in_data[i] and xuanze[1] in not_in_data[i]:
    # if str(xuanze[0]) in not_in_data[i] and str(xuanze[1]) in not_in_data[i]:
    if str(xuanze[0]) in not_in_data[i] :
        not_in_data_xuanze.append(not_in_data[i])
in_data_xuanze = []
for i in range(len(in_data)):
    # if xuanze[0] in in_data[i] and xuanze[1] in in_data[i]:
    # if str(xuanze[0]) in in_data[i] and str(xuanze[1]) in in_data[i]:
    if str(xuanze[0]) in in_data[i] :
        in_data_xuanze.append(in_data[i])
combined_in_data_xuanze = []
for i in range(len(combined_indata)):
    # if xuanze[0] in in_data[i] and xuanze[1] in in_data[i]:
    # if str(xuanze[0]) in in_data[i] and str(xuanze[1]) in in_data[i]:
    if str(xuanze[0]) in combined_indata[i] :
        combined_in_data_xuanze.append(combined_indata[i])
print("两个数字组合都在not_in_data中的三数字组合：", sorted(not_in_data_xuanze))
print("两个数字组合都在in_data中的三数字组合：", sorted(in_data_xuanze))
print("两个数字组合都在combined_indata中的三数字组合：", sorted(combined_in_data_xuanze))
print("三数字组合拆分详情：")
# for detail in details:
#     print(f"三数字组合: {detail['three_digits']}")
#     print(f"两个数字组合: {detail['pairs']}")
#     print(f"存在的数据组合: {detail['existing_pairs']}")
#     print(f"缺失的数据组合: {detail['missing_pairs']}")
#     print("---")





