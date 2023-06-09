import bpy
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

# 创建一个新的立方体对象
new_mesh = bpy.data.meshes.new('new_mesh')
# 定义立方体的顶点和面
# vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)]
# faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]

def toTuplesByStep3(datals):
    ds = tuple(datals)
    n = 3
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds

vs = [0, -15, 0, 0, -15, 10, 8.6, -15, -5, -8.6, -15, -5, 0, -15, 10, 8.6, -15, -5, -8.6, -15, -5, 0, 15, 0, 0, 15, 0, 0, 15, 0]
ivs = [0, 2, 1, 0, 3, 2, 0, 1, 3, 5, 8, 4, 6, 9, 5, 4, 7, 6]

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