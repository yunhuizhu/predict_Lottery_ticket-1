# 假设你的数字组如下：
group1 = [6,7,9,14,16,18,23,24,30,36,44,50,54,55,58,59,65,76,77,80] #窗口3
group2 = [3,7,8,9,12,20,25,32,34,36,37,40,45,51,63,65,67,71,73,79] #窗口4
group3 = [7,14,16,17,19,21,27,35,39,42,45,48,49,53,58,60,68,72,74,80] #窗口5
group4 = [2,5,18,19,24,52,53,60,72,74] #请用实际数字替换

group5=[2,7,10,13,28,29,34,37,38,44,48,49,50,52,57,59,63,65,72] #上一期中奖结果

# 找出前三组都存在的数字
common_numbers = set(group1) & set(group2) & set(group3)
print("Common numbers in first three groups: ", common_numbers)

# 找出0到80中没有在四组里面的数字
all_numbers = set(range(81)) # 创建一个包含0到80的集合
numbers_in_groups = set(group1 + group2 + group3 + group4) # 创建一个包含四组所有数字的集合
missing_numbers = all_numbers - numbers_in_groups
print("Numbers not in any group: ", missing_numbers)
filter_number = missing_numbers-set(group5)
print("filter_number: ", filter_number)

same_numbers4 = set(group3) & set(group1)
same_numbers5 = set(group3) & set(group2)
same_numbers6 = set(group1) & set(group2)

print("Group 3 and group1 same numbers: ", same_numbers4)
print("Group 3 and group2 same numbers: ", same_numbers5)
print("Group 1 and group2 same numbers: ", same_numbers6)
