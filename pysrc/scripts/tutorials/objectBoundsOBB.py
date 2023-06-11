#!/usr/bin/python
# -*- coding: UTF-8 -*-
# https://docs.blender.org/api/current/bpy.types.Object.html
# select a object in object mode first

# select a object in object mode first
import bpy
import numpy as np
from mathutils import Vector

oj      = bpy.context.object
verts   = [v.co for v in oj.data.vertices]

points = np.asarray(verts)
means = np.mean(points, axis=1)

cov = np.cov(points, y = None,rowvar = 0,bias = 1)

v, vect = np.linalg.eig(cov)

tvect = np.transpose(vect)
points_r = np.dot(points, np.linalg.inv(tvect))

co_min = np.min(points_r, axis=0)
co_max = np.max(points_r, axis=0)

xmin, xmax = co_min[0], co_max[0]
ymin, ymax = co_min[1], co_max[1]
zmin, zmax = co_min[2], co_max[2]

xdif = (xmax - xmin) * 0.5
ydif = (ymax - ymin) * 0.5
zdif = (zmax - zmin) * 0.5

cx = xmin + xdif
cy = ymin + ydif
cz = zmin + zdif

corners = np.array([
    [cx - xdif, cy - ydif, cz - zdif],
    [cx - xdif, cy + ydif, cz - zdif],
    [cx - xdif, cy + ydif, cz + zdif],
    [cx - xdif, cy - ydif, cz + zdif],
    [cx + xdif, cy + ydif, cz + zdif],
    [cx + xdif, cy + ydif, cz - zdif],
    [cx + xdif, cy - ydif, cz + zdif],
    [cx + xdif, cy - ydif, cz - zdif],
])

corners = np.dot(corners, tvect)
center = np.dot([cx, cy, cz], tvect)

corners = [Vector((el[0], el[1], el[2])) for el in corners]

print("local space:")
for el in corners: print(el)

print("")
print("world space:")
mat = oj.matrix_world
for el in corners: print(mat @ el)