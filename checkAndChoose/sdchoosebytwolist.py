# 给定的两个列表
list1 =['03', '04', '05', '07', '14', '19', '23', '24', '27', '34', '39', '45', '46', '47', '48', '49', '56', '68', '69', '78', '79', '89']
list2 = ['01', '02', '04', '08', '09', '13', '15', '19', '23', '24', '25', '34', '35', '36', '38', '39', '45', '56', '57', '58', '59', '67', '79', '89']

# 生成所有可能的三数字组合（0-9）
from itertools import combinations

all_combinations = list(combinations(range(10), 3))

# 存储满足条件的组合
valid_combinations = []

# 检查每个三数字组合
for combo in all_combinations:
    # 生成三个数字对（按升序排列）
    pairs = []
    for pair in combinations(combo, 2):
        sorted_pair = ''.join(str(d) for d in sorted(pair))
        pairs.append(sorted_pair)

    # 检查每个数字对的类型
    common_count = 0
    in_any_list_count = 0

    for pair in pairs:
        in_list1 = pair in list1
        in_list2 = pair in list2

        if in_list1 and in_list2:
            common_count += 1
            in_any_list_count += 1
        elif in_list1 or in_list2:
            in_any_list_count += 1

    # 检查条件：恰好一个共有对，另外两个组合中至少有一个存在于某个列表中
    if common_count >= 1 and common_count <= 2 and in_any_list_count >= 1:  # 至少2个对在某个列表中
        valid_combinations.append(''.join(str(d) for d in sorted(combo)))

# 输出所有满足条件的组合
print("满足条件的组合:")
for combo in valid_combinations:
    print(combo)

# 详细输出每个有效组合的情况
print("\n详细分析:")
for combo in valid_combinations:
    pairs = []
    for pair in combinations([int(d) for d in combo], 2):
        sorted_pair = ''.join(str(d) for d in sorted(pair))
        pairs.append(sorted_pair)

    print(f"\n组合 {combo}:")
    for pair in pairs:
        in_list1 = pair in list1
        in_list2 = pair in list2
        status = ""
        if in_list1 and in_list2:
            status = "共有对（两个列表都有）"
        elif in_list1:
            status = "只在列表1"
        elif in_list2:
            status = "只在列表2"
        else:
            status = "不在任何列表"
        print(f"  {pair}: {status}")