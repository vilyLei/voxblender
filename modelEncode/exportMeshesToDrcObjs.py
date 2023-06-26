#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
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
                # print("setting false.")
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
                filePath = savingDir + "export_" + str(index) + ".obj"
                index += 1
                bpy.ops.export_scene.obj(filepath=filePath, use_selection = True, use_materials=False, use_triangles=True)
                # bpy.ops.export_scene.obj(filepath=filePath, use_selection = True)
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


encoderPath = "draco_encoder.exe"
modelFilePath = "export_0.obj"

def exportObjs():
    global modelFilePath
    clearAllMeshesInScene()
    modelFilePath = modelFilePath.replace("\\","/")
    modelFilePath = modelFilePath.replace("//","/")
    index = modelFilePath.rindex("/")
    fileDir = modelFilePath[0:index+1] + "dracoObj/"
    print("exportMeshesToDrcObjs::exportObjs(), modelFilePath: ", modelFilePath)
    print("exportMeshesToDrcObjs::exportObjs(), fileDir: ", fileDir)
    # return
    loadModelWithUrl(modelFilePath)

    # scaleFlag = uniformScaleSceneObjs((2.0, 2.0, 2.0))
    print("#### ### #### ### ### ### ### ### ### ### ###")
    # getSceneObjsBounds()

    # blend_file_path = bpy.data.filepath
    # directory = os.path.dirname(blend_file_path)
    # target_file = rootDir + 'voxblender/private/obj/scene01/export_test01.obj'
    # bpy.ops.export_scene.obj(filepath=target_file)
    
    exportAMeshPerObj( fileDir )

def encodeStart():
    global encoderPath
    print("encodeStart() init ...")
    ###
if __name__ == "__main__":
    argv = sys.argv
    # print("argv: \n", argv)
    print("exportMeshesToDrcObjs init ...")
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        # print("sub0 argv: \n", argv)
        if len(argv) > 0:            
            # encoderPath = argv[0].split("=")[1]
            modelFilePath = argv[0].split("=")[1]
            # sys_renderingModulePath = argv[1].split("=")[1]
            # sys_rtaskDir = argv[2].split("=")[1]
            exportObjs()
            encodeStart()
            
    else:
        argv = []
    # ### for test
    # renderingStart()
    # if r_progress >= 100:
    #     updateRenderStatus()
    print("####### exportMeshesToDrcObjs end ...")

# D:\programs\blender\blender.exe -b -P .\exportMeshesToDrcObjs.py -- modelFilePath=scene01\scene01.fbx