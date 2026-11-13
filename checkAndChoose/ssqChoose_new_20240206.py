from collections import Counter

import csv
from itertools import combinations, product

import data_analysis
filename = "./zip/ssq_20261104.csv"  # 替换为你的CSV文件名

ckRedMap = {}  # 创建一个空字典来存储行号和列表的映射
ckBlueMap = {}  # 创建一个空字典来存储行号和列表的映射
# 创建位置统计字典，用于统计每个位置上的数字出现次数
red_position_stats = {i: {} for i in range(6)}  # 双色球红球有6个位置
blue_position_stats = {}  # 蓝球位置统计
# cj_red = [1,5,6,7,9,14,16,18,23,27,29,30,32]  # 请用实际数字替换
# cj_red = [1,2,13,21,23,29]  #n 请用实际数字替换
cj_red_raw = [13,14,19,25,29,32,12]  #n 请用实际数字替换，最后一位是篮球
cj_blue = [cj_red_raw[-1]]  # 最后一位是篮球
cj_red = cj_red_raw[:-1]    # 前6位是红球
red_sh=[]
red_sh2=[]
cj_red_pre = [5,6,10,25,27,30,11]
cj_blue_pre=[]

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # 跳过第一行（标题行）

    for line_number, row in enumerate(csv_reader, start=1):
        ckBlueMap[str(line_number)] = [int(row[-1])]  # 获取最后一个元素
        red_numbers = list(map(int, row[:-1]))
        ckRedMap[str(line_number)] = red_numbers

        # 统计红球每个位置上的数字出现次数
        for position, number in enumerate(red_numbers):
            if position >= len(red_position_stats):
                print(f"警告: 红球位置 {position} 超出统计范围")
                continue
            if number not in red_position_stats[position]:
                red_position_stats[position][number] = 0
            red_position_stats[position][number] += 1

        # 统计蓝球数字出现次数
        blue_number = int(row[-1])
        if blue_number not in blue_position_stats:
            blue_position_stats[blue_number] = 0
        blue_position_stats[blue_number] += 1

# 按位置统计打印红球
print("\n=== 红球按位置统计数字出现次数 ===")
# for position in range(6):  # 双色球红球有6个位置
#     if red_position_stats[position]:  # 如果该位置有统计数据
#         print(f"第{position+1}个红球数字:")
#         # 按出现次数降序排列
#         sorted_position_stats = sorted(red_position_stats[position].items(),
#                                      key=lambda x: x[1], reverse=True)
#         for number, count in sorted_position_stats:
#             print(f"  [{number}:{count}]")
#         print()  # 空行分隔

# 蓝球统计打印
print("=== 蓝球数字出现次数 ===")
sorted_blue_stats = sorted(blue_position_stats.items(), key=lambda x: x[1], reverse=True)
for number, count in sorted_blue_stats:
    print(f"  [{number}:{count}]")
print()

for count, numbers in ckRedMap.items():
    common_numbers = [num for num in numbers if num in cj_red]
    print(f"ckred{count}：{numbers}")
    # 打印当前行每个位置的数字
    # print(f"  位置统计: ", end="")
    # for pos, num in enumerate(numbers):
    #     print(f"第{pos+1}位[{num}]", end=" ")
    # print()
    # print(f"ckred{count} 中有 {len(common_numbers)} 个 cj_red 的值，分别是：{common_numbers}")

for count, numbers in ckRedMap.items():
    common_numbers = [num for num in numbers if num in cj_red]
    # print(f"ckred{count} 值，分别是：{numbers}")
    print(f"ckred{count}_cj：{common_numbers}")
    # commonsh_numbers = [num for num in numbers if num in red_sh]
    # print(f"ckred{count} 中有 {len(commonsh_numbers)} 个 red_sh 的值，分别是：{commonsh_numbers}")
# real_sh_red=[]
# for count, numbers in ckRedMap.items():
#     commonsh_numbers = [num for num in numbers if num in red_sh]
#     print(f"ckred{count} 中有 {len(commonsh_numbers)} 个 red_sh 的值，分别是：{commonsh_numbers}")
#     if len(commonsh_numbers) >= 2:
#         print(f"ckred{count} 中都有red_sh的值，ckred{count}的所有值，分别是：{numbers}")
#         # 将列表转换为集合以执行差集操作
#         real_sh_red.extend(set(numbers))

