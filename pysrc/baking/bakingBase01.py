#!/usr/bin/python
# -*- coding: UTF-8 -*-
# thanks: https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.hide_set
# thanks: https://blender.stackexchange.com/questions/191091/bake-a-texture-map-with-python
import bpy
import time
import os


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)


rootDir = "D:/dev/webdev/"
if not os.path.exists(rootDir):
    rootDir = "D:/dev/webProj/"



cube01 = bpy.data.objects["Cube"]
image_name = cube01.name + '_BakedTexture'
img = bpy.data.images.new(image_name,512,512)
# hideFlag = cube01.hide_get()
# print("hideFlag: ", hideFlag)
# cube01.hide_set(not hideFlag)
bpy.context.scene.render.bake.use_pass_direct = False
bpy.context.scene.render.bake.use_pass_indirect = False
bpy.context.scene.render.bake.use_pass_color = True
#Due to the presence of any multiple materials, it seems necessary to iterate on all the materials, and assign them a node + the image to bake.
for mat in cube01.data.materials:
    mat.use_nodes = True #Here it is assumed that the materials have been created with nodes, otherwise it would not be possible to assign a node for the Bake, so this step is a bit useless
    nodes = mat.node_tree.nodes
    texture_node = nodes.new('ShaderNodeTexImage')
    texture_node.name = 'Bake_node'
    texture_node.select = True
    nodes.active = texture_node
    texture_node.image = img #Assign the image to the node

# baking_filePath = rootDir + 'voxblender/renderingImg/baking/baking_cube_' +'diffuse'+ ".jpg"
baking_filePath = rootDir + 'voxblender/renderingImg/baking/baking_cube_' +'normal'+ ".jpg"
print("baking_filePath: ", baking_filePath)
bpy.context.view_layer.objects.active = cube01
# bpy.ops.object.bake(filepath=baking_filePath)
# bpy.ops.object.bake(type='NORMAL',filepath=baking_filePath,save_mode='EXTERNAL')
# bpy.ops.object.bake(type='NORMAL',filepath=baking_filePath)
# bpy.ops.object.bake(type='DIFFUSE', save_mode='EXTERNAL')
bpy.ops.object.bake(type='NORMAL', save_mode='EXTERNAL')
# cube01.bake(filepath=baking_filePath)
img.save_render(filepath=baking_filePath)
print("proc end.")
