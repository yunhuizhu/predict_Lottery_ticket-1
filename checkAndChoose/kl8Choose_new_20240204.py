from collections import Counter
import csv
import data_analysis

filename = "zip/kl8_20261112_1.csv"  # 替换为你的CSV文件名

cj = [3,11,16,26,27,29,35,37,44,47,48,52,53,56,58,61,67,69,70,75]  # 请用实际数字替换
# cj = [3,6,13,14,17,19,23,28,34,38,41,43,47,55,58,62,70,73,74,80]  # 请用实际数字替换
cj_pre = [8,13,14,17,22,23,33,34,35,36,47,49,51,54,60,63,68,69,75,79]
cj_flag= True
ckMap = {}  # 创建一个空字典来存储行号和列表的映射
# 创建位置统计字典，用于统计每个位置上的数字出现次数
position_stats = {i: {} for i in range(20)}  # 假设最多20个位置
prepartions =["1-10", "11-20", "21-30", "31-40"]
# prepartions =["41-50", "51-60", "61-70", "71-80"]
maxsum = 11
minsum = 9
minbjcount=2
maxbjcount=3
with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）
    for line_number, row in enumerate(csv_reader, start=1):
        sorted_row = sorted(list(map(int, row)))  # 对每一行的数据进行排序
        ckMap[str(line_number)] = sorted_row  # 将排序后的数据存入字典
        
        # 统计每个位置上的数字出现次数
        for position, number in enumerate(sorted_row):
            if number not in position_stats[position]:
                position_stats[position][number] = 0
            position_stats[position][number] += 1
zx_sh=[]
sh2=[]
#遍历ckmap,打印出ckmap中每行的跨度（最大数跟最小数之差）并放到数组并打印出来，每行的偶数个数并放到数组，并打印出来
ckkd_map = {}
ckoushu_map={}
cksum_map={}
# 查找cj中同时在cj_pre中的数字
cj_in_cj_pre = [num for num in cj if num in cj_pre]
print("cj中同时在cj_pre中的数字:", cj_in_cj_pre)

# 查找对望码
mirror_codes = []
mirror_count = 0
# print("\n对望码:")
for num in cj:
    mirror = data_analysis.get_mirror_number(num)
    if mirror and mirror in cj_pre:
        mirror_codes.append((num, mirror))
        mirror_count += 1
        # print(f"{num} <-> {mirror}")

print(f"对望码数量: {mirror_count}  对望码：", mirror_codes)
# print("对望码：",mirror_codes)

# 查找邻码
adjacent_codes = []
adjacent_count = 0
# print("\n邻码:")
for num in cj:
    adjacents = data_analysis.get_adjacent_numbersByNum(num)
    for adj in adjacents:
        if adj in cj_pre:
            adjacent_codes.append((num, adj))
            adjacent_count += 1
            # print(f"{num} <-> {adj}")

print(f"邻码数量: {adjacent_count} 邻码：{adjacent_codes}")
for count, numbers in ckMap.items():
    #算和值numbers数相加设置给cksum_map
    cksum_map[count]= sum(numbers)
    ckkd_map[count]= max(numbers) - min(numbers);
    ckoushu_map[count]= len([num for num in numbers if num % 2 == 0]);
#统计ckkd_map里面的value值的数量
# print("ckkd_map:", ckkd_map)
# 定义分区
partitions = []
for i in range(1, 81, 10):
    partition = list(range(i, i + 10))
    partitions.append(partition)

# 创建一个字典来存储每个分区的行号和数量
partition_map = {f"{i}-{i+9}": [] for i in range(1, 81, 10)}
ckPartitionmap_Map = {}
# 遍历 ckMap，计算每行数据有几个分区，分区里面有几个数
for line_number, numbers in ckMap.items():
    ckPartionMap ={}
    for partition in partitions:
        ckPartionList = [num for num in numbers if num in partition]
        partition_str = f"{partition[0]}-{partition[-1]}"
        ckPartionMap[partition_str] = ckPartionList

    # print(f"ck{line_number} 中有 {len(ckPartionMap)} 个 partion 的值，分别是：{ckPartionMap}")
    ckPartitionmap_Map[line_number] = ckPartionMap

