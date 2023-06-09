#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import bpy
import mathutils
import bmesh
import time
from bpy_extras import object_utils

now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

print("sys init ...")

print("sys.path: ", sys.path)
# 下面这一行代码用于在Scripting窗口中运行pythion脚本代码引入自定义module
dirStr = r"D:/dev/webProj/voxblender/pysrc/scripts/tutorials"
if not (dirStr in  sys.path):
    sys.path += [dirStr]
else:
    print("path include this dir ...")

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    #print(sys.path)
import boundsUtils
import meshObjScaleUtils


sceneObjects = bpy.data.objects
listObjs = list(bpy.data.objects)

print("listObjs: ", listObjs)


# dict for mesh:object[]
mesh_objects = {}
mesh_obj_names = []

# create dict with meshes
for m in bpy.data.meshes:
    mesh_objects[m.name] = []
    mesh_obj_names.append(m.name)
print("A mesh_obj_names: ", mesh_obj_names)
mesh_obj_names = []
# attach objects to dict keys
for o in bpy.context.scene.objects:
    # only for meshes
    if o.type == 'MESH':
        # if this mesh exists in the dict
        if o.data.name in mesh_objects:
            # object name mapped to mesh
            mesh_objects[o.data.name].append(o.name)
            mesh_obj_names.append(o.data.name)

# meshes = set(o.data for o in scene.objects if o.type == 'MESH')
print("B mesh_obj_names: ", mesh_obj_names)
print("B mesh_objects: ", mesh_objects)


boundsData = meshObjScaleUtils.getObjsBounds(mesh_obj_names, sceneObjects)
print("boundsData: ", boundsData)
scaleFlag = meshObjScaleUtils.uniformScaleObjs((2.0, 2.0, 2.0), mesh_obj_names, sceneObjects)
print("sys end ...")