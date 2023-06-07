import numpy as np
import struct

def toDoubleList(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//8
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/8)+'d',d_str)
    # 相关匹配格式和字节序请见: https://docs.python.org/zh-cn/3/library/struct.html#struct.calcsize
    data = struct.unpack(segLen*'d',dataStr)
    return data
#########
def toFloatList(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//4
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/4)+'f',d_str)
    data = struct.unpack(segLen*'f',dataStr)
    return data

def toUint16List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//2
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/2)+'H',d_str)
    data = struct.unpack(segLen*'H',dataStr)
    return data

def toUint32List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//4
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/4)+'I',d_str)
    data = struct.unpack(segLen*'I',dataStr)
    return data

file = open('../../models/geom01_vs.bin','rb')
dataStr = file.read()
data_vs = toFloatList(dataStr)
print("float data_vs:\n", data_vs)
print("\n")
file = open('../../models/geom01_ivs.bin','rb')
dataStr = file.read()
data_ivs = toUint16List(dataStr)
print("float data_ivs:\n", data_ivs)