# 打印每个分区的行号和数量
# for line_number, ckPartionMap in ckPartitionmap_Map.items():
#     print(f"ck{line_number} 中有 {len(ckPartionMap)} 个 partion 的值，分别是：{ckPartionMap}")
#分别统计ckPartionMap中的ckPartion有多少个ckPartion数量
partionMap = {}
for line_number, ckPartionMap in ckPartitionmap_Map.items():
    for partition_str, ckPartionList in ckPartionMap.items():
        if partition_str not in partionMap:
            partionMap[partition_str] = []
        partionMap[partition_str].append({line_number:len(ckPartionList)})
# for partition_str, lineNumberPartion in partionMap.items():
#     print(f"{partition_str} 中有 {len(lineNumberPartion)} 个 partion 的值，分别是：{lineNumberPartion}")
# 计算前面4个分区中每个key的value的和值
sum_dict = {}
for partition_str, lineNumberPartion in partionMap.items():
    if partition_str in prepartions:
        for entry in lineNumberPartion:
            for key, value in entry.items():
                if key not in sum_dict:
                    sum_dict[key] = value
                else:
                    sum_dict[key] += value
# 打印前面4个分区中每个key的value的和值，并按value从大到小排序
sorted_sum_dict = dict(sorted(sum_dict.items(), key=lambda item: item[1], reverse=True))
# print(f"每个key的value的和值（按value从大到小排序）: {sorted_sum_dict}")
#查询value值是8到13之间的key
sumkeys = []
# for key, value in sorted_sum_dict.items():
#     if minsum < value <= maxsum:
#         sumkeys.append(key)
#         print(f"key: {key}, value: {value}")
# 计算前面4个分区中每个key的value的和值
partionsum_dict = {}
for partition_str, lineNumberPartion in partionMap.items():
    if partition_str in prepartions:
        for entry in lineNumberPartion:
            for key, value in entry.items():
                if key in sumkeys:
                    if partition_str not in partionsum_dict:
                        partionsum_dict[partition_str] = value
                    else:
                        partionsum_dict[partition_str] += value

# 打印前面4个分区中每个key的value的和值，并按value从大到小排序
sorted_partionsum_dict = dict(sorted(partionsum_dict.items(), key=lambda item: item[1], reverse=True))
# print(f"每个partion的value的和值（按value从大到小排序）: {sorted_partionsum_dict}")

# 查看对应数字有多少个，大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
choosegroups = []
for count, numbers in ckMap.items():
    # print("ck"+count, numbers)
    if count  in sumkeys:
      choosegroups+= numbers
choosecounter = Counter(choosegroups)
# 从1到80，如果不在groups中，就放到noNum列表中
choosenoNum = []
for i in range(1, 81):
    if i not in choosegroups:
        choosenoNum.append(i)
# print("choosenoNum:", choosenoNum)
chooseckcommons = {}
chooseckcommons[0] = choosenoNum
for number, count in choosecounter.items():
    if count not in chooseckcommons:
        chooseckcommons[count] = [number]
    else:
        chooseckcommons[count].append(number)
# print(f"sumkeys :{sumkeys}" )
# for count, numbers in chooseckcommons.items():
#     print(f"chooseckcommon{count}个数字：{sorted(list(set(numbers)))}")
choosecjcommon={}
for count, numbers in chooseckcommons.items():
    for cjtemp in cj:
        if cjtemp in numbers:
            if count not in choosecjcommon:
                choosecjcommon[count] = [cjtemp]
            else:
                 choosecjcommon[count].append(cjtemp)
            # print("cj:"+str(cjtemp)+";commoncount:"+str(count))

#cjcommon打印出来 按照count的顺序打印
# for count, numbers in choosecjcommon.items():
#     print("choosecjcommon"+str(count)+":", sorted(list(set(numbers))))

# 定义尾数分区
tails = []
for i in range(1, 10, 1):
    #j从0到8 i+j*10
    tail = [i + j * 10 for j in range(8)]
    tails.append(tail)
cktailmap_Map = {}
# 遍历 ckMap，计算每行数据有几个分区，分区里面有几个数
for line_number, numbers in ckMap.items():
    cktailMap ={}
    for partition in tails:
        ckPartionList = [num for num in numbers if num in partition]
        partition_str = f"{partition[0]}"
        cktailMap[partition_str] = ckPartionList

    # print(f"ck{line_number} 中有 {len(ckPartionMap)} 个 partion 的值，分别是：{ckPartionMap}")
    cktailmap_Map[line_number] = cktailMap

