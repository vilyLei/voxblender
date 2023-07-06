import bpy
import os

rootDir = "D:/dev/webdev/"
if not os.path.exists(rootDir):
    rootDir = "D:/dev/webProj/"
# import mathutils
# # 创建一个cube
# bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0,0, 0), scale=(1, 1, 1))
# # 获取这个cube
# cube = bpy.data.objects["Cube"]
# print("a cube: ", cube)
# # v0 = mathutils.Vector((2.0, 0.0, 0.0))
# # # 设置这个cube的坐标(X轴坐标为2.0,Y轴和轴为0.0), 移动这个cube
# # cube.location = v0

# obj_filePath = "D:/dev/blender/modules/box01.obj"
# imported_object = bpy.ops.import_scene.obj(filepath=obj_filePath)
# obj_object = bpy.context.selected_objects[0]
# print('Imported the apple obj name: ', obj_object.name)


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
bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

renderer = bpy.context.scene.render
# renderer.film_transparent = True
renderer.image_settings.file_format='PNG'
renderer.filepath = rootDir + "voxblender/renderingImg/rendering.png"
renderer.resolution_x = 512 #perhaps set resolution in code
renderer.resolution_y = 512
bpy.ops.render.render(write_still=True)

# D:\programs\blender\blender.exe -b -P .\renderingObjModel.py