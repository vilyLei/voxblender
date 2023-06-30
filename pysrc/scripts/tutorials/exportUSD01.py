import bpy
import os
import time



now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
directory = ""
target_file = os.path.join(directory, "D:/dev/webProj/voxblender/renderingImg/export.usdz")

bpy.ops.wm.usd_export(filepath=target_file)
print("export usd proc end.")