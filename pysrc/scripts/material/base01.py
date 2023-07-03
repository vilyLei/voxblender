#!/usr/bin/python
# -*- coding: UTF-8 -*-
# thanks: https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.hide_set

import bpy
print("---------------------------------------")
cube01 = bpy.data.objects["Cube"]
# hideFlag = cube01.hide_get()
# print("hideFlag: ", hideFlag)
# cube01.hide_set(not hideFlag)
# bpy.context.object.active_material
material0 = cube01.active_material
print("material0: ", material0)
print("material0.diffuse_color: ", material0.diffuse_color)
material0.diffuse_color = (0.5,1,0, 1.0)
print("material0.diffuse_color: ", list(material0.diffuse_color))
# for key, obj in enumerate(material0):
#    print("key: ", key, obj)
# material0 = bpy.data.materials.new("VertCol")
# material0.use_nodes = True
material0.use_nodes = True
node_tree = material0.node_tree
nodes = node_tree.nodes
bsdf = nodes.get("Principled BSDF") 
for i, o in enumerate(bsdf.inputs):
    print(">>>: ", i, o.name)

print("")
baseColor = bsdf.inputs['Base Color']
print("$$$, baseColor.default_value: ", list(baseColor.default_value))
baseColor.default_value = (0.7,0.0,0.7, 1.0)
specular = bsdf.inputs['Specular']
specular.default_value = 0.81
print("$$$, specular.default_value: ", specular.default_value)
roughness = bsdf.inputs['Roughness']
roughness.default_value = 0.81
print("$$$, roughness.default_value: ", roughness.default_value)

# bpy.data.materials['Material'] = newmat
# bpy.data.materials['Material'].node_tree.nodes["Principled BSDF"] = bsdf