# 打印每个分区的行号和数量
# for line_number, ckPartionMap in cktailmap_Map.items():
#     print(f"ck{line_number} 中有 {len(ckPartionMap)} 个 tail 的值，分别是：{ckPartionMap}")
#分别统计ckPartionMap中的ckPartion有多少个ckPartion数量
tailsMap = {}
for line_number, ckPartionMap in cktailmap_Map.items():
    for partition_str, ckPartionList in ckPartionMap.items():
        if partition_str not in tailsMap:
            tailsMap[partition_str] = []
        tailsMap[partition_str].append({line_number:len(ckPartionList)})
# for partition_str, lineNumberPartion in tailsMap.items():
#     print(f"{partition_str} 中有 {len(lineNumberPartion)} 个 tail 的值，分别是：{lineNumberPartion}")

# 计算每个行号对应的尾列值的数量之和
tail_sum_map = {}
for line_number, ckPartionMap in cktailmap_Map.items():
    if line_number in sumkeys:
        for partition_str, ckPartionList in ckPartionMap.items():
            if partition_str not in tail_sum_map:
                tail_sum_map[partition_str] = 0
            tail_sum_map[partition_str]= tail_sum_map[partition_str]+len(ckPartionList)

# # 打印每个行号对应的尾列值的数量之和
# for line_number, total_count in tail_sum_map.items():
#     print(f"行号 {line_number} 的尾列值数量之和: {total_count}")

# 打印每个行号对应的尾列값的数量之和，并按value从大到小排序
sorted_tail_sum_map = dict(sorted(tail_sum_map.items(), key=lambda item: item[1], reverse=True))
# print(f"每个行号对应的尾列的数量之和（按value从大到小排序）: {sorted_tail_sum_map}")




# 定义起始点和间隔
start = 600
interval = 25

# 创建一个字典来存储结果
interval_map = {}

# 遍历 cksum_map 中的每个值
for key, value in cksum_map.items():
    # 计算该值所在的区间
    lower_bound = (value - start) // interval * interval + start
    upper_bound = lower_bound + interval

    # 将区间表示为字符串
    interval_str = f"{lower_bound}-{upper_bound}"

    # 如果该区间不在 interval_map 中，则创建一个新的列表
    if interval_str not in interval_map:
        interval_map[interval_str] = []

    # 将 key 添加到对应的区间列表中
    interval_map[interval_str].append(key)

# 打印结果
# for interval, keys in interval_map.items():
#     print(f"{interval}: {keys}")
cksum_map_counter = Counter(v for v in cksum_map.values())
# print("cksum_map_counter:", cksum_map_counter)
# print("ckoushu_map:", ckoushu_map)
ckoushu_map_counter = Counter(v for v in ckoushu_map.values())
# print("ckoushu_map_counter:", ckoushu_map_counter)
# 打印每个值及其出现的次数
# for value, count in value_counter.items():
#     print(f"{value}: {count}")

# 按位置统计打印
# print("\n=== 按位置统计数字出现次数 ===")
# for position in range(20):  # 假设最多20个位置
#     if position_stats[position]:  # 如果该位置有统计数据
#         print(f"第{position+1}个数字:")
#         # 按出现次数降序排列
#         sorted_position_stats = sorted(position_stats[position].items(),
#                                      key=lambda x: x[1], reverse=True)
#         for number, count in sorted_position_stats:
#             print(f"  [{number}:{count}]")
#         print()  # 空行分隔

for count, numbers in ckMap.items():
    common_numbers = [num for num in numbers if num in cj]
    print(f"ck{count}-cj：{common_numbers}")
# for count, numbers in ckMap.items():
#     common_numbers = [num for num in numbers if num in zx_sh]
#     print(f"ck{count} 中有 {len(common_numbers)} 个 zx_sh 的值，分别是：{common_numbers}")
#有到8次的数字的时候关注6，7，还有nonun
# cj = [1,4,7,8,10,15,21,27,31,33,35,37,43,44,49,51,63,64,66,74]  # 请用实际数字替换
# checkMap=checkMap={1: {'3': 2}, 2: {'1': 1}, 3: {'3': 3, '4': 1},
ckkd_map_counter = Counter(v for v in ckkd_map.values())
# print("ckkd_map_counter:", ckkd_map_counter)
# print("cksum_map:", cksum_map)
# 定义起始点和间隔
start = 600
interval = 25

# 创建一个字典来存储结果
interval_map = {}

# 遍历 cksum_map 中的每个值
for key, value in cksum_map.items():
    # 计算该值所在的区间
    lower_bound = (value - start) // interval * interval + start
    upper_bound = lower_bound + interval

    # 将区间表示为字符串
    interval_str = f"{lower_bound}-{upper_bound}"

    # 如果该区间不在 interval_map 中，则创建一个新的列表
    if interval_str not in interval_map:
        interval_map[interval_str] = []

    # 将 key 添加到对应的区间列表中
    interval_map[interval_str].append(key)

