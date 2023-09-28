from collections import Counter
# 假设你的数字组如下：
ckRed3 = [8,21,22,25,28,32]  # 请用实际数字替换
ckRed4 = [11,18,20,22,30,31]  # 请用实际数字替换
ckRed5 = [1,7,15,27,30,31]  # 请用实际数字替换
ckRed7 = [1,6,9,13,14,28]  # 请用实际数字替换
ckRed9 = [1,3,6,14,27,28]  # 请用实际数字替换
ckRed10 = [1,11,14,22,26,33]  # 请用实际数字替换
ckRed11 = [1,7,9,11,13,20]  # 请用实际数字替换
ckRed12 = [1,5,13,21,23,31]  # 请用实际数字替换
ckRed13 = [3,12,23,24,29,33]  # 请用实际数字替换
ckRed14 = [1,3,6,13,27,28]  # 请用实际数字替换
ckRed15 = [9,14,31,3,16,18]  # 请用实际数字替换
ckBlue3 = [10]  # 请用实际数字替换
ckBlue4 = [7]  # 请用实际数字替换
ckBlue5 = [2]  # 请用实际数字替换
ckBlue7 = [1]  # 请用实际数字替换
ckBlue9 = [10]  # 请用实际数字替换
ckBlue10 = [10]  # 请用实际数字替换
ckBlue11 = [8]  # 请用实际数字替换
ckBlue12 = [14]  # 请用实际数字替换
ckBlue13 = [9]  # 请用实际数字替换
ckBlue14 = [4]  # 请用实际数字替换
ckBlue15 = [1]  # 请用实际数字替换
rxRed=[4,10,21,26,29,31]
rxBlue=[8]
ckRedMap = {'3':ckRed3,'4':ckRed4,'5':ckRed5,'7':ckRed7,'9':ckRed9,'10':ckRed10,'11':ckRed11,'12':ckRed12,'13':ckRed13,'14':ckRed14,'15':ckRed15}
ckBlueMap = {'3':ckBlue3,'4':ckBlue4,'5':ckBlue5,'7':ckBlue7,'9':ckBlue9,'10':ckBlue10,'11':ckBlue11,'12':ckBlue12,'13':ckBlue13,'14':ckBlue14,'15':ckBlue15}
remain_red = set(range(1, 34))
remain_blue = set(range(1, 17))
for count, numbers in ckRedMap.items():
    remain_red = remain_red-set(numbers)
    temp = set(numbers) & set(rxRed)
    print("rx_ckRed"+count, temp)
for count, numbers in ckBlueMap.items():
    remain_blue = remain_blue-set(numbers)
    temp = set(numbers) & set(rxBlue)
    print("rx_ckBlue"+count, temp)
print("remain_red:",remain_red)
temp = set(remain_red) & set(rxRed)
print("rx_remain_red:",temp)
print("remain_blue:",remain_blue)
temp = set(remain_blue) & set(rxBlue)
print("rx_remain_red:",temp)