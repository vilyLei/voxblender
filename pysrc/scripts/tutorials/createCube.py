import bpy
import mathutils
# 创建一个cube
bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0,0, 0), scale=(1, 1, 1))
# 获取这个cube
cube = bpy.data.objects["Cube"]
print("a cube: ", cube)
v0 = mathutils.Vector((2.0, 0.0, 0.0))
# 设置这个cube的坐标(X轴坐标为2.0,Y轴和轴为0.0), 移动这个cube
cube.location = v0