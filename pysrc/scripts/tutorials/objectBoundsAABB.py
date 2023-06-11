#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://docs.blender.org/api/current/bpy.types.Object.html
# select a object in object mode first
import bpy
from mathutils import Vector

oj  = bpy.context.object
box = oj.bound_box

print("AABB box: ", box)
box_vt0 = box[0]
print("box_vt0: ", box_vt0)
print("box_vt0[0]: ", box_vt0[0])
# Local Space
#for el in box:
#    for v in el:
#        print(v)

print("--- ---")

# World Space
p = [oj.matrix_world @ Vector(corner) for corner in box]
print(p)