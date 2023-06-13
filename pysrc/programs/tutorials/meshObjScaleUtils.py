#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
        if ns in sceneObjects:
            meshObjs.append(sceneObjects[ns])
        #
    
    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    for obj in meshObjs:
        # print("mesh obj: ", obj)
        print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)
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
# dimensions
def uniformScaleObjs(dstSizeV, meshObjNames, sceneObjects):
    print("uniformScaleObjs() init ...")
    print("uniformScaleObjs() meshObjNames: ", meshObjNames)
    meshObjs = []
    for ns in meshObjNames:
        if ns in sceneObjects:
            meshObjs.append(sceneObjects[ns])
        #
    
    boundsData = getObjsBounds(meshObjNames, sceneObjects)
    sizeV = boundsData[2]
    
    sx = dstSizeV[0] / (sizeV[0] + 1.0)
    sy = dstSizeV[1] / (sizeV[1] + 1.0)
    sz = dstSizeV[2] / (sizeV[2] + 1.0)
    # 等比缩放
    sx = sy = sz = min(sx, min(sy, sz))
    # sx = sy = sz = 0.02
    for obj in meshObjs:
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
    print("uniformScaleObjs() end ...")
    return True

def uniformScaleObjsByValue(s, meshObjNames, sceneObjects):
    print("uniformScaleObjsByValue() init ...")
    print("uniformScaleObjsByValue() meshObjNames: ", meshObjNames)
    meshObjs = []
    for ns in meshObjNames:
        meshObjs.append(sceneObjects[ns])
        #
    for obj in meshObjs:
        location = obj.location
        location[0] *= s
        location[1] *= s
        location[2] *= s
        obj.location = location
        if obj.scale:
            scale = obj.scale
            scale[0] *= s
            scale[1] *= s
            scale[2] *= s
            obj.scale = scale
        else:
            obj.scale = (s,s,s)        
            print("obj.scale: ", obj.scale)
        #
    print("uniformScaleObjsByValue() end ...")
    return True