# 打印结果
# for interval, keys in interval_map.items():
#     print(f"{interval}: {keys}")
cksum_map_counter = Counter(v for v in cksum_map.values())
# print("cksum_map_counter:", cksum_map_counter)
# print("ckoushu_map:", ckoushu_map)
ckoushu_map_counter = Counter(v for v in ckoushu_map.values())
# print("ckoushu_map_counter:", ckoushu_map_counter)
# 打印每个值及其出现的次数
# for value, count in value_counter.items():
#     print(f"{value}: {count}")
# for count, numbers in ckMap.items():
#     common_numbers = [num for num in numbers if num in cj]
#     print(f"ck{count} 中有 {len(common_numbers)} 个 cj 的值，分别是：{common_numbers}")
#ckmap相邻交集并打印
ckjiaock_map = {}
jiaojiset=[]
jiaojish_map ={}
for count, numbers in ckMap.items():
    ckjiaock_count ={}
    comparecount = int(count)+1
    for count1,numbers1 in ckMap.items():
        if comparecount==int(count1):
         common_numbers = [num for num in numbers if num in numbers1]
         ckjiaock_count[count1] =common_numbers
         for commonnum in common_numbers:
            if commonnum not in jiaojiset:
              jiaojiset.append(commonnum)
         print(f"ck{count} 和 ck{count1} 的交集有 {len(common_numbers)} 个值，分别是：{common_numbers}")
         if cj_flag:
             cj_jiaoji = [num for num in cj if num in common_numbers]
             print(f"ck{count} 和 ck{count1} 的交集跟cj 的交集有 {len(cj_jiaoji)} 个 cj 的值，分别是：{cj_jiaoji}")
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
# print("jiaojiset:", sorted(list(set(jiaojiset))))
# if cj_flag:
#     cj_jiaojiset = [num for num in cj if num in jiaojiset]
#     print(f"cj 的交集有 {len(cj_jiaojiset)} 个值，分别是：{cj_jiaojiset}")
#1到80的数字减去jiaojiset 剩余并打印
# remaining_numbers = sorted(list(set(range(1, 81)) - set(jiaojiset)))
# print("remaining_numbers:", remaining_numbers)
# if cj_flag:
#     cj_remaining_numbers = [num for num in cj if num in remaining_numbers]
#     print(f"cj 的剩余有 {len(cj_remaining_numbers)} 个值，分别是：{cj_remaining_numbers}")
#ckmap减去jiaojiset 剩余的值
# for count, numbers in ckMap.items():
#     nojiaoji_numbers = [num for num in numbers if num not in jiaojiset]
#     print(f"ck{count} 中有 {len(nojiaoji_numbers)} 个 没有jiaojiset 的值，分别是：{nojiaoji_numbers}")
#     if cj_flag:
#         cj_nojiaoji_numbers = [num for num in cj if num in nojiaoji_numbers]
#         print(f"ck{count} 中有 {len(cj_nojiaoji_numbers)} 个 cj 的值，分别是：{cj_nojiaoji_numbers}")
# ckremaining_numbers = {}
# for count, ckjiaock_count in ckjiaock_map.items():
#     # 각 ckjiaock_count를 내림차순으로 정렬하여 상위 3개 선택
#     sorted_cks = sorted(ckjiaock_count.items(), key=lambda item: len(item[1]), reverse=True)
#     top_3_cks = sorted_cks[:2]
#     kill_numbers = set()
#     for count1, intersection_numbers in top_3_cks:
#         kill_numbers.update(intersection_numbers)
#     remaining_numbers = sorted(list(set(ckMap[count]) - set(kill_numbers)))
#     print(f"ck{count} 跟杀号交集有 {len(remaining_numbers)} 个值，分别是：{remaining_numbers}")
#     ckremaining_numbers[count] = remaining_numbers
#     # 新增：计算与 cj 的交集
#     cj_intersection = list(set(remaining_numbers) & set(cj))
#     cj_intersection.sort()
#     if len(cj_intersection)==0:
#         continue
# for count,jiaojish_count  in jiaojish_map.items():
#     print(f"ck{count} 交集有 {len(jiaojish_count)} 个值，分别是：{set(jiaojish_count)}")
#     if cj_flag:
#         cj_jiaoji = list(set(jiaojish_count) & set(cj))
#         print(f"ck{count} cj_jiaoji: {cj_jiaoji}（共 {len(cj_jiaoji)} 个）")
#     remaining_numbers = sorted(list(set(ckMap[str(count)]) - set(jiaojish_count)))
#     # print(f"ck{count} remaining_numbers: {remaining_numbers}（共 {len(remaining_numbers)} 个）")
#     #
#     if cj_flag:
#         cj_remaining = list(set(remaining_numbers) & set(cj))
#         print(f"ck{count} cj_remaining: {cj_remaining}（共 {len(cj_remaining)} 个）")
    # print(f"ck{count} remaining_numbers 与 cj 的交集: {cj_intersection}（共 {len(cj_intersection)} 个）")
