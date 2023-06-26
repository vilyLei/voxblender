#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bpy
import mathutils
from mathutils import Matrix
import time
import os

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"
now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

def exportAMeshPerObj(savingDir):
    print("exportAMeshPerObj() init ...")
    # global rootDir

    mesh_objectDict = {}
    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
            mesh_objectDict[m.name] = []
    
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                print("setting false.")
                obj.hide_set(False)
                obj.select_set(False)
                ### ###
    ### ########################################################
    index = 0
    
    # target_file_dir = rootDir + 'voxblender/private/obj/scene01/export_test01.obj'
    # file_dir = rootDir + 'voxblender/private/obj/scene01/'
    
    context = bpy.context
    viewlayer = context.view_layer
    
    if not os.path.exists(savingDir):
        os.makedirs(savingDir)
    ########################################
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:

                # obj.hide_set(True)
                # obj.select_set(True)
                viewlayer.objects.active = obj
                obj.select_set(True)
                filePath = savingDir + "export_" + str(index) + ".ply"
                index += 1
                bpy.ops.export_mesh.ply(filepath=filePath, use_selection = True)
                obj.hide_set(False)
                obj.select_set(False)
                # break
                ### ###
    #

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
    # 加载 OBJ 模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    #
def loadAFbxMesh(fbx_file):
    # 加载 FBX 模型
    imported_object = bpy.ops.import_scene.fbx(filepath=fbx_file)
    #
def loadAGlbMesh(glb_file):
    # 加载 GLB 模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    #
def loadAUsdMesh(usd_file):
    # 加载 USD 模型
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


clearAllMeshesInScene()
modelUrl = rootDir + "voxblender/models/apple01.glb"
modelUrl = rootDir + "voxblender/models/apple01.usdc"
# modelUrl = rootDir + "voxblender/models/model01.usdz"
# modelUrl = rootDir + "voxblender/models/model01.glb"
# modelUrl = rootDir + "voxblender/models/model03.glb"
# modelUrl = rootDir + "voxblender/private/glb/xiezi-en.glb"
# modelUrl = rootDir + "voxblender/models/scene03.fbx"
modelUrl = rootDir + "voxblender/models/scene01.fbx"
# modelUrl = rootDir + "voxblender/models/scene03.glb"
# modelUrl = rootDir + "voxblender/models/scene01.obj"
loadModelWithUrl(modelUrl)

# scaleFlag = uniformScaleSceneObjs((2.0, 2.0, 2.0))
print("#### ### #### ### ### ### ### ### ### ### ###")
# getSceneObjsBounds()

# blend_file_path = bpy.data.filepath
# directory = os.path.dirname(blend_file_path)
# target_file = rootDir + 'voxblender/private/obj/scene01/export_test01.obj'
# bpy.ops.export_scene.obj(filepath=target_file)
savingDir = rootDir + 'voxblender/private/obj/scene01_ply/'
exportAMeshPerObj( savingDir )


print("exportMeshesToPlys exec finish ...")
# D:\programs\blender\blender.exe -b -P .\exportMeshesToPlys.py



# import bpy
# from pathlib import Path

# context = bpy.context
# scene = context.scene
# viewlayer = context.view_layer

# obs = [o for o in scene.objects if o.type == 'MESH']
# bpy.ops.object.select_all(action='DESELECT')    

# path = Path("/tmp")
# for ob in obs:
#     viewlayer.objects.active = ob
#     ob.select_set(True)
#     stl_path = path / f"{ob.name}.stl"
#     bpy.ops.export_mesh.stl(
#             filepath=str(stl_path),
#             use_selection=True)
#     ob.select_set(False)