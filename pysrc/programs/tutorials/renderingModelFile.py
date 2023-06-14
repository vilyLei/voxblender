import os
import sys
import time
import bpy
from bpy import context

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    print(sys.path)

import meshObjScaleUtils

rootDir = "D:/dev/webProj/"
rootDir = "D:/dev/webdev/"

def clearScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
################################################################################
    
def loadAFbxMesh(fbx_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.fbx(filepath=fbx_file)
    print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
    fbx_object = bpy.context.selected_objects[0]
    # fbx_object.scale = (0.1,0.1,0.1)
    print("fbx_object: ", fbx_object)
    #

def loadAGlbMesh(glb_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
    glb_object = bpy.context.selected_objects[0]
    # glb_object.scale = (0.01,0.01,0.01)
    print("glb_object: ", glb_object)
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

clearScene()
modelUrl = rootDir + "voxblender/models/apple01.glb"
modelUrl = rootDir + "voxblender/models/model01.glb"
modelUrl = rootDir + "voxblender/models/model03.glb"
modelUrl = rootDir + "voxblender/private/glb/xiezi-en.glb"
# modelUrl = rootDir + "voxblender/models/scene03.fbx"
# modelUrl = rootDir + "voxblender/models/scene03.glb"
loadAGlbMesh(modelUrl)
# loadAFbxMesh(modelUrl)

# 等待1秒钟
# time.sleep(2.0)
sceneObjects = bpy.data.objects

# dict for mesh:object[]
mesh_objectDict = {}
mesh_obj_names = []
mesh_objs = []

# create dict with meshes
for m in bpy.data.meshes:
    mesh_objectDict[m.name] = []
# attach objects to dict keys
for o in bpy.context.scene.objects:
    # only for meshes
    if o.type == 'MESH':
        # if this mesh exists in the dict
        if o.data.name in mesh_objectDict:
            # object name mapped to mesh
            mesh_obj_names.append(o.data.name)
            mesh_objs.append(o)

# meshes = set(o.data for o in scene.objects if o.type == 'MESH')
print("mesh_obj_names: ", mesh_obj_names)
print("mesh_objectDict: ", mesh_objectDict)
print("mesh_objs: ", mesh_objs)


# scaleFlag = meshObjScaleUtils.uniformScaleObjsByValue(0.05, mesh_obj_names, sceneObjects)
# scaleFlag = meshObjScaleUtils.uniformScaleObjs((2.0, 2.0, 2.0), mesh_obj_names, sceneObjects)
scaleFlag = meshObjScaleUtils.uniformScaleSceneObjs((2.0, 2.0, 2.0))
objsFitToCamera()

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

# Connect the environment texture to the background output
bg_output = bg_tree.nodes['Background']
bg_output.inputs['Strength'].default_value = 0.5
bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

# 设置设备类型为GPU
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.cycles.samples = 512

output_img_resolution = 4096

renderer = bpy.context.scene.render
renderer.engine = 'CYCLES'
# renderer.film_transparent = True
renderer.image_settings.file_format='PNG'
renderer.filepath = rootDir + "voxblender/renderingImg/renderingModelFile.png"
renderer.resolution_x = output_img_resolution
renderer.resolution_y = output_img_resolution
bpy.ops.render.render(write_still=True)

# D:\programs\blender\blender.exe -b -P .\renderingModelFile.py