queues = []
chooseNum = []
# for count, numbers in ckRedMap.items():
#     commonsh_numbers = [num for num in numbers if num not in red_sh2]
#     print(f"ckred{count} 中去除red_sh2  的值，分别是：{commonsh_numbers}")
#     if len(commonsh_numbers) >= 1 or  len(commonsh_numbers)  ==0:
#         for num in commonsh_numbers:
#             if num not in chooseNum:
#                 chooseNum.append(num)
#         queues.append(commonsh_numbers);
# print("queues:", queues)
# print("chooseNum:", sorted(set(chooseNum)))
# #去重打印
# print("real_sh_red:", sorted(set(list(real_sh_red))))
#ckmap相邻交集并打印
ckjiaock_map = {}
jiaojish_map ={}
jiaojish = []
for count, numbers in ckRedMap.items():
    ckjiaock_count ={}
    comparecount = int(count)+1
    for count1,numbers1 in ckRedMap.items():
        if comparecount==int(count1):
         common_numbers = [num for num in numbers if num in numbers1]
         ckjiaock_count[count1] =common_numbers
         jiaojish.extend(common_numbers)
         current_key = int(count)
         # print(f"ck{count} 和 ck{count1} 的交集有 {len(common_numbers)} 个值，分别是：{common_numbers}")
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
print("jiaojish:", sorted(set(jiaojish)))
#ckRedMap 减去jiaojish 并打印，for循环
for count, numbers in ckRedMap.items():
    common_numbers = [num for num in numbers if num not in jiaojish]
    print(f"ckred{count} 中有 {len(common_numbers)} 个不在 jiaojish 的值，分别是：{common_numbers}")
# 查看对应数字有多少个，大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
for count,jiaojish_count  in jiaojish_map.items():
    print(f"ck{count} 交集有 {len(jiaojish_count)} 个值，分别是：{set(jiaojish_count)}")
    remaining_numbers = sorted(list(set(ckRedMap[str(count)]) - set(jiaojish_count)))
    # print(f"ck{count} remaining_numbers: {remaining_numbers}（共 {len(remaining_numbers)} 个）")
    # print(f"ck{count} remaining_numbers 与 cj 的交集: {cj_intersection}（共 {len(cj_intersection)} 个）")
ckkd_map = {}
ckoushu_map={}
cksum_map={}
for count, numbers in ckRedMap.items():
    #算和值numbers数相加设置给cksum_map
    cksum_map[count]= sum(numbers)
    ckkd_map[count]= max(numbers) - min(numbers);
    ckoushu_map[count]= len([num for num in numbers if num % 2 == 0]);
#统计ckkd_map里面的value值的数量
# print("ckkd_map:", ckkd_map)
ckkd_map_counter = Counter(v for v in ckkd_map.values())
# print("ckkd_map_counter:", ckkd_map_counter)
# print("cksum_map:", cksum_map)
# 定义起始点和间隔
start = 60
interval = 10

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
groups = []
for count, numbers in ckBlueMap.items():
    # print("ck"+count, numbers)
    groups+= numbers
counter = Counter(groups)

# print("groups:", list(set(groups)))
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
        print("篮球"+ str(count)+":", sorted(numbers))
    if count >= 2:
        #numbers是一个列表，里面是数字，sh是一个列表，里面是数字，把numbers放到sh中
        shahao+= numbers
        print("篮球"+str(count)+":", sorted(numbers))
print("篮球杀号:", list(set(shahao)))
print("篮球非杀号:", list(set(feishahao)))
print("篮球noNum:", sorted(noNum))
# 假设你的数字组如下：
# for count, numbers in ckRedMap.items():
#     # print("ck"+count, sorted(numbers))
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
# shahao =[]
feishahao=[]
ckcommons = {}
ckcommons[0] =noNum
for number, count in counter.items():
    if count not in ckcommons:
        ckcommons[count] = [number]
    else:
        ckcommons[count].append(number)
#大于4个的单独列出来并打印出来。小于4个的也单独列出来并打印出来
for count, numbers in ckcommons.items():
    if count>4:
        shahao += numbers
        print("红球"+ str(count)+":", sorted(numbers))
    if count <=3:
        feishahao+= numbers
        #numbers是一个列表，里面是数字，sh是一个列表，里面是数字，把numbers放到sh中
        print("红球"+str(count)+":", sorted(numbers))
    if count ==4:
        print("红球"+str(count)+":", sorted(numbers))
