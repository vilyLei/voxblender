#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import subprocess
import sys
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

blender_command = "D:\programs\\blender\\blender.exe -b -P .\\renderingModelFile.py"

tilesTotal = 1
tilesIndex = 0
r_progress = 0.0
dis_rprogress = 75.0
preTileSNList = [0 ,0,0]
sys_rendererExePath = ""
sys_renderingModulePath = ""
sys_rtaskDir = ""

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

statusData = {
    "rendering-ins":"rbld-scene-renderer",
    "rendering-task":
    {
        "uuid":"rtrt88970-8990",
        "taskID":1,
        "name":"high-image-rendering",
        "phase":"running",
        "progress":20,
        "times":2
    },
    "rendering-status":"task:running"
}
rconfig = None

def getJsonObjFromFile(path):
    file = open(path,'rb')
    jsonDataStr = file.read()
    # print("jsonDataStr: \n", jsonDataStr)
    jsonObj = json.loads(jsonDataStr)
    return jsonObj

def writeErrorStatus(logInfo):
    global rconfig
    if rconfig is None:
        rconfig = getJsonObjFromFile( sys_rtaskDir + 'config.json' )

    taskObj = rconfig["task"]
    global statusData
    rtask = statusData["rendering-task"]
    rtask["phase"] = "error"
    rtask["progress"] = 100
    rtask["times"] = taskObj["times"]
    rtask["taskID"] = taskObj["taskID"]
    
    with open(sys_rtaskDir + 'renderingStatus.json', 'w') as f:
        json.dump(statusData, f)
    ##################################################
    with open(sys_rtaskDir + 'error_log.txt', 'w') as file:
        file.write(logInfo)
    ##################################################

def updateRenderStatus():
    
    global rconfig
    global r_progress
    global statusData
    url = sys_rtaskDir + 'renderingStatus.json'
    
    rtask = statusData["rendering-task"]
    if rconfig is None:
        rconfig = getJsonObjFromFile( sys_rtaskDir + 'config.json' )
        taskObj = rconfig["task"]
        rtask["times"] = taskObj["times"]
        rtask["taskID"] = taskObj["taskID"]
    rtask["progress"] = r_progress
    if r_progress >= 100:
        rtask["phase"] = "finish"

    print("&$$$$$$$ updateRenderStatus(), r_progress: ", r_progress)
    # 将数据写入 JSON 格式的文件
    with open(url, 'w') as f:
        json.dump(statusData, f)

def getRSampleProgressInfo(line):
    rinfos = line.split(" Sample")
    # print("getRSampleProgressInfo(), rinfos: ", rinfos)
    rinfos = rinfos[1].strip()
    rinfos = rinfos.split("/")
    f0 = float(rinfos[0])
    f1 = float(rinfos[1])
    factor = f0/f1
    return (factor, f0, f1)

def getRTileProgressInfo(line):
    rinfos = line.split("| Rendered ")[1]
    # print("rinfos: ", rinfos)
    rinfos = rinfos.split(" ")
    rinfos = rinfos[0].strip()
    rinfos = rinfos.split("/")
    t0 = float(rinfos[0])
    t1 = float(rinfos[1])
    factor = t0 / t1
    # print("getRTileProgressInfo(), ", rinfos[0], "/", rinfos[1])
    return (factor, t0, t1)

def getRTileProgress(line):
    # print(">>>>>>>>>>>>>>>> #### getRTileProgress ####")
    global preTileSNList
    global r_progress
    global dis_rprogress
    tfactors = getRTileProgressInfo(line)
    sample_factors = getRSampleProgressInfo( line )
    if preTileSNList[1] == tfactors[1] and preTileSNList[2] == tfactors[2]:
        tstot = sample_factors[2]
        k0 = (tfactors[1] * tstot  + sample_factors[1])
        k1 = (tfactors[2] * tstot)
        factor = k0/k1
        pro = round(factor * dis_rprogress) + 10
        if pro > r_progress:
            r_progress = pro            
            print("###> rendering progress: ", r_progress, "%")
            updateRenderStatus()
        # print("#### tile rending, sample info: ", k0, k1, factor, round(factor * dis_rprogress), dis_rprogress)
    else:
        preTileSNList[1] = tfactors[1]
        preTileSNList[2] = tfactors[2]

