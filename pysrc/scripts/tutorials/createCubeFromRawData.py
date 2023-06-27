import bpy
import bmesh
import struct



def toTuplesByStepN(datals, stepN = 4):
    ds = tuple(datals)
    rds = tuple(ds[i:i + stepN] for i in range(0, len(ds), stepN))
    return rds

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


def clearAllMeshesInScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    #
def clearRawIScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
clearAllMeshesInScene()
################################
rootDir = "D:/dev/webProj/"
#rootDir = "D:/dev/webdev/"



file_vs = open(rootDir + 'voxblender/models/verticesBox.bin','rb')
dataStr_vs = file_vs.read()
data_vs = list(toTuplesByStepN(toFloat32List(dataStr_vs), 3))
print("data_vs:\n", data_vs)
file_ivs = open(rootDir + 'voxblender/models/indicesBox.bin','rb')
dataStr_ivs = file_ivs.read()
data_ivs = list(toTuplesByStepN(toUint16List(dataStr_ivs), 3))
print("data_ivs:\n", data_ivs)

file_uvs = open(rootDir + 'voxblender/models/uvBox.bin','rb')
dataStr_uvs = file_uvs.read()
data_uvs = list(toTuplesByStepN(toFloat32List(dataStr_uvs), 2))
print("data_uvs:\n", data_uvs)


file_nvs = open(rootDir + 'voxblender/models/normalBox.bin','rb')
dataStr_nvs = file_nvs.read()
data_nvs = list(toTuplesByStepN(toFloat32List(dataStr_nvs), 3))
print("data_nvs:\n", data_nvs)

# 顶点数据
vertices = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (1, 1, 0), (1, 0, 1), (0, 1, 1),
    (1, 1, 1), (0, 0, 0)
]

# 面数据
faces = [
    (0, 1, 3), (0, 3, 4), (7, 6, 5),
    (7, 5, 2), (0, 4, 5), (0, 5, 1),
    (1, 5, 6), (1, 6, 3), (3, 6, 7),
    (3, 7, 4), (4, 7, 2), (4, 2, 5)
]

# 法线数据
normals = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1),
    (-1, 0, 0), (0, -1, 0), (0, 0, -1)
]

# UV 数据
uv_coords = [
    (1, 0), (0, 1), (0, 0),
    (1, 1), (1, 1), (0, 1),
    (1, 1), (0, 0)
]

vertices = data_vs
faces = data_ivs
normals = data_nvs
uv_coords = data_uvs

# 创建mesh和物体
mesh = bpy.data.meshes.new("Cube")
robjEntity = bpy.data.objects.new("Cube", mesh)

# 将物体添加到场景
scene = bpy.context.scene
scene.collection.objects.link(robjEntity)

# 创建bmesh对象
bm = bmesh.new()
bm.from_mesh(mesh)

# bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
# bm.faces.ensure_lookup_table()

# 添加顶点
# print("vertices: ", vertices)
for v in vertices:
    # print("v: ", v)
    bm.verts.new(v)

bm.verts.ensure_lookup_table()
print("len(faces): ", len(faces))
# 添加面
for k in range(0, len(faces)):
    bm.faces.new([bm.verts[i] for i in faces[k]])
# bm.faces.new([bm.verts[i] for i in faces[0]])
# bm.faces.new([bm.verts[i] for i in faces[1]])
# ... 在这里为其他面重复这个过程

# 添加法线
for vert, normal in zip(bm.verts, normals):
    vert.normal = normal

# 添加UV坐标
uv_layer = bm.loops.layers.uv.verify()
for f, uv in zip(bm.faces, uv_coords):
    for loop in f.loops:
        loop[uv_layer].uv = uv

# 更新mesh数据
bm.to_mesh(mesh)
bm.free()

# 更新mesh的法线
mesh.calc_normals()

robjEntity.scale = (0.1,0.1, 0.1)

# 添加UV纹理到物体
# mesh.uv_textures.new("UVMap")

vertex_normals = robjEntity.data.vertex_normals
# 遍历每个顶点和其法线
for i, vertex in enumerate(robjEntity.data.vertices):
    normal = vertex_normals[i]
    print("vtx normal: ", normal.vector)
print("proc end ...")