ck_shmap = {}
ck_sh_notcjpremap = {}
ck_sh_cjpre_cjmap = {}

# 计算 ck_shmap：ckMap 中每个 ck 的数字减去 shahao 中的数字
for count, numbers in ckRedMap.items():
    ck_shmap[count] = [num for num in numbers if num not in shahao]
print(f"shahao:{shahao}")
# 打印 ck_shmap
# print("ck_shmap:")
# for count, numbers in ck_shmap.items():
#     print(f"ck{count}-sh ：{numbers}")

# cksh_cjmap = {}
# # 计算 ck_shmap：ckMap 中每个 ck 的数字减去 shahao 中的数字
# for count, numbers in ck_shmap.items():
#     cksh_cjmap[count] = [num for num in numbers if num  in cj_red]
# for count, numbers in cksh_cjmap.items():
#     print(f"cksh{count}-cj ：{numbers}")

cksh_cjshmap = {}
# 计算 ck_shmap：ckMap 中每个 ck 的数字减去 shahao 中的数字
# for count, numbers in ck_shmap.items():
#     cksh_cjshmap[count] = [num for num in numbers if num not in cj_red]
# for count, numbers in cksh_cjshmap.items():
#     print(f"cksh{count}-cjsh ：{numbers}")
# 构建 queues
queues = []
for key, values in cksh_cjshmap.items():
    queues.append(values)

# print(f"queues ：{queues}")

#从cksh_cjshmap里面每个队列里面选择0到1个数字，

# print("红球noNum:", sorted(noNum))
# print("红球杀号:", list(set(shahao)))
# print("红球非杀号:", list(set(feishahao)))

# df = data_analysis.read_and_clean_data_ssq_red(filename)
# data_analysis.remove_and_count(df, shahao,2)

# for count, numbers in ckcommons.items():
#     for cjtemp in cj_red:
#         if cjtemp in numbers:
#             print("cj:"+str(cjtemp)+";commoncount:"+str(count))
# for cjtemp in cj_red:
#     if cjtemp in noNum:
#             print("cj:"+str(cjtemp)+";nonum")
ckredcommon_cjmap = {}

# 计算 ck_shmap：ckMap 中每个 ck 的数字减去 shahao 中的数字
for count, numbers in ckcommons.items():
    ckredcommon_cjmap[count] = [num for num in numbers if num in cj_red]


# 打印 ck_shmap
print("ckred_cjmap:")
for count, numbers in ckredcommon_cjmap.items():
    print(f"common{count}-cj ：{numbers}")
# 打印 ck_shmap
print("ckred:")
for count, numbers in ckcommons.items():
    print(f"common{count} ：{sorted(numbers)}")

for count, numbers in ckcommons.items():
    commonsh_numbers = [num for num in numbers if num not in red_sh2]
    print(f"common{count} 中去除red_sh2  的值，分别是：{commonsh_numbers}")

all_numbers = set(range(1, 33))
#打印
print("all_numbers:", all_numbers)
# 获取斜码
oblique_codes = data_analysis.get_oblique_codes(cj_red, cj_red_pre,33)
print("斜码:", oblique_codes)
print("斜码长度", len(oblique_codes),len(oblique_codes)/4)
# 获取跳码
jump_codes = data_analysis.get_jump_codes(cj_red, cj_red_pre,33)
print("跳码:", jump_codes)
print("跳码长度", len(jump_codes),len(jump_codes)/4)

# oblique_codes = data_analysis.get_oblique_codes(cj_blue, cj_blue_pre,15)
# print("斜码:", oblique_codes)
# print("斜码长度", len(oblique_codes),len(oblique_codes)/4)
# # 获取跳码
# jump_codes = data_analysis.get_jump_codes(cj_blue, cj_blue_pre,15)
# print("跳码:", jump_codes)
# print("跳码长度", len(jump_codes),len(jump_codes)/4)

# kaixin=[1,14]
#
# df = data_analysis.read_and_clean_data_ssq_red(filename)
# data_analysis.remove_and_count(df, kaixin,3)
# df = data_analysis.read_and_clean_data_ssq_red(filename)
# counter_pairs = data_analysis.count_pairs(df,3)
# data_analysis.print_common_pairs(counter_pairs,100)
