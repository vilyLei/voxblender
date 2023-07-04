#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bpy
import mathutils
from mathutils import Matrix
import time
import os


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

def getSceneObjsBounds():
    print("getObjsBounds() init ...")
    
    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
            mesh_objectDict[m.name] = []
    
    # sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                # print("getSceneObjsBounds() list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)
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
    
    # for obj in meshObjs:
    #     # print("mesh obj: ", obj)
    #     print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)        

    minV = (minx, miny, minz)
    maxV = (maxx, maxy, maxz)
    width = maxV[0] - minV[0]
    height = maxV[1] - minV[1]
    long = maxV[2] - minV[2]
    # print("minV: ", minV)
    # print("maxV: ", maxV)
    print("width: ", width)
    print("height: ", height)
    print("long: ", long)
    print("getObjsBounds() end ...")

    # for debug
    # boundsUtils.createBoundsFrameBox(minV, maxV)
    return (minV,  maxV, (width, height, long))
###
def uniformScaleSceneObjs(dstSizeV):
    print("uniformScaleSceneObjs() init ...")
    boundsData = getSceneObjsBounds()
    sizeV = boundsData[2]

    # sx = dstSizeV[0] / sizeV[0]
    # sy = dstSizeV[1] / sizeV[1]

    if sizeV[0] > 0.0001:
        sx = dstSizeV[0] / sizeV[0]
    else:
        sx = 1.0
    if sizeV[1] > 0.0001:
        sy = dstSizeV[1] / sizeV[1]
    else:
        sy = 1.0
    if sizeV[2] > 0.0001:
        sz = dstSizeV[2] / sizeV[2]
    else:
        sz = 1.0
    # 等比缩放
    sx = sy = sz = min(sx, min(sy, sz))

    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
        mesh_objectDict[m.name] = []
    
    # sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                location = obj.location
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
    print("uniformScaleSceneObjs() end ...")
    return True

def clearAllMeshesInScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    #
def clearScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
################################################################################
def loadAObjMesh(obj_file):
    # 加载OBJ模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    #    
def loadAFbxMesh(fbx_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.fbx(filepath=fbx_file)
    #
def loadAGlbMesh(glb_file):
    # 加载glb模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    #
def loadAUsdMesh(usd_file):
    # 加载usd模型
    imported_object = bpy.ops.wm.usd_import(filepath=usd_file)
    #

def loadModelWithUrl(url):
    resType = url.split('.')[1]
    resType = resType.lower()
    print("######### loadModelWithUrl(), resType: ", resType)
    if resType == "obj":
            loadAObjMesh(url)
    elif resType == "fbx":
        loadAFbxMesh(url)
    elif resType == "glb":
        loadAGlbMesh(url)
    elif resType == "usdc":
        loadAUsdMesh(url)
    elif resType == "usdz":
        loadAUsdMesh(url)
    else:
        return False
    return True
    #

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

clearAllMeshesInScene()
modelUrl = rootDir + "voxblender/models/apple02.glb"
# modelUrl = rootDir + "voxblender/models/apple01.usdc"
# modelUrl = rootDir + "voxblender/models/model01.usdz"
# modelUrl = rootDir + "voxblender/models/model01.glb"
# modelUrl = rootDir + "voxblender/models/model03.glb"
# modelUrl = rootDir + "voxblender/private/glb/xiezi-en.glb"
# modelUrl = rootDir + "voxblender/models/scene03.fbx"
# modelUrl = rootDir + "voxblender/models/scene01.fbx"
# modelUrl = rootDir + "voxblender/models/scene03.glb"
# modelUrl = rootDir + "voxblender/models/scene01.obj"
loadModelWithUrl(modelUrl)

# scaleFlag = uniformScaleSceneObjs((2.0, 2.0, 2.0))
print("#### ### #### ### ### ### ### ### ### ### ###")
# getSceneObjsBounds()

blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
# target_file = os.path.join(directory, '../../private/obj/export_test01.obj')
# target_file = rootDir + 'voxblender/private/obj/export_test01.obj'
# bpy.ops.export_scene.obj(filepath=target_file)


target_file = os.path.join(directory, "D:/dev/webProj/voxblender/renderingImg/glbToBld.blend")
bpy.ops.wm.save_as_mainfile(filepath=target_file)

print("saveModelFileToBlendFile exec finish ...")
# D:\programs\blender\blender.exe -b -P .\saveModelFileToBlendFile.py