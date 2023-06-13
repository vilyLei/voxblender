#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import bpy
import time
from bpy import context
# from bpy_extras import object_utils

now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

print("scaleObjectsToFitSize sys init ...")
print("sys init ...")

print("sys.path: ", sys.path)
# 下面这一行代码用于在Scripting窗口中运行pythion脚本代码引入自定义module
dirStr = r"D:/dev/webProj/voxblender/pysrc/scripts/tutorials"
if not (dirStr in sys.path):
    sys.path += [dirStr]
else:
    print("path include this dir ...")

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
# dir = os.path.dirname(bpy.data.filepath)
# if not dir in sys.path:
#     sys.path.append(dir )
    #print(sys.path)
# import boundsUtils
import meshObjScaleUtils


def objsFitToCamera():
    # Select objects that will be rendered
    for obj in context.scene.objects:
        obj.select_set(False)
    for obj in context.visible_objects:
        if not (obj.hide_get() or obj.hide_render):
            obj.select_set(True)
    #
    print("objsFitToCamera ops ...")
    bpy.ops.view3d.camera_to_view_selected()
    #

sceneObjects = bpy.data.objects

# dict for mesh:object[]
mesh_objects = {}
mesh_obj_names = []

# create dict with meshes
for m in bpy.data.meshes:
    mesh_objects[m.name] = []
# attach objects to dict keys
for o in bpy.context.scene.objects:
    # only for meshes
    if o.type == 'MESH':
        # if this mesh exists in the dict
        if o.data.name in mesh_objects:
            # object name mapped to mesh
            mesh_obj_names.append(o.data.name)

# meshes = set(o.data for o in scene.objects if o.type == 'MESH')
print("mesh_obj_names: ", mesh_obj_names)
print("mesh_objects: ", mesh_objects)

def showBoundBoxInfo(meshObjNames, sceneObjects):
    print("showBoundBoxInfo() init ...")
    meshObjs = []
    for ns in meshObjNames:
        meshObjs.append(sceneObjects[ns])
        #
    for obj in meshObjs:
        # print("mesh obj: ", obj)
        print("mesh obj.bound_box: ", obj.bound_box[0], obj.bound_box[1], obj.bound_box[2])
        for v in obj.bound_box:
            print("     v: ", list(v))

showBoundBoxInfo(mesh_obj_names, sceneObjects)
boundsData = meshObjScaleUtils.getObjsBounds(mesh_obj_names, sceneObjects)
print("boundsData: ", boundsData)
scaleFlag = meshObjScaleUtils.uniformScaleObjs((2.0, 2.0, 2.0), mesh_obj_names, sceneObjects)

objsFitToCamera()

print("scaleObjectsToFitSize sys end ...")