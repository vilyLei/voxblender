#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import bpy
import threading
import time
# import bmesh
# import struct

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    #print("sys.path: ", sys.path)

import rsystem
import rconfig
version = rsystem.getVersion()
print("version: ", version)

class RenderingCfg:
    name = ""
    rootPath = ""
    configPath = ""
    configObj = {}
    def __init__(self, root_path):
        self.rootPath = root_path
        #
    def parseArgvParams(self, argv):
        print("parseArgvParams() init ...")
        print("argv: ", argv)
        total = len(argv)
        if total > 0:
            configDir = argv[0]
            configDir = configDir.split("=")[1]
            print("configDir: ", configDir)
            self.configPath = configDir + "config.json"
            self.getConfigData()
        #
    def getConfigData(self):
        print("getConfigData() init ...")
        self.configObj = rconfig.getJsonObjFromFile(self.configPath)
        print("getConfigData() self.configObj: ", self.configObj)
        #

## os.path.join(file_path, inner_path

sysRenderingCfg = RenderingCfg("")
def render_progress(scene):
    # 该函数将在渲染过程中多次调用，更新进度
    # print("         $$$ Cycles Rendering Progress: ", progress)
    current_frame = scene.frame_current
    total_frames = scene.frame_end - scene.frame_start + 1
    progress = (current_frame - scene.frame_start) / total_frames
    print("         $$$ Cycles Rendering Progress: ", progress)
    
def loadAObjMesh(obj_file):
    # 加载OBJ模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
    obj_object = bpy.context.selected_objects[0]
    # obj_object.scale = (0.1,0.1,0.1)
    print("obj_object: ", obj_object)
    #
def loadAObjMeshFromCfg():    
    cfgJson = sysRenderingCfg.configObj
    if "resource" in cfgJson:
        res = cfgJson["resource"]
        modelUrls = res["models"]
        url = modelUrls[0]
        print("model url: ", url)
        loadAObjMesh(url)
        return True
    else:
        print("has not mesh data ...")
    return False
    #
# call by a thread
def start_render():
    bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)
    #
def renderingCurrSceneToImg():
    
    # rootDir = "D:/dev/webProj/"
    rootDir = "D:/dev/webdev/"
    # 渲染进度回调函数的设置
    bpy.app.handlers.render_write.append(render_progress)

    renderer = bpy.context.scene.render

    # 获取Cycles渲染设备的首选项
    cycles_preferences = bpy.context.preferences.addons['cycles'].preferences
    # 启用GPU渲染
    cycles_preferences.compute_device_type = 'CUDA'  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    # 创建一个设备集合，包括所有可用的GPU设备
    devices = cycles_preferences.get_devices()
    print(">>> devices: ", devices)
    # 激活所有可用的GPU设备
    # for device in devices:
    #     if device.type == 'CUDA':  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    #         device.use = True
    # 设置设备类型为GPU
    bpy.context.scene.cycles.device = 'GPU'

    # bpy.data.scenes["Scene"].cycles.samples = VALUE

    rimg_resolution  = 4096
    # renderer.engine = 'BLENDER_EEVEE'
    renderer.engine = 'CYCLES'
    renderer.image_settings.file_format='PNG'
    renderer.filepath = rootDir + "voxblender/renderingImg/renderingFromConfig.png"
    renderer.resolution_x = rimg_resolution
    renderer.resolution_y = rimg_resolution
    bpy.context.scene.cycles.samples = 64
    # bpy.ops.render.render(write_still=True)
    bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)

    # async call rendering process    
    # render_thread = threading.Thread(target=start_render, daemon=True)
    # render_thread.start()
    # render_thread.join()
    

    #
def clearScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
################################################################################

def rtaskRun():

    clearScene()
    
    # cfgJson = sysRenderingCfg.configObj
    # print("isinstance(cfgJson, dict): ", isinstance(cfgJson, dict))
    # print('"resource" in cfgJson: ', "resource" in cfgJson)

    loadMeshFromCfgFlag = loadAObjMeshFromCfg()
    print("loadMeshFromCfgFlag: ", loadMeshFromCfgFlag)
    if loadMeshFromCfgFlag:
        renderingCurrSceneToImg()
    else:
        print("non-rendering ...")

    print("rendering proc end ...")

if __name__ == "__main__":
    argv = sys.argv
    print("argv: \n", argv)
    if argv.index("--") > 0:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    print("rendering task init ...")
    sysRenderingCfg.parseArgvParams(argv)
    rtaskRun()

# D:\programs\blender\blender.exe -b -P .\renderingFromConfig.py -- dir=./assets/