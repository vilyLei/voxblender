#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import bpy
import bmesh
import struct

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    #print(sys.path)

import rsystem
version = rsystem.getVersion()
print("version: ", version)

def clearScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
################################################################################
def toTuplesByStep4(datals):
    ds = tuple(datals)
    n = 4
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds

def toTuplesByStep3(datals):
    ds = tuple(datals)
    n = 3
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds

def toTuplesByStep2(datals):
    ds = tuple(datals)
    n = 2
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds

def toFloat32List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//4
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/4)+'f',dataStr)
    data = struct.unpack(segLen*'f',dataStr)
    return data
###
def toUint16List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//2
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/2)+'f',dataStr)
    data = struct.unpack(segLen*'H',dataStr)
    return data
###
def toUint32List(dataStr):
    bytesTotal = len(dataStr)
    print("bytesTotal: ", bytesTotal)
    # 下面的双斜线是除法结果为整数
    segLen = bytesTotal//4
    print("segLen: ", segLen)
    # 如果考虑字节序，字节序为big-endian，则以下语句改为  data = struct.unpack('>'+str(bytesTotal/4)+'I',dataStr)
    data = struct.unpack(segLen*'I',dataStr)
    return data


################################

def getFloat32FileData(dir, filePath, stride = 3):
    file_vs = open(dir + filePath,'rb')
    dataStr = file_vs.read()
    if stride == 3:
        return list(toTuplesByStep3(toFloat32List(dataStr)))
    else:
        return list(toTuplesByStep2(toFloat32List(dataStr)))

def getUint16FileData(dir, filePath, stride = 3):
    file_vs = open(dir + filePath,'rb')
    dataStr = file_vs.read()
    if stride == 3:
        return list(toTuplesByStep3(toUint16List(dataStr)))
    else:
        return list(toTuplesByStep4(toUint16List(dataStr)))

def getUint32FileData(dir, filePath, stride = 3):
    file_vs = open(dir + filePath,'rb')
    dataStr = file_vs.read()
    if stride == 3:
        return list(toTuplesByStep3(toUint32List(dataStr)))
    else:
        return list(toTuplesByStep4(toUint32List(dataStr)))

################################################################

def rtaskRun():

    clearScene()

    rootDir = "D:/dev/webProj/"
    #rootDir = "D:/dev/webdev/"


    vertices = getFloat32FileData(rootDir, 'voxblender/models/verticesBox.bin')
    print("vertices:\n", vertices)

    faces = getUint16FileData(rootDir, 'voxblender/models/indicesBox.bin')
    print("faces:\n", faces)

    uv_coords = getFloat32FileData(rootDir, 'voxblender/models/uvBox.bin', 2)
    print("uv_coords:\n", uv_coords)

    normals = getFloat32FileData(rootDir, 'voxblender/models/normalBox.bin')
    print("normals:\n", normals)

    # 创建mesh和物体
    mesh = bpy.data.meshes.new("Cube")
    robjEntity = bpy.data.objects.new("Cube", mesh)

    # 将物体添加到场景
    scene = bpy.context.scene
    scene.collection.objects.link(robjEntity)

    # 创建bmesh对象
    bm = bmesh.new()
    bm.from_mesh(mesh)

    # bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)
    # bm.faces.ensure_lookup_table()

    # 添加顶点
    # print("vertices: ", vertices)
    for v in vertices:
        # print("v: ", v)
        bm.verts.new(v)

    bm.verts.ensure_lookup_table()
    print("len(faces): ", len(faces))
    # 添加面
    for k in range(0, len(faces)):
        bm.faces.new([bm.verts[i] for i in faces[k]])
    # ... 在这里为其他面重复这个过程

    # 添加法线
    for vert, normal in zip(bm.verts, normals):
        vert.normal = normal

    # 添加UV坐标
    uv_layer = bm.loops.layers.uv.verify()
    for f, uv in zip(bm.faces, uv_coords):
        for loop in f.loops:
            loop[uv_layer].uv = uv

    # 更新mesh数据
    bm.to_mesh(mesh)
    bm.free()

    # 更新mesh的法线
    mesh.calc_normals()

    robjEntity.scale = (0.1,0.1, 0.1)

    # 添加UV纹理到物体
    # mesh.uv_textures.new("UVMap")

    vertex_normals = robjEntity.data.vertex_normals
    # 遍历每个顶点和其法线
    for i, vertex in enumerate(robjEntity.data.vertices):
        normal = vertex_normals[i]
        print("vtx normal: ", normal.vector)
    ################################################################
    print("build proc end ...")
    print("ready to rendering ...")

    renderer = bpy.context.scene.render
    
    renderer.engine = 'BLENDER_EEVEE'
    renderer.image_settings.file_format='PNG'
    renderer.filepath = rootDir + "voxblender/renderingImg/loadAndRenderingMeshFromeRawData.PNG"
    renderer.resolution_x = 512 #perhaps set resolution in code
    renderer.resolution_y = 512
    bpy.ops.render.render(write_still=True)
    print("rendering proc end ...")
if __name__ == "__main__":
    argv = sys.argv
    print("argv: \n", argv)
    # argv = argv[argv.index("--") + 1:]
    print("rendering task init ...")
    rtaskRun()

# D:\programs\blender\blender.exe -b -P .\loadMeshAndRenderingFromRawData.py -- dir=./