def renderingStart():

    if sys_rendererExePath != "":
        rendererExePath = sys_rendererExePath
        print("apply sys rendererExePath")
    else:
        rendererExePath = "D:/programs/blender/blender.exe"
    
    if sys_renderingModulePath != "":
        print("apply sys renderingModulePath")
        renderingModulePath = sys_renderingModulePath
    else:
        renderingModulePath = rootDir + "voxblender/pysrc/programs/tutorials/modelFileRendering.py"
    
    params = " -- dir=none"
    if sys_rtaskDir != "":
        params = " -- dir=" + sys_rtaskDir
    
    blender_command = rendererExePath + " -b -P " + renderingModulePath + params
    print("blender_command:\n",blender_command)
    # return
    global r_progress
    global dis_rprogress
    process = subprocess.Popen(blender_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

    for line in iter(process.stdout.readline, ""):
        print(line, end="")
        # try:
        #     print(line, end="")
        # except Exception as e:
        #     print("Error: print(line, end='')")
        if "Fra:" in line:
            if " Denoising" in line:
                print("## denoising.")
                r_progress = 95
                print("## rendering progress: ", r_progress, "%")
                updateRenderStatus()
            elif " Finished" in line:
                print("## rendering Finished.")
                r_progress = 90
                updateRenderStatus()
                print("## rendering progress: ", r_progress, "%")
            elif " Tiles," in line:
                getRTileProgress(line)
                # print("## tile rendering.")
            elif " Sample" in line:
                sample_factor = getRSampleProgressInfo( line )[0]
                r_progress = round(sample_factor * dis_rprogress) + 10
                updateRenderStatus()
                print("## rendering progress: ", r_progress, "%")
            elif " ViewLayer | Initializing" in line:
                if r_progress < 1:
                    r_progress = 1                
                updateRenderStatus()
                print("## rendering progress: ", r_progress, "%")
            elif " ViewLayer | Updating Images" in line:
                if r_progress < 2:
                    r_progress = 2                
                updateRenderStatus()
                print("## rendering progress: ", r_progress, "%")
            elif " ViewLayer | Updating Objects" in line:
                if r_progress < 3:
                    r_progress = 3
                print("## rendering progress: ", r_progress, "%")
            elif " ViewLayer | Updating Scene BVH" in line:
                if r_progress < 5:
                    r_progress = 5                
                updateRenderStatus()
                print("## rendering progress: ", r_progress, "%")
            elif " ViewLayer | Updating Device" in line:
                if r_progress < 8:
                    r_progress = 8                
                updateRenderStatus()
                print("## rendering progress: ", r_progress, "%")
        elif "(Saving:" in line:
            r_progress = 100
            # updateRenderStatus()
            print("## rendering finish and saved a pic.")
            print("## rendering progress: ", r_progress, "%")
        elif "Blender quit" in line:
            print("## Blender quit.")
        elif "Error:" in line:
            now = int(round(time.time()*1000))
            currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
            errorInfo = "\n### " + currTime + ""
            errorInfo += "\n### " + sys_rtaskDir + ""
            errorInfo += "\n### have a Error in bcRenderShell: \n" + line
            print(errorInfo)
            writeErrorStatus(errorInfo)
        else:
            i = 0

    process.stdout.close()
    process.wait()
    #

if __name__ == "__main__":
    argv = sys.argv
    # print("argv: \n", argv)
    print("bcRenderShell init ...")
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
        # print("sub0 argv: \n", argv)
        if len(argv) > 1:            
            sys_rendererExePath = argv[0].split("=")[1]
            sys_renderingModulePath = argv[1].split("=")[1]
            sys_rtaskDir = argv[2].split("=")[1]
            # print("sys_rendererExePath: ", sys_rendererExePath)
            # print("sys_renderingModulePath: ", sys_renderingModulePath)
            renderingStart()
            i = 0
    else:
        argv = []
    # ### for test
    # renderingStart()
    if r_progress >= 100:
        updateRenderStatus()
    print("####### bcRenderShell end ...")
################################################################################
# D:/dev/webProj/voxblender/models/model01/apple01.glb
# D:/dev/webProj/voxblender/models/model01/
# python .\bcRenderShell.py
# python D:\dev\webProj\voxblender\pysrc\programs\tutorials\bcRenderShell.py -- renderer=D:/programs/blender/blender.exe rmodule=D:/dev/webProj/voxblender/pysrc/programs/tutorials/modelFileRendering.py rtaskDir=D:/dev/webProj/voxblender/models/model01/
# python D:\dev\webProj\voxblender\pysrc\programs\tutorials\bcRenderShell.py -- renderer=D:\\programs\\blender\\blender.exe rmodule=D:\\dev\\webProj\\voxblender\\pysrc\\programs\\tutorials\\modelFileRendering.py rtaskDir=D:/dev/webProj/voxblender/models/model01/