# for count, numbers in ckremaining_numbers.items():
#     ckjiaock_count ={}
#     ckremaining_intersection = []
#     for count1,numbers1 in ckremaining_numbers.items():
#         if count==count1:
#             continue
#         common_numbers = [num for num in numbers if num in numbers1]
#         ckjiaock_count[count1] =common_numbers
#         if len(common_numbers)==0:
#             continue
#         # print(f"ckremain{count} 和 ckremain{count1} 的交集有 {len(common_numbers)} 个值，分别是：{common_numbers}")
#         # 新增：计算与 cj 的交集
#         ckremaining_intersection.extend(common_numbers)
#         cj_intersection = list(set(common_numbers) & set(cj))
#         cj_intersection.sort()
#         if len(cj_intersection)==0:
#             continue
#     print(f"ckremain{count} ckremaining_intersection: {sorted(list(ckremaining_intersection)) }")
#     cj_intersection = list(set(ckremaining_intersection) & set(cj))
#     cj_intersection.sort()
#     if len(cj_intersection) == 0:
#         continue
    # print(f"ckremain{count} cj_intersection: {cj_intersection}（共 {len(cj_intersection)} 个）")



#有到8次的数字的时候关注6，7，还有nonun
# cj = [1,4,7,8,10,15,21,27,31,33,35,37,43,44,49,51,63,64,66,74]  # 请用实际数字替换
# checkMap=checkMap={1: {'3': 2}, 2: {'1': 1}, 3: {'3': 3, '4': 1}, 4: {'3': 4, '5': 5, '6': 6}, 5: {'1': 4, '6': 9}, 6: {'2': 8}, 7: {'5': 10}, 8: {'3': 9}, 9: {'5': 12}, 10: {'3': 11, '5': 14}, 12: {'3': 13}, 13: {'5': 16, '6': 16}, 14: {'3': 14, '4': 11}, 15: {'3': 17, '4': 14, '5': 19}, 16: {'1': 15, '6': 18}, 17: {'1': 16, '3': 18}, 18: {'2': 17}, 19: {'4': 19}}
# 初始化结果字典
result = {}

# for count, numbers in ckMap.items():
#     print("ck"+count, numbers)
#
#     # 打印当前行每个位置的数字
#     print(f"  位置统计: ", end="")
#     for pos, num in enumerate(numbers):
#         print(f"第{pos+1}位[{num}]", end=" ")
#     print()
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
zshahao =[]
bjhao =[]
xiaoyu3=[]
ckcommons = {}
ckcommons[0] = noNum
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)

#大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
for count, numbers in ckcommons.items():
    # filename contain _h 就查询count==3 or count ==4
    # if filename.find("_h") != -1:
    #     if count==3 or count ==4:
    #         bjhao+= numbers
    # else:
    #     if count==2 or count ==3:
    #         bjhao+= numbers
    if count >=2 and count<=4:
        bjhao+= numbers
    if count != 1 and count<3:
        xiaoyu3+= numbers
    if count > 4 or count <=1 :
        #numbers是一个列表，里面是数字，sh是一个列表，里面是数字，把numbers放到sh中
        shahao+= numbers
        if count>5:
            zshahao+= numbers
        print("ckcommons"+str(count)+":", sorted(list(set(numbers))))
    else:
        print("ckcommons"+ str(count)+":", sorted(list(set(numbers))))


cjcommon={}
for count, numbers in ckcommons.items():
    for cjtemp in cj:
        if cjtemp in numbers:
            if count not in cjcommon:
                cjcommon[count] = [cjtemp]
            else:
                 cjcommon[count].append(cjtemp)
            # print("cj:"+str(cjtemp)+";commoncount:"+str(count))

