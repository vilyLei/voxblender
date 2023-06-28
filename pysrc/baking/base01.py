#!/usr/bin/python
# -*- coding: UTF-8 -*-
# thanks: https://docs.blender.org/api/current/bpy.types.Object.html#bpy.types.Object.hide_set

import bpy

cube01 = bpy.data.objects["Cube"]
hideFlag = cube01.hide_get()
print("hideFlag: ", hideFlag)
cube01.hide_set(not hideFlag)
