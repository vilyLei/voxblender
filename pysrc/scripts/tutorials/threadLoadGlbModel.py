#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import bpy
import threading
import time
from bpy import context
import os

rootDir = "D:/dev/webdev/"
if not os.path.exists(rootDir):
    rootDir = "D:/dev/webProj/"


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

print("sys.path: ", sys.path)
# 下面这一行代码用于在Scripting窗口中运行pythion脚本代码引入自定义module
dirStr = r"D:/dev/webProj/voxblender/pysrc/scripts/tutorials"
if not (dirStr in sys.path):
    sys.path += [dirStr]
else:
    print("path include this dir ...")

import meshObjScaleUtils

def loadAGlbMesh(glb_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    # print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
    # glb_object = bpy.context.selected_objects[0]
    # glb_object.scale = (0.01,0.01,0.01)
    # print("glb_object: ", glb_object)
    # Check if the model was loaded successfully

    # loaded_objects = bpy.context.selected_objects
    # if not loaded_objects:
    #     print("Error: Failed to load the GLB model.")
    # else:
    #     print("GLB model loaded successfully.")
    #     for obj in loaded_objects:
    #         print(f"Loaded object: {obj.name}")
    #
def clearScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    #
def render_scene(scene):
    
    # 渲染进度回调函数的设置
    # bpy.app.handlers.render_write.append(on_render_progress)

    # renderer = scene.render

    # # 获取Cycles渲染设备的首选项
    # cycles_preferences = bpy.context.preferences.addons['cycles'].preferences
    # # 启用GPU渲染
    # cycles_preferences.compute_device_type = 'CUDA'  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    # # 创建一个设备集合，包括所有可用的GPU设备
    # devices = cycles_preferences.get_devices()
    # print(">>> devices: ", devices)
    # # 激活所有可用的GPU设备
    # # for device in devices:
    # #     if device.type == 'CUDA':  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    # #         device.use = True
    # # 设置设备类型为GPU
    # scene.cycles.device = 'GPU'

    # rimg_resolution  = 4096
    # # renderer.engine = 'BLENDER_EEVEE'
    # renderer.engine = 'CYCLES'
    # renderer.image_settings.file_format='PNG'
    # renderer.filepath = rootDir + "voxblender/renderingImg/multiThrRenderBlenderFile.png"
    # renderer.resolution_x = rimg_resolution
    # renderer.resolution_y = rimg_resolution
    # bpy.context.scene.cycles.samples = 64
    # bpy.ops.render.render(write_still=True)
    #
    clearScene()
    modelUrl = rootDir + "voxblender/models/apple01.glb"
    # modelUrl = rootDir + "voxblender/models/model01.glb"
    modelUrl = rootDir + "voxblender/models/model03.glb"
    loadAGlbMesh(modelUrl)
    
    time.sleep(1.5)
    print("render_scene sys end ...")
################################################################################
print("threadTest sys begin ...")
scene = bpy.context.scene
thread = threading.Thread(target=render_scene, args=(scene, ))
# thread = threading.Thread(target=render_scene, args=(on_render_progress))
thread.start()

def sceneObjsFitToCamera():
    # Select objects that will be rendered
    for obj in context.scene.objects:
        obj.select_set(False)
    for obj in context.visible_objects:
        if not (obj.hide_get() or obj.hide_render):
            obj.select_set(True)
    #
    print("sceneObjsFitToCamera ops ...")
    bpy.ops.view3d.camera_to_view_selected()
    #
def testMeshObjStatus():
    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
        mesh_objectDict[m.name] = []
    
    sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:                
                print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)
                ds = obj.dimensions
                sizeValue += ds[0]
                sizeValue += ds[1]
                sizeValue += ds[2]
    #
    print("testMeshObjStatus(), sizeValue: ", sizeValue)
    if sizeValue > 0.001:
        return True
    else:
        return False


while thread.is_alive():
    print("### main thread waiting ...")
    flag = testMeshObjStatus()
    time.sleep(0.5)
    if flag:
        print("enter next step job ...")
        break
    #
#########################################################
#########################################################
# sceneObjects = bpy.data.objects

# # dict for mesh:object[]
# mesh_objects = {}
# mesh_obj_names = []

# # create dict with meshes
# for m in bpy.data.meshes:
#     mesh_objects[m.name] = []
# # attach objects to dict keys
# for o in bpy.context.scene.objects:
#     # only for meshes
#     if o.type == 'MESH':
#         # if this mesh exists in the dict
#         if o.data.name in mesh_objects:
#             # object name mapped to mesh
#             mesh_obj_names.append(o.data.name)
# ###
# boundsData = meshObjScaleUtils.getObjsBounds(mesh_obj_names, sceneObjects)
boundsData = meshObjScaleUtils.getSceneObjsBounds()
print("boundsData: ", boundsData)
scaleFlag = meshObjScaleUtils.uniformScaleSceneObjs((2.0, 2.0, 2.0))
sceneObjsFitToCamera()
print("threadTest sys end ...")