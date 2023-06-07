import bpy
import struct
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)


def toFloat32List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//4
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/4)+'f',dataStr)
    data = struct.unpack(segLen*'f',dataStr)
    return data
###
def toUint16List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//2
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/2)+'f',dataStr)
    data = struct.unpack(segLen*'H',dataStr)
    return data
###
def toUint32List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//4
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/4)+'I',dataStr)
    data = struct.unpack(segLen*'I',dataStr)
    return data

################################
file_vs = open('D:/dev/webProj/voxblender/models/geom01_vs.bin','rb')
dataStr_vs = file_vs.read()
data_vs = toFloat32List(dataStr_vs)
print("data_vs:\n", data_vs)
file_ivs = open('D:/dev/webProj/voxblender/models/geom01_ivs.bin','rb')
dataStr_ivs = file_ivs.read()
data_ivs = toUint16List(dataStr_ivs)
print("data_ivs:\n", data_ivs)


# 创建一个新的立方体对象
new_mesh = bpy.data.meshes.new('new_mesh')

def toTuplesByStep3(datals):
    ds = tuple(datals)
    n = 3
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds

#vs = [0, -15, 0, 0, -15, 10, 8.6, -15, -5, -8.6, -15, -5, 0, -15, 10, 8.6, -15, -5, -8.6, -15, -5, 0, 15, 0, 0, 15, 0, 0, 15, 0]
#ivs = [0, 2, 1, 0, 3, 2, 0, 1, 3, 5, 8, 4, 6, 9, 5, 4, 7, 6]

vs = list(data_vs)
ivs = list(data_ivs)

vsLen = len(vs)
for i in range(0, vsLen):
    vs[i] *= 0.1

vertices = toTuplesByStep3(vs)
faces = toTuplesByStep3(ivs)
print("vertices: ", vertices)
print("faces: ", faces)

#vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0)]
#faces = [(0, 1, 2)]
#vertices = [(0, -15, 0), (0, -15, 10), (8.6, -15, -5), (-8.6, -15, -5), (0, -15, 10), (8.6, -15, -5), (-8.6, -15, -5), (0, 15, 0), (0, 15, 0), (0, 15, 0)]
#faces = [(0, 2, 1), (0, 3, 2), (0, 1, 3), (5, 8, 4), (6, 9, 5), (4, 7, 6)]
# 使用顶点和面创建立方体网格
# from_pydata(vertices, edges, faces)
new_mesh.from_pydata(vertices, [], faces)
new_mesh.update()

# make object from mesh
new_object = bpy.data.objects.new('new_object', new_mesh)
# new_object.scale = (2.0,2.0,2.0)
# make collection
new_collection = bpy.data.collections.new('new_collection')
bpy.context.scene.collection.children.link(new_collection)
# add object to scene collection
new_collection.objects.link(new_object)
#resultP = list(lsa[i:i + n] for i in range(0, len(lsa), n))
#tupleb = (0,1,2,3,4,5,6,7,8)
#resultP = tuple(tupleb[i:i + n] for i in range(0, len(tupleb), n))

# uv_layer = new_object.data.uv_layers.active
# print("uv_layer: ", uv_layer)
# # 遍历 UV 数据
# for loop in new_object.data.loops:
#     uv_coords = uv_layer.data[loop.index].uv
#     print("UV coordinates for loop %d: (%f, %f)" % (loop.index, uv_coords[0], uv_coords[1]))

print("proc end.")