#cjcommon打印出来 按照count的顺序打印
if cj_flag:
    for count, numbers in cjcommon.items():
        print("cjcommon" + str(count) + ":", sorted(list(set(numbers))))
    for cjtemp in cj:
        if cjtemp in noNum:
            print("cj:" + str(cjtemp) + ";nonum")
print("shahao:", sorted(list(set(shahao))))
#shahao跟cj交集
shahao_cj = [num for num in shahao if num in cj]
print("shahao_cj:", sorted(list(set(shahao_cj))))
print("zshahao:", sorted(list(set(zshahao))))
# 获取 shahao 中每个数字的相邻号码并合并
# shahao=[1,3,5,22,27,33,34,45,48,58,59,60,62,65,70,71,73]

# 统计尾数0-9在ckcommons2到ckcommons4中的分布
ckcommons_2to4 = []
for c in range(2, 5):
    if c in ckcommons:
        ckcommons_2to4.extend(ckcommons[c])
tail_stat = {i: [] for i in range(10)}
for num in ckcommons_2to4:
    tail_stat[num % 10].append(num)
for tail in range(10):
    if cj_flag:
        tail_cj = [num for num in tail_stat[tail] if num in cj]
        print(f"尾数{tail}: {sorted(tail_stat[tail])}（共{len(tail_stat[tail])}个） cj:{sorted(tail_cj)}（共{len(tail_cj)}个）")
    else:
        print(f"尾数{tail}: {sorted(tail_stat[tail])}（共{len(tail_stat[tail])}个）")

adjacent_numbers_list = []
for number in shahao:
    adjacent_numbers = [number - 1, number + 1]
    adjacent_numbers_list.extend(adjacent_numbers)

# 去除 shahao 中存在的数字
filtered_adjacent_numbers = [num for num in adjacent_numbers_list if num not in shahao]

# 去重并排序
unique_filtered_adjacent_numbers = sorted(list(set(filtered_adjacent_numbers)))

print("过滤后的相邻号码:", unique_filtered_adjacent_numbers)
#zshahao跟cj交集
zshahao_cj = [num for num in zshahao if num in cj]
print("zshahao_cj:", sorted(list(set(zshahao_cj))))

# 获取斜码
oblique_codes = data_analysis.get_oblique_codes(cj, cj_pre)
print("斜码:", oblique_codes)
print("斜码长度", len(oblique_codes),len(oblique_codes)/4)
# 获取跳码
jump_codes = data_analysis.get_jump_codes(cj, cj_pre)
print("跳码:", jump_codes)
print("跳码长度", len(jump_codes),len(jump_codes)/4)
allremain_cj = []
remaining_numbers_data=[]
for count,jiaojish_count  in jiaojish_map.items():
    # print(f"ck{count} 交集有 {len(jiaojish_count)} 个值，分别是：{set(jiaojish_count)}")
    remaining_numbers = sorted(list(set(ckMap[str(count)]) - set(jiaojish_count)))
    #remaining_numbers跟unique_filtered_adjacent_numbers 交集
    remaining_numbers = sorted(list(set(remaining_numbers) & set(unique_filtered_adjacent_numbers)))
    # print(f"ck{count} remaining_numbers: {remaining_numbers}（共 {len(remaining_numbers)} 个）")
    remaining_numbers_data.append(remaining_numbers)

    #remaining_numbers跟cj交集
    # if cj_flag:
    #     remaining_numbers_cj = [num for num in remaining_numbers if num in cj]
    #     allremain_cj.extend(remaining_numbers_cj)
    #     print(f"ck{count} remaining_numbers_cj: {remaining_numbers_cj}（共 {len(remaining_numbers_cj)} cj 个）")

# 步骤 1：构建冲突图
conflict_graph = data_analysis.build_conflict_graph(remaining_numbers_data)

# 步骤 2：获取所有候选数字（根据你的数据范围）
all_candidate_numbers = set(num for group in remaining_numbers_data for num in group)

# 步骤 3：找出所有可行的互斥组合
valid_combinations = data_analysis.find_all_valid_combinations(
    conflict_graph=conflict_graph,
    all_candidates=all_candidate_numbers,
    required_size= 8 # 可选：指定组合长度
)

# 输出结果
print("可行的互斥数字组合数量:", len(valid_combinations))
for idx, combo in enumerate(valid_combinations[:12], 1):  # 只展示前10个组合
    print(f"组合 {idx}: {combo}")
    # remaining_numbers跟cj交集
    if cj_flag:
        combo_cj = [num for num in combo if num in cj]
        print(f"{idx} combo_cj: {combo_cj}（共 {len(combo_cj)} cj 个）")


