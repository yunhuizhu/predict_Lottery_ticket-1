# 假设你的数字组如下：
group1 = [1,10,21,28,32,34,36,42,44,46,47,48,52,56,63,66,67,73,76,79]  # 请用实际数字替换
group2 = [2,3,5,6,7,12,28,34,37,42,48,49,54,61,66,67,71,73,77,80]  # 请用实际数字替换
group3 = [28,30,36,37,43,44,45,47,49,50,53,54,55,56,59,61,62,68,70,71]  # 请用实际数字替换
group4 = [2,5,18,19,24,52,53,60,72,74]  # 请用实际数字替换
final_group = [2,7,10,13,28,29,34,37,38,44,48,49,50,52,57,59,63,65,72]  # 请用实际数字替换

# 找出每组与最终组相同的数字
same_numbers1 = set(group1) & set(final_group)
same_numbers2 = set(group2) & set(final_group)
same_numbers3 = set(group3) & set(final_group)
same_numbers4 = set(group3) & set(group1)
same_numbers5 = set(group3) & set(group2)
same_numbers6 = set(group1) & set(group2)
same_numbers7 = set(group4) & set(final_group)
same_numbers8 = set(group1) & set(group4)
same_numbers9 = set(group2) & set(group4)
same_numbers10 = set(group3) & set(group4)

# 打印结果
print("Group 1 and final group same numbers: ", same_numbers1)
print("Group 2 and final group same numbers: ", same_numbers2)
print("Group 3 and final group same numbers: ", same_numbers3)
print("Group 4 and final group same numbers: ", same_numbers4)
print("Group 5 and final group same numbers: ", same_numbers5)
print("Group 6 and final group same numbers: ", same_numbers6)
print("Group 7 and final group same numbers: ", same_numbers7)
print("Group 8 and final group same numbers: ", same_numbers8)
print("Group 9 and final group same numbers: ", same_numbers9)
print("Group 10 and final group same numbers: ", same_numbers10)