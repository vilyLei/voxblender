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

target_file = os.path.join(directory, "D:/dev/webProj/voxblender/renderingImg/export_glb.glb")
bpy.ops.export_scene.gltf(filepath=target_file, export_lights=True, export_cameras=True)


# target_file = os.path.join(directory, "D:/dev/webProj/voxblender/renderingImg/export_bld.blend")
# # bpy.ops.export_scene.append(filepath=target_file, export_lights=True, export_cameras=True)
# bpy.ops.wm.append(filepath=target_file)

print("export proc end.")