#remaining_numbers_data去重打印
# 将所有remaining_numbers中的数字合并到一个列表中，然后去重排序
all_remaining_numbers = []
for numbers_list in remaining_numbers_data:
    all_remaining_numbers.extend(numbers_list)

print("remaining_numbers_data:", sorted(list(set(all_remaining_numbers))))
print("allremain_cj:", sorted(list(set(allremain_cj))))
# print("bjhao:", sorted(list(set(bjhao))))
# #bjhao跟cj交集
# bjhao_cj = [num for num in bjhao if num in cj]
# print("bjhao_cj:", sorted(list(set(bjhao_cj))))
# #bjhao跟cj交集
# bjhao_notcj = [num for num in bjhao if num not in cj]
# print("bjhao_notcj:", sorted(list(set(bjhao_notcj))))
#遍历cj，使用数字作为key，数字跟数字的加减1的值的列表作为value，之后遍历ckcommons,如果数字在value中，且count小于4，就打印出来,并且打印出来ckcommons的count值
# cjMap = {}
# #小于3的数字，放到列表，之后去重打印
# xuanze = []
#
# for number in cj:
#     cjMap[number] = [number-1, number+1,number]
# # for count, numbers in ckcommons.items():
# #     for number in numbers:
# #        for key, value in cjMap.items():
# #            if number in value and number not in shahao and count<3:
# #                print("cjMap:", number, value, count,key)
# #                xuanze.append(number);
# #cjMap noNum中存在则打印出来
# for key, value in cjMap.items():
#     for number in noNum:
#       if number in value:
#         print("nonum:", number, value, key)
#
# #xz去重打印
# print("xuanze:", sorted(list(set(xuanze))))
# print("nonum:", sorted(list(set(noNum))))
# #打印顺序排序打印
#

# print("xiaoyu3:", sorted(list(set(xiaoyu3))))
# #xy3跟xz的
# print("xiaoyu3_xuanze:", list(set(xiaoyu3) & set(xuanze)))
#ckmap跟shahao分别相减生成对应的ck_shmap 并打印,之后再跟cj生成ck_sh_cjmap,并打印
# 初始化 ck_shmap 和 ck_sh_cjmap
ck_shmap = {}
ck_sh_notcjmap = {}
ck_sh_cjpre_cjmap = {}
ck_sh_zxmap = {}

# 计算 ck_shmap：ckMap 中每个 ck 的数字减去 shahao 中的数字
for count, numbers in ckMap.items():
    ck_shmap[count] = [num for num in numbers if num not in shahao]
    # if cj_flag== False:
    #     ck_shmap[count] =[num for num in ck_shmap[count] if num not in cj]
    # else:
    #     ck_shmap[count] =[num for num in ck_shmap[count] if num not in cj_pre]
for count, numbers in ck_shmap.items():
    ck_sh_zxmap[count] = [num for num in numbers if num not in zx_sh]

# 打印每个ck中属于shahao的数字
for count, numbers in ckMap.items():
    shahao_in_ck = [num for num in numbers if num not in shahao]
    print(f"ck{count}-shahao：{shahao_in_ck}")
# 打印 ck_shmap
# print("ck_shmap:")
# for count, numbers in ck_shmap.items():
#     print(f"ck{count}-sh ：{numbers}")
# 计算 ck_sh_cjmap：ck_shmap 中每个 ck 的数字与 cj 的交集
cksh_cjmap={}
for count, numbers in ck_shmap.items():
    cksh_cjmap[count] = [num for num in numbers if num in cj]
cksh_zxcjmap={}
for count, numbers in ck_sh_zxmap.items():
    cksh_zxcjmap[count] = [num for num in numbers if num in cj]
