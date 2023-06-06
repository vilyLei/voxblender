import bpy
import math
import time

# 获取命令行参数
obj_file = "D:/dev/webProj/voxblender/modules/box03.obj"
output_file = "D:/dev/webProj/voxblender/renderingImg/rendering03.png"

print("bpy.data.objects: ", bpy.data.objects)
print("lsit(bpy.data.objects): ", list(bpy.data.objects))

light = bpy.data.objects["Light"]
print("light: ", light)
print("light.type: ", light.type)
print("list(bpy.data.lights): ", list(bpy.data.lights))
light = bpy.data.lights["Light"]
print("light.type: ", light.type)
light.energy = 1000
light.color = (1.0, 0.0, 0.0)

cube01 = bpy.data.objects["Cube"]
if cube01:
    bpy.data.objects.remove(cube01)
else:
    print("has not the defaukt Cube.")

print("###  ###  ###  ###  ###")
# 加载OBJ模型
imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
obj_object = bpy.context.selected_objects[0]
print("obj_object: ", obj_object)
for item in bpy.context.selected_objects:
    item.scale = (1.0, 3.0, 1.0)

# 设置渲染引擎
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# 设置输出路径和文件格式
bpy.context.scene.render.filepath = output_file
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 512 #perhaps set resolution in code
bpy.context.scene.render.resolution_y = 512

# 等待1秒钟
time.sleep(0.5)

# 渲染并保存图片
bpy.ops.render.render(write_still=True)

# D:\programs\blender\blender.exe -b -P  .\loadAndRendering_default.py