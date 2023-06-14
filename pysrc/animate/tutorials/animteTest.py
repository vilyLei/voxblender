#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import bpy
import threading
import time
from bpy import context


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

# 下面这一行代码用于在Scripting窗口中运行pythion脚本代码引入自定义module
dirStr = r"D:/dev/webProj/voxblender/pysrc/scripts/tutorials"
if not (dirStr in sys.path):
    sys.path += [dirStr]
else:
    print("path include this dir ...")

# import meshObjScaleUtils

def loadAGlbMesh(glb_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    #
def clearScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    #
def render_scene(scene):
    rootDir = "D:/dev/webProj/"
    # rootDir = "D:/dev/webdev/"
    
    time.sleep(1.5)
    # print("render_scene sys end ...")
################################################################################
print("threadTest sys begin ...")
scene = bpy.context.scene
thread = threading.Thread(target=render_scene, args=(scene, ))
# thread = threading.Thread(target=render_scene, args=(on_render_progress))
thread.start()

cube01 = bpy.data.objects["Cube"]
# if cube01:
#     bpy.data.objects.remove(cube01)
# else:

playing = True
playTimes = 6
while thread.is_alive() or playing:
    print("### main playTimes: ", playTimes)
    if cube01:
        pos = cube01.location
        print("pos: ", pos)
        pos.x += 0.2
        cube01.location = pos
        # bpy.context.scene.update()
        bpy.context.view_layer.update()
        #
    if playTimes < 1:
        print("enter next step job ...")
        break
    else:
        playTimes -= 1
    #
    time.sleep(0.5)
    #
#########################################################
#########################################################

print("threadTest sys end ...")