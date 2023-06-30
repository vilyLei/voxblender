#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bpy
import mathutils
from mathutils import Matrix
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)


def getSceneObjsBounds():
    print("getObjsBounds() init ...")
    
    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
            mesh_objectDict[m.name] = []
    
    # sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                # print("getSceneObjsBounds() list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)
                for v in obj.bound_box:
                    v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))

                    if v_world[0] < minx:
                        minx = v_world[0]
                    if v_world[0] > maxx:
                        maxx = v_world[0]

                    if v_world[1] < miny:
                        miny = v_world[1]
                    if v_world[1] > maxy:
                        maxy = v_world[1]

                    if v_world[2] < minz:
                        minz = v_world[2]
                    if v_world[2] > maxz:
                        maxz = v_world[2]
    
    # for obj in meshObjs:
    #     # print("mesh obj: ", obj)
    #     print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)        

    minV = (minx, miny, minz)
    maxV = (maxx, maxy, maxz)
    width = maxV[0] - minV[0]
    height = maxV[1] - minV[1]
    long = maxV[2] - minV[2]
    # print("minV: ", minV)
    # print("maxV: ", maxV)
    # print("width: ", width)
    # print("height: ", height)
    # print("long: ", long)
    print("getObjsBounds() end ...")

    # for debug
    # boundsUtils.createBoundsFrameBox(minV, maxV)
    return (minV,  maxV, (width, height, long))
###
def uniformScaleSceneObjs(dstSizeV):
    print("uniformScaleSceneObjs() init ...")
    boundsData = getSceneObjsBounds()
    sizeV = boundsData[2]

    # sx = dstSizeV[0] / sizeV[0]
    # sy = dstSizeV[1] / sizeV[1]

    if sizeV[0] > 0.0001:
        sx = dstSizeV[0] / sizeV[0]
    else:
        sx = 1.0
    if sizeV[1] > 0.0001:
        sy = dstSizeV[1] / sizeV[1]
    else:
        sy = 1.0
    if sizeV[2] > 0.0001:
        sz = dstSizeV[2] / sizeV[2]
    else:
        sz = 1.0
    # 等比缩放
    sx = sy = sz = min(sx, min(sy, sz))

    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
        mesh_objectDict[m.name] = []
    
    # sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                location = obj.location
                location[0] *= sx
                location[1] *= sy
                location[2] *= sz
                obj.location = location
                scale = obj.scale
                scale[0] *= sx
                scale[1] *= sy
                scale[2] *= sz
                obj.scale = scale
                #
    print("uniformScaleSceneObjs() end ...")
    return True

scaleFlag = uniformScaleSceneObjs((2.0, 2.0, 2.0))
# Create a new camera
# camera_data = bpy.data.cameras.new('Camera')
# camera_object = bpy.data.objects.new('Camera', camera_data)
# bpy.context.scene.collection.objects.link(camera_object)
# camera_object = bpy.data.cameras["Camera"]
camera_object = bpy.data.objects["Camera"]
print("camera_object: ", camera_object)
print("camera_object.matrix_world: ", camera_object.matrix_world)

cdvs = (-0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 5.000000476837158, 0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 5.000000476837158, 0, 0.8164965510368347, 0.5773502588272095, 5.000000476837158, -0, 0, -0, 1)
cdvs = (0.7071067690849304, -0.40824827551841736, 0.5773502588272095, 2.390000104904175, 0.7071067690849304, 0.40824827551841736, -0.5773502588272095, -2.390000104904175, 0, 0.8164965510368347, 0.5773502588272095, 2.390000104904175, -0, 0, -0, 1)

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


camera_object = bpy.data.objects["Camera"]
camera_object.matrix_world = cam_world_matrix


print("cam_world_matrix: ", cam_world_matrix)
print("cam_world_matrix[0]: ", cam_world_matrix[0])

# Set camera field of view
camera_object.data.lens = 50
camera_object.data.angle = 3.14159065 * 45.0/180.0
camera_object.data.clip_start = 0.1
camera_object.data.clip_end = 20.0

print("proc end ...")