# if cj_flag:
#     # 打印 ck_sh_cjmap
#     print("\ncksh_cjmap:")
#     for count, numbers in cksh_cjmap.items():
#         print(f"ck_shmap{count} 与 cj 的交集：{numbers}")
#
# print("ck_sh_zxmap:")
# for count, numbers in ck_sh_zxmap.items():
#     print(f"ck{count}-sh_zx ：{numbers}")
#跟unique_filtered_adjacent_numbers 交集
ck_sh_zx_adjecent_map={}
#false执行
# if cj_flag == False:
#     for count, numbers in ck_sh_zxmap.items():
#         ck_sh_zx_adjecent_map[count] = [num for num in numbers if num in unique_filtered_adjacent_numbers]
#         print(f"ck_sh_zx_adjecent_map{count}：{ck_sh_zx_adjecent_map[count]}")
#
# if cj_flag:
#     # 打印 ck_sh_cjmap
#     print("\ncksh_zxcjmap:")
#     for count, numbers in cksh_zxcjmap.items():
#         print(f"ck_sh_zxmap{count} 与 cj 的交集：{numbers}")
#
# # 计算 ck_sh_cjmap：ck_shmap 中每个 ck 的数字与 cj 的交集
# cksh_sh4map={}
# for count, numbers in ck_shmap.items():
#     cksh_sh4map[count] = [num for num in numbers if num not in ckcommons[4]]
#
# # 打印 ck_sh_cjmap
# print("\ncksh_sh4map:")
# for count, numbers in cksh_sh4map.items():
#     print(f"ck_shmap{count} 与 sh4 的差：{numbers}")
#
# # 计算 ck_sh_cjmap：ck_shmap 中每个 ck 的数字与 cj 的交集
# for count, numbers in ck_shmap.items():
#     ck_sh_notcjmap[count] = [num for num in numbers if num not in cj]
#
# # 打印 ck_sh_cjmap
# print("\nck_sh_cjpremap:")
# for count, numbers in ck_sh_notcjmap.items():
#     print(f"ck{count}-sh - cj差集 的：{numbers}")
#
#
# # 计算 ck_sh_cjmap：ck_shmap 中每个 ck 的数字与 cj 的交集
# ck_sh_notcj_notsh2map = {}
# for count, numbers in ck_sh_notcjmap.items():
#     ck_sh_notcj_notsh2map[count] = [num for num in numbers if num not in sh2]
# # 打印 ck_sh_cjmap
# print("\nck_sh_notcj_notsh2map:")
# for count, numbers in ck_sh_notcj_notsh2map.items():
#     print(f"ck_sh_notcj_notsh2map{count} 与 sh2 的差集：{numbers}")
#
#
# # 计算 ck_sh_cjmap：ck_shmap 中每个 ck 的数字与 cj 的交集
# for count, numbers in ck_sh_notcjmap.items():
#     ck_sh_cjpre_cjmap[count] = [num for num in numbers if num in cj]
# # 打印 ck_sh_cjmap
# print("\nck_sh_cjpre_cjmap:")
# for count, numbers in ck_sh_cjpre_cjmap.items():
#     print(f"ck_sh_cjpre_cjmap{count} 与 cj 的交集：{numbers}")
#
#
#
# # 可视化结果
# print("\nSummary:")
# print("ck_shmap:", ck_shmap)
# print("ck_sh_cjpre_cjmap:", ck_sh_cjpre_cjmap)


containNum=[]
# containNum=[8,62]
kaixin=[]

# df = data_analysis.read_and_clean_data(filename)
# data_analysis.remove_and_count(df, shahao,6)
# data_analysis.remove_and_count(df,  (list(set(shahao) | set(kaixin))),4)
# # data_analysis.remove_and_count_contain(df, (list(set(shahao) | set(kaixin))),7,containNum)
# ck_cjpremap={}
# for count, numbers in ckcommons.items():
#     for cjtemp in cj_pre:
#         if cjtemp in numbers:
#             if count not in ck_cjpremap:
#                 ck_cjpremap[count] = [cjtemp]
#             else:
#                  ck_cjpremap[count].append(cjtemp)

# for count, numbers in ck_cjpremap.items():
#     print("ck_cjpremap交集"+str(count)+":", sorted(list(set(numbers))))
# ck_cjpremap2={}
# for count, numbers in ckcommons.items():
#     for cjtemp in numbers:
#         if cjtemp not in cj_pre:
#             if count not in ck_cjpremap2:
#                 ck_cjpremap2[count] = [cjtemp]
#             else:
#                  ck_cjpremap2[count].append(cjtemp)
#
# for count, numbers in ck_cjpremap2.items():
#     print("ck_cjpremap2减集"+str(count)+":", sorted(list(set(numbers))))
#生成1到80的数字
# all_numbers = set(range(1, 81))
# shmax=[2,3,12,14,16,21,23,24,25,30,32,33,35,36,38,41,43,45,46,47,49,50,56,58,60,63,64,65,66,67,73,74,75,77,78]
# shahao = set(shmax)
# chooseMax = all_numbers-shahao-set(cj)
# #打印
# print("chooseMax:", chooseMax)
