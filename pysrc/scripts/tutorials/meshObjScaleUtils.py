#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bpy
import mathutils

# 下面这一行代码用于在Scripting窗口中运行pythion脚本代码引入自定义module
# sys.path += [r"D:/dev/webProj/voxblender/pysrc/scripts/tutorials"]

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
# dir = os.path.dirname(bpy.data.filepath)
# if not dir in sys.path:
#     sys.path.append(dir )
#     #print(sys.path)

# import boundsUtils


def getObjsBounds(meshObjNames, sceneObjects):
    print("getObjsBounds() init ...")
    meshObjs = []
    for ns in meshObjNames:
        if sceneObjects[ns]:
            meshObjs.append(sceneObjects[ns])
        #
    
    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    for obj in meshObjs:
        # print("mesh obj: ", obj)
        print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]))
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

    minV = (minx, miny, minz)
    maxV = (maxx, maxy, maxz)
    width = maxV[0] - minV[0]
    height = maxV[1] - minV[1]
    long = maxV[2] - minV[2]
    print("minV: ", minV)
    print("maxV: ", maxV)
    print("width: ", width)
    print("height: ", height)
    print("long: ", long)
    print("getObjsBounds() end ...")

    # for debug
    # boundsUtils.createBoundsFrameBox(minV, maxV)
    return (minV,  maxV, (width, height, long))

def uniformScaleObjs(dstSizeV, meshObjNames, sceneObjects):
    print("A uniformScaleObjs() init ...")
    print("A uniformScaleObjs() meshObjNames: ", meshObjNames)
    meshObjs = []
    for ns in meshObjNames:
        if sceneObjects[ns]:
            meshObjs.append(sceneObjects[ns])
        #
    
    boundsData = getObjsBounds(meshObjNames, sceneObjects)
    sizeV = boundsData[2]
    sx = dstSizeV[0] / sizeV[0]
    sy = dstSizeV[1] / sizeV[1]
    sz = dstSizeV[2] / sizeV[2]
    # 等比缩放
    sx = sy = sz = min(sx, min(sy, sz))
    print("uniformScaleObjs() sx: ", sx)
    for obj in meshObjs:
        location = obj.location
        print("uniformScaleObjs() location: ", location)
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
    print("uniformScaleObjs() end ...")
    return True

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
                print("getSceneObjsBounds() list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)
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
    print("minV: ", minV)
    print("maxV: ", maxV)
    print("width: ", width)
    print("height: ", height)
    print("long: ", long)
    print("getObjsBounds() end ...")

    # for debug
    # boundsUtils.createBoundsFrameBox(minV, maxV)
    return (minV,  maxV, (width, height, long))
###
def uniformScaleSceneObjs(dstSizeV):
    print("uniformScaleSceneObjs() init ...")
    boundsData = getSceneObjsBounds()
    sizeV = boundsData[2]
    sx = dstSizeV[0] / sizeV[0]
    sy = dstSizeV[1] / sizeV[1]
    sz = dstSizeV[2] / sizeV[2]
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