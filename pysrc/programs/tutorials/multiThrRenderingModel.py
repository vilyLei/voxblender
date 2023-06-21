import os
import sys
import time
import bpy
from bpy import context
import threading

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    # print(sys.path)

import meshObjScaleUtils

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

def clearAllMeshesInScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    #
def clearScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
################################################################################
def loadAObjMesh(obj_file):
    # 加载OBJ模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    #    
def loadAFbxMesh(fbx_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.fbx(filepath=fbx_file)
    #
def loadAGlbMesh(glb_file):
    # 加载glb模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    #
def loadAUsdMesh(usd_file):
    # 加载usd模型
    imported_object = bpy.ops.wm.usd_import(filepath=usd_file)
    #

def loadModelWithUrl(url):
    resType = url.split('.')[1]
    resType = resType.lower()
    print("######### loadModelWithUrl(), resType: ", resType)
    if resType == "obj":
            loadAObjMesh(url)
    elif resType == "fbx":
        loadAFbxMesh(url)
    elif resType == "glb":
        loadAGlbMesh(url)
    elif resType == "usdc":
        loadAUsdMesh(url)
    elif resType == "usdz":
        loadAUsdMesh(url)
    else:
        return False
    return True
    #
def objsFitToCamera():
    # Select objects that will be rendered
    for obj in context.scene.objects:
        obj.select_set(False)
    for obj in context.visible_objects:
        if not (obj.hide_get() or obj.hide_render):
            obj.select_set(True)
    #
    print("objsFitToCamera ops ...")
    bpy.ops.view3d.camera_to_view_selected()
    #

def load_handler(dummy):
    print("### Load Handler:", bpy.data.filepath)
    print("### Load dummy:", dummy)


bpy.app.handlers.load_post.append(load_handler)

# # 获取模型文件的加载进度
# while bpy.context.window_manager.progress_update != 1.0:
#     pass

# clearScene()
clearAllMeshesInScene()
modelUrl = rootDir + "voxblender/models/apple01.glb"
modelUrl = rootDir + "voxblender/models/apple01.usdc"
# modelUrl = rootDir + "voxblender/models/model01.usdz"
# modelUrl = rootDir + "voxblender/models/model01.glb"
# modelUrl = rootDir + "voxblender/models/model03.glb"
# modelUrl = rootDir + "voxblender/private/glb/xiezi-en.glb"
modelUrl = rootDir + "voxblender/models/scene03.fbx"
# modelUrl = rootDir + "voxblender/models/scene03.glb"
loadModelWithUrl(modelUrl)

# 等待1秒钟
# time.sleep(2.0)
sceneObjects = bpy.data.objects

# dict for mesh:object[]
mesh_objectDict = {}
mesh_obj_names = []
mesh_objs = []

scaleFlag = meshObjScaleUtils.uniformScaleSceneObjs((2.0, 2.0, 2.0))
objsFitToCamera()


def render_scene(scene):
    # Set the background to use an environment texture
    # bpy.context.scene.render.film_transparent = True
    bpy.context.scene.world.use_nodes = True
    bg_tree = bpy.context.scene.world.node_tree
    # bg_tree.nodes is bpy.types.Nodes type
    bg_node = bg_tree.nodes.new(type='ShaderNodeTexEnvironment')
    # bg_node.location = (-300, 300)
    bg_node.select = True
    bg_tree.nodes.active = bg_node

    # Load the environment texture file
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/box.jpg')
    bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/street.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/stinsonBeach.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/sky_cloudy.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/memorial.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/cool_white.hdr')

    # Connect the environment texture to the background output
    bg_output = bg_tree.nodes['Background']
    bg_output.inputs['Strength'].default_value = 0.5
    bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

    # 设置设备类型为GPU
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 16

    # print("bpy.context.scene.cycles: ", bpy.context.scene.cycles)


    output_img_resolution = 4096 // 8

    output_img_resolution = 128

    renderer = bpy.context.scene.render

    renderer.engine = 'CYCLES'
    # renderer.threads = 8
    # renderer.film_transparent = True
    # renderer.image_settings.file_format='PNG'
    # renderer.filepath = rootDir + "voxblender/renderingImg/multiThrRenderingModel.png"
    renderer.image_settings.file_format='JPEG'
    renderer.filepath = rootDir + "voxblender/renderingImg/multiThrRenderingModel.jpg"
    #https://docs.blender.org/api/current/bpy.types.RenderEngine.html
    renderer.resolution_x = output_img_resolution
    renderer.resolution_y = output_img_resolution

    print("### renderer.pixel_aspect_x: ", renderer.pixel_aspect_x)
    print("### renderer.pixel_aspect_y: ", renderer.pixel_aspect_y)
    renderer.pixel_aspect_x = 1.0
    renderer.pixel_aspect_y = 1.0
    bpy.ops.render.render(write_still=True)
    # bpy.ops.render.render(write_still=False)

print("multiThrRenderingModel sys begin ...")
# scene = bpy.context.scene
# thread = threading.Thread(target=render_scene, args=(scene, ))
# # thread = threading.Thread(target=render_scene, args=(on_render_progress))
# thread.start()
rtimes = 10
#thread.is_alive()
thread = None
while rtimes > 0:
    # print("###")
    time.sleep(1.0)
    if thread is None:
        rtimes -= 1
        if rtimes == 8:
            scene = bpy.context.scene
            thread = threading.Thread(target=render_scene, args=(scene, ))
            thread.start()
    elif not thread.is_alive():
        print("waiting ...")
        thread = None
    #
print("multiThrRenderingModel sys end ...")
# D:\programs\blender\blender.exe -b -P .\multiThrRenderingModel.py