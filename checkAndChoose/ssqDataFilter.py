from collections import Counter, defaultdict

input_str = """3,25115,02,03,08,19,24,30,02
4,25114,01,20,21,25,26,27,10
5,25113,08,10,13,15,24,31,16
6,25112,03,09,11,13,20,32,02
7,25111,09,14,18,28,31,33,12
8,25110,01,05,11,14,16,19,08
9,25109,05,06,09,17,18,31,03"""
def remove_and_intersect(first_array, *other_arrays):
    """
    从其他数组中移除与第一数组相同的值，然后计算两两交集
    """
    # 第一步：从其他数组中移除与第一数组相同的值
    filtered_arrays = []
    first_set = set(first_array)

    for array in other_arrays:
        # 过滤掉与第一数组相同的元素
        filtered = [item for item in array if item not in first_set]
        filtered_arrays.append(filtered)

    # 第二步：计算两两交集
    intersections = []
    for i in range(len(filtered_arrays)):
        for j in range(i + 1, len(filtered_arrays)):
            set1 = set(filtered_arrays[i])
            set2 = set(filtered_arrays[j])
            intersection = list(set1 & set2)
            intersections.append({
                'arrays': (i, j),
                'intersection': intersection
            })

    return {
        'filtered_arrays': filtered_arrays,
        'intersections': intersections
    }




# 分割各组字符串并处理所有组（去除前两个元素）
groups_str = input_str.split()
processed_groups = []
for s in groups_str:
    nums = list(map(int, s.split(',')))
    # 去除前两个元素和最后一个元素
    processed_group = nums[2:-1] if len(nums) >= 3 else []
    processed_groups.append(set(processed_group))

# 收集所有数组的数字（用于整体统计）
all_numbers = []
for s in groups_str:
    nums = list(map(int, s.split(',')))
    processed_group = nums[2:] if len(nums) >= 2 else []
    all_numbers.extend(processed_group)

# ==============================================
# 1. 整体数字出现次数统计（按次数分组）
# ==============================================
# 统计数字出现次数
count_all = Counter(all_numbers)

# 构建次数到数字数组的映射
frequency_map_all = defaultdict(list)
for num, freq in count_all.items():
    frequency_map_all[freq].append(num)

# 排序处理：次数降序，数字升序
sorted_frequencies_all = sorted(frequency_map_all.keys(), reverse=True)
result_all = []
for freq in sorted_frequencies_all:
    numbers = sorted(frequency_map_all[freq])
    result_all.append(f"{freq}次: {numbers}")

# 格式化输出
print("=== 所有数组数字出现次数统计（按次数分组） ===")
print("按出现次数分组的数字数组:")
for line in result_all:
    print(line)
print()

# ==============================================
# 2. 交集结果及交集数字统计
# ==============================================
# 提取处理后的第一组和其他组
first_group = processed_groups[0]
other_groups = processed_groups[1:]

# 计算交集并收集所有交集中的数字
all_intersection_numbers = []
intersection_results = []
for i, group in enumerate(other_groups, start=1):
    intersection = first_group & group
    sorted_intersection = sorted(intersection)
    intersection_results.append(f"第{i}组与第一组的交集: {sorted_intersection}")
    all_intersection_numbers.extend(sorted_intersection)

# 打印交集结果
print("=== 所有组去除前两数后的交集结果 ===")
for line in intersection_results:
    print(line)

# ==============================================
# 3. 交集中数字出现次数统计（按次数分组）
# ==============================================
# 统计交集中数字出现次数
count_inter = Counter(all_intersection_numbers)

# 构建次数到数字数组的映射
frequency_map_inter = defaultdict(list)
for num, freq in count_inter.items():
    frequency_map_inter[freq].append(num)

# 排序处理：次数降序，数字升序
sorted_frequencies_inter = sorted(frequency_map_inter.keys(), reverse=True)
result_inter = []
for freq in sorted_frequencies_inter:
    numbers = sorted(frequency_map_inter[freq])
    result_inter.append(f"{freq}次: {numbers}")

# 格式化输出
print("\n=== 交集中数字出现次数统计（按次数分组） ===")
print("按出现次数分组的数字数组:")
for line in result_inter:
    print(line)
result = remove_and_intersect(first_group,  *other_groups)
print("过滤后的数组:", result['filtered_arrays'])
print("两两交集:", result['intersections'])