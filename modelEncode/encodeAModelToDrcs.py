#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
import sys
import time
import os

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

encoderPath = "draco_encoder.exe"
modelFilePath = "export_0.obj"

def exportObjs():
    global modelFilePath
    print("####### encodeStart call end ...")
    # D:\programs\blender\blender.exe -b -P .\exportMeshesToDrcObjs.py -- modelFilePath=scene01\scene01.fbx
    encode_command = "D:\\programs\\blender\\blender.exe -b -P .\\exportMeshesToDrcObjs.py -- modelFilePath="+modelFilePath
    print("encode_command: ", encode_command)
    # return
    process = subprocess.Popen(encode_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, universal_newlines=True)
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
    process.stdout.close()
    process.wait()
    print("####### encodeAModelToDrcs::exportObjs() call end ...")


def encodeAObjFile(filePath, savingDir):
    global encoderPath

    # parts = modelFilePath.split(".")
    index = filePath.rindex(".")
    namePath = filePath[0:index]
    # suffix = modelFilePath[index+1:]
    print("namePath: ", namePath)
    # print("suffix: ", suffix)
    index = namePath.rindex("/")
    fname = namePath[index+1:]
    fileSavingPath = savingDir + fname + ".drc"
    encode_command = encoderPath + " -i " + filePath +" -o " + fileSavingPath + " -cl 10 -qp 11 -qt 10 -qn 10 -qg 8"
    print("encode_command: ", encode_command)
    # return
    process = subprocess.Popen(encode_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, universal_newlines=True)
    # for line in iter(process.stdout.readline, ""):
    #     print(line, end="")
    # process.stdout.close()
    process.wait()
    print("####### encodeAModelToDrcs::encodeStart() call end ...")

def findAllObjFile(dirPath):
    for root, ds, fs in os.walk(dirPath):
        for f in fs:
            yield f
    #######
def encodeStart():
    global modelFilePath
    mfPath = modelFilePath.replace("\\","/")
    mfPath = mfPath.replace("//","/")
    index = mfPath.rindex("/")
    mfDir = mfPath[0:index+1]
    objsDir = mfDir + "dracoObj/"
    savingDir = mfDir + "draco/"
    
    print("encodeAModelToDrcs::encodeStart(), mfPath: ", mfPath)
    print("encodeAModelToDrcs::encodeStart(), mfDir: ", mfDir)
    print("encodeAModelToDrcs::encodeStart(), objsDir: ", objsDir)
    print("encodeAModelToDrcs::encodeStart(), savingDir: ", savingDir)
    
    if not os.path.exists(savingDir):
        os.makedirs(savingDir)
    # total = 0
    fileNames = []
    for file in findAllObjFile(objsDir):
        print("file A: ", file)
        fileNames.append(objsDir + file)
        # encodeAObjFile(objsDir + file, savingDir)
        # total += 1
        # if total > 1:
        #     break
    
    for i in range(0, len(fileNames)):
        print("file B: ", fileNames[i])
        encodeAObjFile(fileNames[i], savingDir)


if __name__ == "__main__":
    argv = sys.argv
    # print("argv: \n", argv)
    print("encodeAModelToDrcs init ...")
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        # print("sub0 argv: \n", argv)
        if len(argv) > 1:            
            encoderPath = argv[0].split("=")[1]
            modelFilePath = argv[1].split("=")[1]
            exportObjs()
            encodeStart()
            
    else:
        argv = []
    # ###
    print("####### encodeAModelToDrcs end ...")
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe modelFilePath=private\scene01\scene01.fbx
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe modelFilePath=private\scene03\scene03.fbx
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe modelFilePath=private\model02\model02.glb