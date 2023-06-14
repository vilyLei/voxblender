import bpy
import threading
import time

def render_scene(scene):
    rootDir = "D:/dev/webProj/"
    # rootDir = "D:/dev/webdev/"
    # 渲染进度回调函数的设置
    # bpy.app.handlers.render_write.append(on_render_progress)

    # renderer = scene.render

    # # 获取Cycles渲染设备的首选项
    # cycles_preferences = bpy.context.preferences.addons['cycles'].preferences
    # # 启用GPU渲染
    # cycles_preferences.compute_device_type = 'CUDA'  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    # # 创建一个设备集合，包括所有可用的GPU设备
    # devices = cycles_preferences.get_devices()
    # print(">>> devices: ", devices)
    # # 激活所有可用的GPU设备
    # # for device in devices:
    # #     if device.type == 'CUDA':  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    # #         device.use = True
    # # 设置设备类型为GPU
    # scene.cycles.device = 'GPU'

    # rimg_resolution  = 4096
    # # renderer.engine = 'BLENDER_EEVEE'
    # renderer.engine = 'CYCLES'
    # renderer.image_settings.file_format='PNG'
    # renderer.filepath = rootDir + "voxblender/renderingImg/multiThrRenderBlenderFile.png"
    # renderer.resolution_x = rimg_resolution
    # renderer.resolution_y = rimg_resolution
    # bpy.context.scene.cycles.samples = 64
    # bpy.ops.render.render(write_still=True)
    #

def on_render_progress(scene, path):
    current_frame = scene.frame_current
    total_frames = scene.frame_end - scene.frame_start + 1
    progress = (current_frame - scene.frame_start) / total_frames
    print(f"渲染进度: {progress * 100:.2f}%")

print("multiThrLoadGlb sys begin ...")
scene = bpy.context.scene
thread = threading.Thread(target=render_scene, args=(scene, ))
# thread = threading.Thread(target=render_scene, args=(on_render_progress))
thread.start()

while thread.is_alive():
    # print("###")
    time.sleep(0.1)
    #
print("multiThrLoadGlb sys end ...")
# D:\programs\blender\blender.exe -b -P .\multiThrLoadGlb.py