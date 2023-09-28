from collections import Counter
# 假设你的数字组如下：
ckRed3 = [9,10,17,24,29,33]  # 请用实际数字替换
ckRed4 = [10,16,19,23,30,31]  # 请用实际数字替换
ckRed5 = [5,11,12,14,20,23]  # 请用实际数字替换
ckRed7 = [2,6,14,19,26,30]  # 请用实际数字替换
ckRed9 = [1,7,14,16,1,3]  # 请用实际数字替换
ckRed10 = [1,21,23,26,30,32]  # 请用实际数字替换
ckRed11 = [6,7,11,14,15,21]  # 请用实际数字替换
ckRed12 = [9,14,16,18,25,27]  # 请用实际数字替换
ckRed13 = [5,6,16,19,20,33]  # 请用实际数字替换
ckRed14 = [22,23,24,26,29,33]  # 请用实际数字替换
ckRed15 = [5,6,8,10,12,24]  # 请用实际数字替换
ckBlue3 = [15]  # 请用实际数字替换
ckBlue4 = [1]  # 请用实际数字替换
ckBlue5 = [11]  # 请用实际数字替换
ckBlue7 = [15]  # 请用实际数字替换
ckBlue9 = [16]  # 请用实际数字替换
ckBlue10 = [8]  # 请用实际数字替换
ckBlue11 = [16]  # 请用实际数字替换
ckBlue12 = [1]  # 请用实际数字替换
ckBlue13 = [16]  # 请用实际数字替换
ckBlue14 = [11]  # 请用实际数字替换
ckBlue15 = [9]  # 请用实际数字替换
rxRed=[1,9,7,13,18,22,32]
rxBlue=[4,5]
cjRed=[9,12,13,22,24,31]
cjBlue=[4]
ckRedMap = {'3':ckRed3,'4':ckRed4,'5':ckRed5,'7':ckRed7,'9':ckRed9,'10':ckRed10,'11':ckRed11,'12':ckRed12,'13':ckRed13,'14':ckRed14,'15':ckRed15}
ckBlueMap = {'3':ckBlue3,'4':ckBlue4,'5':ckBlue5,'7':ckBlue7,'9':ckBlue9,'10':ckBlue10,'11':ckBlue11,'12':ckBlue12,'13':ckBlue13,'14':ckBlue14,'15':ckBlue15}
remain_red = set(range(1, 34))
remain_blue = set(range(1, 17))
for count, numbers in ckRedMap.items():
    remain_red = remain_red-set(numbers)
    temp = set(numbers) & set(rxRed)
    print("rx_ckRed"+count, temp)
    temp = set(numbers) & set(cjRed)
    print("cj_ckRed"+count, temp)
for count, numbers in ckBlueMap.items():
    remain_blue = remain_blue-set(numbers)
    temp = set(numbers) & set(rxBlue)
    print("rx_ckBlue"+count, temp)
    temp = set(numbers) & set(rxBlue)
    print("cj_ckBlue"+count, temp)

print("remain_red:",remain_red)
temp = set(remain_red) & set(rxRed)
print("rx_remain_red:",temp)
temp = set(remain_red) & set(cjRed)
print("cj_remain_red:", temp)

print("remain_blue:",remain_blue)
temp = set(remain_blue) & set(rxBlue)
print("cj_remain_blue:", temp)
temp = set(remain_blue) & set(cjBlue)
print("rx_remain_blue:",temp)