#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess
import sys
import time
# r_progress = 100

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

encoderPath = "draco_encoder.exe"
modelFilePath = "export_0.obj"

def encodeStart():
    global encoderPath

    encoderPath = "draco_encoder.exe"
    # parts = modelFilePath.split(".")
    index = modelFilePath.rindex(".")
    namePath = modelFilePath[0:index]
    # suffix = modelFilePath[index+1:]
    print("namePath: ", namePath)
    # print("suffix: ", suffix)

    encode_command = encoderPath + " -i " + modelFilePath +" -o " + namePath + ".drc -cl 10 -qp 11 -qt 10 -qn 10 -qg 8"
    print("encode_command: ", encode_command)
    # return
    process = subprocess.Popen(encode_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, universal_newlines=True)
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
    process.stdout.close()
    process.wait()
    print("####### encodeStart call end ...")
if __name__ == "__main__":
    argv = sys.argv
    # print("argv: \n", argv)
    print("encodeAMeshModel init ...")
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        # print("sub0 argv: \n", argv)
        if len(argv) > 1:            
            encoderPath = argv[0].split("=")[1]
            modelFilePath = argv[1].split("=")[1]
            # sys_renderingModulePath = argv[1].split("=")[1]
            # sys_rtaskDir = argv[2].split("=")[1]
            encodeStart()
            
    else:
        argv = []
    # ### for test
    # renderingStart()
    # if r_progress >= 100:
    #     updateRenderStatus()
    print("####### encodeAMeshModel end ...")
    # python .\encodeAMeshModel.py -- encoder=D:\dev\webProj\voxblender\modelEncode\draco_encoder.exe modelFilePath=export_0.ply