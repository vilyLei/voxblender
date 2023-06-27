#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
import sys
import time
import os
import json

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

encoderPath = "draco_encoder.exe"
modelFilePath = "export_0.obj"
modelFileDir = "./"

exportPyPath = ".\\exportMeshesToDrcObjs.py"

statusData = {
    "rins":"encoder",
    "phase":"finish"
}

def writeStatusFile():
    with open(modelFileDir + 'draco/status.json', 'w') as f:
        json.dump(statusData, f)
    ###
def exportObjs():
    global modelFilePath
    global exportPyPath
    print("####### encodeStart call end ...")
    # D:\dev\webProj\voxblender\modelEncode\exportMeshesToDrcObjs.py
    # D:\programs\blender\blender.exe -b -P .\exportMeshesToDrcObjs.py -- modelFilePath=scene01\scene01.fbx
    
    fileInfos = os.path.splitext(modelFilePath)
    # print("fileInfos: ", fileInfos)
    suffix = fileInfos[1][1:]
    suffix = suffix.lower()
    if suffix == "blend" or suffix == "bld":
        encode_command = "D:\\programs\\blender\\blender.exe -b "+ modelFilePath +" -P " + exportPyPath + " -- modelFilePath="+modelFilePath
    else:
        encode_command = "D:\\programs\\blender\\blender.exe -b -P " + exportPyPath + " -- modelFilePath="+modelFilePath
    
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
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
    process.stdout.close()
    process.wait()
    print("####### encodeAModelToDrcs::encodeStart() call end ...")

def findAllObjFile(dirPath):
    for root, ds, fs in os.walk(dirPath):
        for f in fs:
            yield f
    #######
def encodeStart():
    global modelFileDir
    global modelFilePath
    mfPath = modelFilePath.replace("\\","/")
    mfPath = mfPath.replace("//","/")
    index = mfPath.rindex("/")
    modelFileDir = mfPath[0:index+1]
    objsDir = modelFileDir + "dracoObj/"
    savingDir = modelFileDir + "draco/"
    
    print("encodeAModelToDrcs::encodeStart(), mfPath: ", mfPath)
    print("encodeAModelToDrcs::encodeStart(), modelFileDir: ", modelFileDir)
    print("encodeAModelToDrcs::encodeStart(), objsDir: ", objsDir)
    print("encodeAModelToDrcs::encodeStart(), savingDir: ", savingDir)
    
    if os.path.exists(savingDir):
        for file in findAllObjFile(savingDir):
            filePath = savingDir + file
            print("remove a file: ", filePath)
            os.remove(filePath)
    else:
        os.makedirs(savingDir)
    # total = 0
    # return
    fileNames = []
    for file in findAllObjFile(objsDir):
        fileNames.append(objsDir + file)
    
    for i in range(0, len(fileNames)):
        encodeAObjFile(fileNames[i], savingDir)
    ###

if __name__ == "__main__":
    argv = sys.argv
    # print("argv: \n", argv)
    print("encodeAModelToDrcs init ...")
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        # print("sub0 argv: \n", argv)
        if len(argv) > 1:            
            encoderPath = argv[0].split("=")[1]
            exportPyPath = argv[1].split("=")[1]
            modelFilePath = argv[2].split("=")[1]
            # fileInfos = os.path.splitext(modelFilePath)
            # print("suffix: ", fileInfos[1][1:])
            # print("fileInfos: ", fileInfos)
            exportObjs()
            encodeStart()
            writeStatusFile()
            
    else:
        argv = []
    # ###
    print("####### encodeAModelToDrcs end ...")
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webdev\voxblender\modelEncode\draco_encoder.exe exportPy=D:\dev\webdev\voxblender\modelEncode\exportMeshesToDrcObjs.py modelFilePath=private\scene01\scene01.fbx
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webdev\voxblender\modelEncode\draco_encoder.exe exportPy=D:\dev\webdev\voxblender\modelEncode\exportMeshesToDrcObjs.py modelFilePath=D:\dev\webdev\voxblender\modelEncode\private\scene01\scene01.fbx
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webdev\voxblender\modelEncode\draco_encoder.exe exportPy=D:\dev\webdev\voxblender\modelEncode\exportMeshesToDrcObjs.py modelFilePath=D:\dev\webdev\voxblender\modelEncode\private\scene04\scene04.blend
    
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe exportPy=D:\dev\webProj\voxblender\modelEncode\exportMeshesToDrcObjs.py modelFilePath=private\scene03\scene03.fbx
    # python D:\dev\webProj\voxblender\modelEncode\encodeAModelToDrcs.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe exportPy=D:\dev\webProj\voxblender\modelEncode\exportMeshesToDrcObjs.py modelFilePath=D:\dev\webProj\voxblender\modelEncode\private\scene03\scene03.fbx
    # python .\encodeAModelToDrcs.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe exportPy=D:\dev\webProj\voxblender\modelEncode\exportMeshesToDrcObjs.py modelFilePath=private\model02\model02.glb