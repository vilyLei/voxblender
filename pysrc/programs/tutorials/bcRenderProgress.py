import subprocess
import math

blender_command = "D:\programs\\blender\\blender.exe -b -P .\\renderingModelFile.py"
process = subprocess.Popen(blender_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)

# Fra:1 Mem:419.85M (Peak 419.85M) | Time:00:05.75 | Remaining:00:01.25 | Mem:773.58M, Peak:773.58M | Scene, ViewLayer | Sample 416/512
# Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 3/4 Tiles, Sample 512/512

# Fra:1 Mem:1264.65M (Peak 1264.65M) | Time:01:01.01 | Mem:402.92M, Peak:774.79M | Scene | ViewLayer | Denoising
# Fra:1 Mem:1264.65M (Peak 1648.65M) | Time:01:17.51 | Mem:1618.92M, Peak:1618.92M | Scene | ViewLayer | Finishing
# Fra:1 Mem:547.85M (Peak 739.85M) | Time:00:10.40 | Mem:773.58M, Peak:773.58M | Scene, ViewLayer | Finished
# Saved: 'D:\dev\webProj\voxblender\renderingImg\renderingModelFile.png'
# Time: 01:19.42 (Saving: 00:01.38)

tilesTotal = 1
tilesIndex = 0
r_prrogress = 0.0
dis_rprogress = 75.0
preTileSNList = [0 ,0,0]

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
    global r_prrogress
    global dis_rprogress
    tfactors = getRTileProgressInfo(line)
    sample_factors = getRSampleProgressInfo( line )
    if preTileSNList[1] == tfactors[1] and preTileSNList[2] == tfactors[2]:
        tstot = sample_factors[2]
        k0 = (tfactors[1] * tstot  + sample_factors[1])
        k1 = (tfactors[2] * tstot)
        factor = k0/k1
        pro = round(factor * dis_rprogress) + 10
        if pro > r_prrogress:
            r_prrogress = pro
        # print("#### tile rending, sample info: ", k0, k1, factor, round(factor * dis_rprogress), dis_rprogress)
        print("#### rendering progress: ", r_prrogress, "%")
    else:
        preTileSNList[1] = tfactors[1]
        preTileSNList[2] = tfactors[2]

def renderTask():

    global r_prrogress
    global dis_rprogress
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
        if "Fra:" in line:
            if " Denoising" in line:
                print("## denoising.")
                r_prrogress = 95
                print("## rendering progress: ", r_prrogress, "%")
            elif " Finished" in line:
                print("## rendering Finished.")
                r_prrogress = 90
                print("## rendering progress: ", r_prrogress, "%")
            elif " Tiles," in line:
                getRTileProgress(line)
                # print("## tile rendering.")
            elif " Sample" in line:
                sample_factor = getRSampleProgressInfo( line )[0]
                r_prrogress = round(sample_factor * dis_rprogress) + 10
                print("## rendering progress: ", r_prrogress, "%")
            elif " ViewLayer | Initializing" in line:
                if r_prrogress < 1:
                    r_prrogress = 1
                print("## rendering progress: ", r_prrogress, "%")
            elif " ViewLayer | Updating Images" in line:
                if r_prrogress < 2:
                    r_prrogress = 2
                print("## rendering progress: ", r_prrogress, "%")
            elif " ViewLayer | Updating Objects" in line:
                if r_prrogress < 3:
                    r_prrogress = 3
                print("## rendering progress: ", r_prrogress, "%")
            elif " ViewLayer | Updating Scene BVH" in line:
                if r_prrogress < 5:
                    r_prrogress = 5
                print("## rendering progress: ", r_prrogress, "%")
            elif " ViewLayer | Updating Device" in line:
                if r_prrogress < 8:
                    r_prrogress = 8
                print("## rendering progress: ", r_prrogress, "%")
        elif "(Saving:" in line:
            r_prrogress = 100
            print("## rendering finish and saved a pic.")
            print("## rendering progress: ", r_prrogress, "%")
        elif "Blender quit" in line:
            print("## Blender quit.")
        else:
            i = 0

    print("####### bcRenderProcess step 03 ...")
    process.stdout.close()
    process.wait()
    #

renderTask()
# for test
# line = "Fra:1 Mem:780.19M (Peak 1084.19M) | Time:01:07.79 | Remaining:00:22.24 | Mem:913.18M, Peak:913.18M | Scene, ViewLayer | Rendered 3/4 Tiles, Sample 512/512"
# line = "Fra:1 Mem:780.19M (Peak 1084.19M) | Time:01:07.91 | Remaining:00:22.22 | Mem:913.18M, Peak:913.18M | Scene, ViewLayer | Rendered 3/4 Tiles, Sample 1/512"
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 0/4 Tiles, Sample 0/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 0/4 Tiles, Sample 100/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 0/4 Tiles, Sample 300/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 0/4 Tiles, Sample 500/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 0/4 Tiles, Sample 512/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 1/4 Tiles, Sample 35/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 1/4 Tiles, Sample 50/512"
# getRTileProgress(line)
# line = "Fra:1 Mem:421.06M (Peak 725.06M) | Time:01:00.43 | Mem:774.79M, Peak:774.79M | Scene, ViewLayer | Rendered 1/4 Tiles, Sample 150/512"
# getRTileProgress(line)
print("####### bcRenderProcess end ...")
# python .\bcRenderProgress.py
# python D:\dev\webProj\voxblender\pysrc\programs\tutorials\bcRenderProgress.py