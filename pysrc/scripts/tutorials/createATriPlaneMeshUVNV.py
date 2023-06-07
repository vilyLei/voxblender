import bpy
import time
import bmesh


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

# 创建一个新的立方体对象
new_mesh = bpy.data.meshes.new('new_mesh')

vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0)]
normals = [(0, 1, 0), (0, 1, 0), (0, 1, 0)]
faces = [(0, 1, 2)]

# vertices = [(0, -15, 0), (0, -15, 10), (8.6, -15, -5), (-8.6, -15, -5), (0, -15, 10), (8.6, -15, -5), (-8.6, -15, -5), (0, 15, 0), (0, 15, 0), (0, 15, 0)]
# faces = [(0, 2, 1), (0, 3, 2), (0, 1, 3), (5, 8, 4), (6, 9, 5), (4, 7, 6)]
# 使用顶点和面创建立方体网格
# from_pydata(vertices, edges, faces)
new_mesh.from_pydata(vertices, [], faces)

# 更新并计算法线
# new_mesh.update(calc_edges=True)
# new_mesh.calc_normals()


# obj = bpy.context.active_object
# bm = bmesh.from_edit_mesh(obj.data)

# 创建UV映射
# uv_layer_name = "UVMap"
bm = bmesh.new()
bm.from_mesh(new_mesh)

bm.faces.ensure_lookup_table()

# 创建UV层
uv_layer = bm.loops.layers.uv.verify()

# 分配UV坐标
uv_coords = [
    (0, 0),
    (1, 0),
    (1, 1),
]
# 这段注释掉的代码也是对的
# for face in bm.faces:
#     for loop, uv_coord in zip(face.loops, uv_coords):
#         print("uv_coord: ", uv_coord)
#         print("loop[uv_layer].uv: ", loop[uv_layer].uv)
#         loop[uv_layer].uv = uv_coord

# uv_coords2 = [
#     [
#     (0, 0),
#     (1, 0),
#     (1, 1),
#     ]
# ]
# for i, face in enumerate(bm.faces):
#     for j, loop in enumerate(face.loops):
#         loop[uv_layer].uv = uv_coords2[i][j]
# #增加新顶点
# for v in vertices:
#     bm.verts.new(v)
# 添加法线
for vert, normal in zip(bm.verts, normals):
    vert.normal = normal
    print("normal: ", normal)

uv_coords = [
    (0, 0),
    (0.8, 0),
    (0.8, 0.8),
]
for face in bm.faces:
    for loop in face.loops:
        loop_uv = loop[uv_layer]
        vert_index = loop.vert.index
        loop_uv.uv = uv_coords[vert_index]
    # face[normal_layer].split_normals = normals[face.index]
    print("face: ", face)

bm.normal_update()

# 更新Mesh对象
bm.to_mesh(new_mesh)
bm.free()

new_mesh.calc_normals()
new_mesh.update()

# make object from mesh
new_object = bpy.data.objects.new('new_object', new_mesh)
# make collection
new_collection = bpy.data.collections.new('new_collection')
bpy.context.scene.collection.children.link(new_collection)
# add object to scene collection
new_collection.objects.link(new_object)
#resultP = list(lsa[i:i + n] for i in range(0, len(lsa), n))
#tupleb = (0,1,2,3,4,5,6,7,8)
#resultP = tuple(tupleb[i:i + n] for i in range(0, len(tupleb), n))


# uv_coords3 = [
#     (0, 0),
#     (0.5, 0),
#     (0.5, 0.5),
# ]
# uv_i = 0
# uv_layer = new_object.data.uv_layers.active
# # 遍历 UV 数据
# for loop in new_object.data.loops:
#     print("uv_layer.data[loop.index]: ", uv_layer.data[loop.index])
#     uv_coords = uv_layer.data[loop.index].uv
#     print("UV coordinates for loop %d: (%f, %f)" % (loop.index, uv_coords[0], uv_coords[1]))
#     # uv_layer.data[loop.index].uv = (0.0, 0.0)
#     uv_layer.data[loop.index].uv = uv_coords3[uv_i]
#     uv_i += 1

vertex_normals = new_object.data.vertex_normals
# 遍历每个顶点和其法线
for i, vertex in enumerate(new_object.data.vertices):
    normal = vertex_normals[i]
    print("vtx normal: ", normal.vector)
print("proc end ...")