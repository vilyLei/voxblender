#!/usr/bin/python3
import functools
import time
abc = 11
ab = 12
ac = abc + ab
print("ac = ",ac)

def add(a,b):
    return a + b

ac3 = add(13, 15)
print("ac3 = ",ac3)
def add1(a, b):
    return a * a + b + 1

ac4 = add1(13, 15)
print("ac4 = ",ac4)
ac4 = add1(3, 5)
print("ac4 = ",ac4)

# print("hi, Geilo, ...")
def compare(a, b):
    if a < b:
        return -1
    elif a > b:
        return 1
    return 0
    #
list01 = []

total = 65536 << 6
# total = 16
# list01 = [0] * total

print("A len(list01): ", len(list01))
startTime = time.time()
printFlag = total <= 16

if len(list01) < 2:
    for i in range(0, total):
        list01.append(total - i - 1)
else:
    for i in range(0, total):
        list01[i] = (total - i - 1)

endTime = time.time()
print("list01 building loss time: ", (endTime - startTime) * 1000, "ms")
if printFlag:
    print("list01: ", list01)

print("list01 sorting begin ...")
startTime = time.time()
# list01.sort(reverse=False)
list01.sort(key=functools.cmp_to_key(compare))
#points.sort(key=functools.cmp_to_key(compare))
endTime = time.time()
print("list01 sort loss time: ", (endTime - startTime) * 1000, "ms")
print("B len(list01): ", len(list01))
if printFlag:
    print("list01: ", list01)
