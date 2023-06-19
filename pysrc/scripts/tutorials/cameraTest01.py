#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bpy
from mathutils import Matrix
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

# Create a new camera
# camera_data = bpy.data.cameras.new('Camera')
# camera_object = bpy.data.objects.new('Camera', camera_data)
# bpy.context.scene.collection.objects.link(camera_object)
# camera_object = bpy.data.cameras["Camera"]
camera_object = bpy.data.objects["Camera"]
print("camera_object: ", camera_object)
print("camera_object.matrix_world: ", camera_object.matrix_world)

cdvs = (-0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 5.000000476837158, 0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 5.000000476837158, 0, 0.8164965510368347, 0.5773502588272095, 5.000000476837158, -0, 0, -0, 1)
cdvs = (-0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 8, 0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 8, 0, 0.8164965510368347, 0.5773502588272095, 8, -0, 0, -0, 1)

def toTuplesByStep4(datals):
    ds = tuple(datals)
    n = 4
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds
cdvsList = toTuplesByStep4(cdvs)

cam_world_matrix = Matrix()
cam_world_matrix[0] = cdvsList[0]
cam_world_matrix[1] = cdvsList[1]
cam_world_matrix[2] = cdvsList[2]
cam_world_matrix[3] = cdvsList[3]


camera_object.matrix_world = cam_world_matrix


print("cam_world_matrix: ", cam_world_matrix)
print("cam_world_matrix[0]: ", cam_world_matrix[0])

# Set camera field of view
camera_object.data.angle = 45
camera_object.data.clip_start = 0.1
camera_object.data.clip_end = 100.0

print("proc end ...")