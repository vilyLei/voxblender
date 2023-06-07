import bpy
import bmesh
from mathutils import Vector

# 顶点数据
vertices = [
    Vector((-1, -1, -1)),
    Vector((-1, -1, 1)),
    Vector((-1, 1, -1)),
    Vector((-1, 1, 1)),
    Vector((1, -1, -1)),
    Vector((1, -1, 1)),
    Vector((1, 1, -1)),
    Vector((1, 1, 1)),
]

# 面数据
faces = [
    (0, 1, 3, 2),
    (4, 0, 2, 6),
    (5, 4, 6, 7),
    (1, 5, 7, 3),
    (2, 3, 7, 6),
    (1, 0, 4, 5),
]

# 创建立方体的Mesh
mesh = bpy.data.meshes.new("Cube")
obj = bpy.data.objects.new("Cube", mesh)

# 将新创建的立方体对象添加到场景中
scene = bpy.context.scene
scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj

# 使用顶点和面数据创建立方体
# 错误代码
bm = bmesh.new()
for v in vertices:
    bm.verts.new(v)
bm.faces.new(bm.verts[i] for i in faces[0])
for face in faces:
    bm.faces.new(bm.verts[i] for i in face)
bm.to_mesh(mesh)
bm.free()

# 创建UV映射
uv_layer = bm.loops.layers.uv.verify()

# 为每个面添加UV坐标
uv_coords = [
    [(0, 0), (0, 1), (1, 1), (1, 0)],
] * 6

for i, face in enumerate(bm.faces):
    for j, loop in enumerate(face.loops):
        loop[uv_layer].uv = uv_coords[i][j]

# 更新Mesh，以将更改应用于立方体对象
mesh.update()