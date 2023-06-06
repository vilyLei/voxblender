import bpy
import math
import time

obj_file = "D:/dev/webProj/voxblender/modules/apple_01.obj"
output_file = "D:/dev/webProj/voxblender/renderingImg/rendering02.png"

print("bpy.data.objects: ", bpy.data.objects)
print("bpy.data.objects: ", list(bpy.data.objects))

# 删除所有默认场景中的对象
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 加载OBJ模型
bpy.ops.import_scene.obj(filepath=obj_file)
obj_object = bpy.context.selected_objects[0]
print("obj_object: ", obj_object)
if obj_object:
    obj_object.scale = (5.0, 5.0, 5.0)

# 创建摄像机
bpy.ops.object.camera_add()
camera = bpy.context.active_object

# 设置摄像机位置
camera.location = (7.3589, -6.9258, 4.9583)
camera.rotation_euler = (63.0*math.pi/180.0, 0, 46.0*math.pi/180.0)

# 设置摄像机作为场景主摄像机
bpy.context.scene.camera = camera

# 设置渲染引擎
bpy.context.scene.render.engine = 'BLENDER_EEVEE'

# 设置输出路径和文件格式
bpy.context.scene.render.filepath = output_file
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512

# 等待1秒钟
time.sleep(0.5)

# 渲染并保存图片
bpy.ops.render.render(write_still=True)