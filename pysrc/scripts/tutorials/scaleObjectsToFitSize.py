#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import bpy
import time
from bpy import context
import mathutils
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
# import meshObjScaleUtils


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
    print("A1 showBoundBoxInfo() init ...")
    meshObjs = []
    for ns in meshObjNames:
        meshObjs.append(sceneObjects[ns])
        #
    for obj in meshObjs:
        # print("mesh obj: ", obj)
        print("A1 mesh obj.bound_box: ", obj.bound_box[0], obj.bound_box[1], obj.bound_box[2])
        for v in obj.bound_box:
            print("     v: ", list(v))

# showBoundBoxInfo(mesh_obj_names, sceneObjects)
# boundsData = meshObjScaleUtils.getObjsBounds(mesh_obj_names, sceneObjects)
# print("boundsData: ", boundsData)
print("--- --- --- ---------------------- pp ------------------------------------------------------")
# scaleFlag = meshObjScaleUtils.uniformScaleObjs((2.0, 2.0, 2.0), mesh_obj_names, sceneObjects)


def getObjsBounds(meshObjNames, sceneObjects):
    print("B0 getObjsBounds() init ...")
    meshObjs = []
    for ns in meshObjNames:
        if sceneObjects[ns]:
            meshObjs.append(sceneObjects[ns])
        #
    
    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    for obj in meshObjs:
        # print("mesh obj: ", obj)
        print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]))
        # while obj.parent is not None:
        #     obj = obj.parent
        for v in obj.bound_box:
            v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))

            if v_world[0] < minx:
                minx = v_world[0]
            if v_world[0] > maxx:
                maxx = v_world[0]

            if v_world[1] < miny:
                miny = v_world[1]
            if v_world[1] > maxy:
                maxy = v_world[1]

            if v_world[2] < minz:
                minz = v_world[2]
            if v_world[2] > maxz:
                maxz = v_world[2]

    minV = (minx, miny, minz)
    maxV = (maxx, maxy, maxz)
    width = maxV[0] - minV[0]
    height = maxV[1] - minV[1]
    long = maxV[2] - minV[2]
    print("B1 minV: ", minV)
    print("B1 maxV: ", maxV)
    print("B1 width: ", width)
    print("B1 height: ", height)
    print("B1 long: ", long)
    print("B1 getObjsBounds() end ...")

    # for debug
    # boundsUtils.createBoundsFrameBox(minV, maxV)
    return (minV,  maxV, (width, height, long))
def uniformScaleObjs(dstSizeV, meshObjNames, sceneObjects):
    print("A0 uniformScaleObjs() init ...")
    print("A0 uniformScaleObjs() meshObjNames: ", meshObjNames)
    meshObjs = []
    for ns in meshObjNames:
        if sceneObjects[ns]:
            meshObjs.append(sceneObjects[ns])
        #
    
    boundsData = getObjsBounds(meshObjNames, sceneObjects)
    sizeV = boundsData[2]
    print("A0 uniformScaleObjs() sizeV: ", sizeV)
    sx = 1.0
    sy = 1.0
    sz = 1.0
    # sx = dstSizeV[0] / sizeV[0]
    # sy = dstSizeV[1] / sizeV[1]
    # sz = dstSizeV[2] / sizeV[2]
    
    # 等比缩放
    sx = sy = sz = min(sx, min(sy, sz))
    sx = sy = sz = 0.1
    print("A0 uniformScaleObjs() sx: ", sx)
    for obj in meshObjs:
        print("A1 uniformScaleObjs() obj.parent: ", obj.parent)
        # if obj.parent is not None:
        #     print("A1 uniformScaleObjs() obj.parent.location: ", obj.parent.location)
        #     if obj.parent.parent is not None:
        #         print("A1 uniformScaleObjs() obj.parent.parent.location: ", obj.parent.parent.location)
        # while obj.parent is not None:
        #     obj = obj.parent
            #
        location = obj.location
        print("A1 uniformScaleObjs() location: ", location)
        location[0] *= sx
        location[1] *= sy
        location[2] *= sz
        obj.location = location
        scale = obj.scale
        scale[0] *= sx
        scale[1] *= sy
        scale[2] *= sz
        obj.scale = scale
        #
    print("uniformScaleObjs() end ...")
    return True
scaleFlag = uniformScaleObjs((2.0, 2.0, 2.0), mesh_obj_names, sceneObjects)
sceneObjsFitToCamera()

print("scaleObjectsToFitSize sys end ...")