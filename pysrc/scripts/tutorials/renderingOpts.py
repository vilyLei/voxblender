import bpy
import time
import math

## 创建一个场景
#scene = bpy.context.scene

## 创建一个摄像机
#bpy.ops.object.camera_add(location=(5, -5, 5))
#camera = bpy.context.object
#camera.name = "MyCamera"
#camera.data.lens = 35
#camera.rotation_euler = (1.0, 0, 0.8)

## 将摄像机设置为场景的活动摄像机
#scene.camera = camera

## 加载一个obj格式的模型
#bpy.ops.import_scene.obj(filepath="D:/dev/blender/modules/apple_01.obj")

## 稍等待一秒钟
#time.sleep(1)

## 设置输出路径和渲染格式
#scene.render.image_settings.file_format = "PNG"
#scene.render.filepath = "D:/dev/blender/renderingImg/rendering01.png"

## 渲染画面
#bpy.ops.render.render(write_still=True)

dataList = (math.pi * 63.0/180.0, 0, math.pi * 46.0/180.0)
print("dataList: ", dataList)
cube01 = bpy.data.objects["Cube"]

print("bpy.data.objects: ", list(bpy.data.objects))

#cam01 = bpy.data.objects["Camera"]
#print("cam01: ", cam01)
#print("cam01.rotation_euler: ", cam01.rotation_euler)
#print("cam01.location: ", cam01.location)
bpy.data.objects.remove(cube01)
print("remove a cube.")