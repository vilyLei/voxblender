import bpy
import os
import threading
import time
import math

rootDir = "D:/dev/webdev/"
if not os.path.exists(rootDir):
    rootDir = "D:/dev/webProj/"

def render_scene(scene, on_render_progress):
# def render_scene(on_render_progress):
    # 设置渲染引擎为Cycles
    # scene.render.engine = 'CYCLES'
    # # 设置渲染完成度回调函数
    # bpy.app.handlers.render_write.append(on_render_progress)
    # # 渲染场景
    # bpy.ops.render.render(write_still=True)
    # 渲染进度回调函数的设置
    bpy.app.handlers.render_write.append(on_render_progress)

    renderer = scene.render

    # 获取Cycles渲染设备的首选项
    cycles_preferences = bpy.context.preferences.addons['cycles'].preferences
    # 启用GPU渲染
    cycles_preferences.compute_device_type = 'CUDA'  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    # 创建一个设备集合，包括所有可用的GPU设备
    devices = cycles_preferences.get_devices()
    print(">>> devices: ", devices)
    # 激活所有可用的GPU设备
    # if devices:
    #     for device in devices:
    #         if device.type == 'CUDA':  # 如果使用NVIDIA GPU，改为'OPENCL'如果使用AMD GPU
    #             device.use = True
    # 设置设备类型为GPU
    scene.cycles.device = 'GPU'



    # Set the background to use an environment texture
    # bpy.context.scene.render.film_transparent = True
    bpy.context.scene.world.use_nodes = True
    bg_tree = bpy.context.scene.world.node_tree
    # bg_tree.nodes is bpy.types.Nodes type
    bg_node = bg_tree.nodes.new(type='ShaderNodeTexEnvironment')
    bg_node.location = (-300, 300)
    bg_node.select = True
    bg_tree.nodes.active = bg_node

    # Load the environment texture file
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/box.jpg')
    bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/street.hdr')

    # Connect the environment texture to the background output
    bg_output = bg_tree.nodes['Background']
    bg_output.inputs['Strength'].default_value = 0.5
    bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

    rimg_resolution  = 256
    # renderer.engine = 'BLENDER_EEVEE'
    renderer.engine = 'CYCLES'
    renderer.image_settings.file_format='PNG'
    renderer.filepath = rootDir + "voxblender/renderingImg/renderBlenderFile.png"
    renderer.resolution_x = rimg_resolution
    renderer.resolution_y = rimg_resolution
    bpy.context.scene.cycles.samples = 64
    bpy.ops.render.render(write_still=True)
    # bpy.ops.render.render('INVOKE_DEFAULT', animation=False, write_still=True)

def on_render_progress(scene, path):
    current_frame = scene.frame_current
    total_frames = scene.frame_end - scene.frame_start + 1
    progress = (current_frame - scene.frame_start) / total_frames
    print(f"渲染进度: {progress * 100:.2f}%")

scene = bpy.context.scene
render_scene(scene, on_render_progress)
# thread = threading.Thread(target=render_scene, args=(scene, on_render_progress))
# # thread = threading.Thread(target=render_scene, args=(on_render_progress))
# thread.start()

# while thread.is_alive():
#     # print("###")
#     time.sleep(0.1)
#     #
# D:\programs\blender\blender.exe -b ..\..\..\models\scene01.blend -P .\renderBlenderFile.py
# D:\programs\blender\blender.exe -b ..\..\..\models\scene05.blend -P .\renderBlenderFile.py
# D:\programs\blender\blender.exe -b ..\..\..\models\fruit_apple.blend -P .\renderBlenderFile.py
# D:\programs\blender\blender.exe -b D:\modling\res\b4kTexGlb.blend -P .\renderBlenderFile.py