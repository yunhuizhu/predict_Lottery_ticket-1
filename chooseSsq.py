# 假设你的数字组如下：
group1_red = [1,4,9,22,26,31] #窗口3
group1_blue = [3] #窗口3
group2_red = [2,12,13,14,24,29] #窗口4
group2_blue = [1] #窗口4
group3_red = [13,15,18,24,28,33] #窗口5
group3_blue = [3] #窗口5
group4_red = [2,10,11,14,21,27] #shangyiqikaijiangjieguo
group4_blue = [11] #shangyiqikaijiangjieguo

group5=[2,7,10,13,28,29,34,37,38,44,48,49,50,52,57,59,63,65,72] #上一期中奖结果

# 找出前三组都存在的数字
common_red_numbers = set(group1_red) & set(group2_red) & set(group3_red)
print("Common red numbers in first three groups: ", common_red_numbers)

# 找出0到80中没有在四组里面的数字
# all_numbers = set(range(81)) # 创建一个包含0到80的集合
# numbers_in_groups = set(group1 + group2 + group3 + group4) # 创建一个包含四组所有数字的集合
# missing_numbers = all_numbers - numbers_in_groups
# print("Numbers not in any group: ", missing_numbers)
# filter_number = missing_numbers-set(group5)
# print("filter_number: ", filter_number)

same_numbers4 = set(group3_red) & set(group1_red)
same_numbers5 = set(group3_red) & set(group2_red)
same_numbers6 = set(group1_red) & set(group2_red)
same_numbers7 = set(group4_red) & set(group1_red)
same_numbers8 = set(group4_red) & set(group2_red)
same_numbers9 = set(group4_red) & set(group3_red)

print("Group 3 and group1 same numbers: ", same_numbers4)
print("Group 3 and group2 same numbers: ", same_numbers5)
print("Group 1 and group2 same numbers: ", same_numbers6)

print("Group 4 and group1 same numbers: ", same_numbers7)
print("Group 4 and group2 same numbers: ", same_numbers8)
print("Group 4 and group3 same numbers: ", same_numbers9)
