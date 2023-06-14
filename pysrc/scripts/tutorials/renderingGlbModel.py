import sys
import time
import bpy
from bpy import context

# 下面这一行代码用于在Scripting窗口中运行pythion脚本代码引入自定义module
dirStr = r"D:/dev/webProj/voxblender/pysrc/scripts/tutorials"
if not (dirStr in sys.path):
    sys.path += [dirStr]
else:
    print("path include this dir ...")

import meshObjScaleUtils

rootDir = "D:/dev/webProj/"
#rootDir = "D:/dev/webdev/"

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

modelUrl = rootDir + "voxblender/models/apple01.glb"
modelUrl = rootDir + "voxblender/models/model01.glb"
modelUrl = rootDir + "voxblender/models/model03.glb"
loadAGlbMesh(modelUrl)

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


scaleFlag = meshObjScaleUtils.uniformScaleObjs((2.0, 2.0, 2.0), mesh_obj_names, sceneObjects)
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
bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

output_img_resolution = 1024

renderer = bpy.context.scene.render
# renderer.film_transparent = True
renderer.image_settings.file_format='PNG'
renderer.filepath = rootDir + "voxblender/renderingImg/rendering.png"
renderer.resolution_x = output_img_resolution
renderer.resolution_y = output_img_resolution
bpy.ops.render.render(write_still=True)

# D:\programs\blender\blender.exe -b -P .\renderingObjModel.py