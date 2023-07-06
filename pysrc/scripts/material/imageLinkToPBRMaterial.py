import bpy
import os

rootDir = "D:/dev/webdev/"
if not os.path.exists(rootDir):
    rootDir = "D:/dev/webProj/"
    
dir_path = "C:\\Users\\Administrator\\Desktop\\objTest"

# for subdir, dirs, files in os.walk(dir_path):
#     for file in files:
#         if file.lower().endswith((".obj", ".obj")):
#             file_path = os.path.join(subdir, file)

#             # Import the OBJ file
#             bpy.ops.import_scene.obj(filepath=file_path)

#             # Get the imported object
#             obj = bpy.context.selected_objects[0]

#             # Add a new material to the object
#             mat = bpy.data.materials.new(name="Material")
#             obj.data.materials.append(mat)

#             # Set the material to use the Principled BSDF shader
#             mat.use_nodes = True
#             nodes = mat.node_tree.nodes
#             principled_bsdf = nodes.get("Principled BSDF")
#             if principled_bsdf is None:
#                 principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
#             material_output = nodes.get("Material Output")
#             if material_output is None:
#                 material_output = nodes.new(type="ShaderNodeOutputMaterial")
#             links = mat.node_tree.links
#             links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

#             # Add an image texture to the material and connect it to the Base Color of the Principled BSDF
#             texture_path = os.path.join(subdir, "texture.jpg")
#             if os.path.exists(texture_path):
#                 image = bpy.data.images.load(texture_path)
#                 texture = bpy.data.textures.new(name="Texture", type='IMAGE')
#                 texture.image = image
#                 texture_node = nodes.new(type="ShaderNodeTexImage")
#                 texture_node.image = image
#                 texture_node.texture_mapping.scale[0] = 2.0
#                 texture_node.texture_mapping.scale[1] = 2.0
#                 links.new(texture_node.outputs["Color"], principled_bsdf.inputs["Base Color"])


#             # Export the object as a GLB file
#             glb_path = os.path.splitext(file_path)[0] + ".glb"
#             bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', export_image_format='AUTO', export_materials='EXPORT')

#             # Delete the imported object
#             bpy.ops.object.select_all(action='DESELECT')
#             obj.select_set(True)
#             bpy.ops.object.delete(use_global=False, confirm=False)

def directToTarget(obj, target):
    constraint = obj.constraints.new('TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    return constraint

meshT = bpy.ops.mesh
# meshT.primitive_cube_add(size=2,location=(0,0,0))
meshT.primitive_cube_add(size=2,location=(0,0,0))
cube = bpy.context.active_object
meshT.primitive_plane_add(size=5)
plane = bpy.context.active_object

light_data = bpy.data.lights.new('light',type='POINT' )
light = bpy.data.objects.new('light', light_data)
bpy.context.collection.objects.link(light)
light.location = (3, -4, 5)
light.data.energy = 200.0

cam_data = bpy.data.cameras.new('camera')
cam = bpy.data.objects.new('camera', cam_data)
cam.location=(6,-6,6)
bpy.context.collection.objects.link(cam)

directToTarget(cam, cube)


mat = bpy.data.materials.new(name='Material')
mat.use_nodes = True
mat_nodes = mat.node_tree.nodes
mat_links = mat.node_tree.links

cube.data.materials.append(mat)

# mat_nodes['Principled BSDF'].inputs['Metallic'].default_value = 1.0
# mat_nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.8,0.3,0.0,1.0)
matNode = mat_nodes[0]
matNode.inputs['Metallic'].default_value = 1.0
matNode.inputs['Base Color'].default_value = (0.8,0.3,0.0,1.0)


# thanks: https://blenderartists.org/t/assign-image-texture-for-material-in-script/1392848/3
links = mat.node_tree.links

node_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
# node_tex.location = [-300,300]
# https://docs.blender.org/api/current/bpy.types.ShaderNodeTexImage.html#shadernodeteximage-shadernode
node_tex.extension = "REPEAT"
node_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/albedo.jpg')
link = links.new(node_tex.outputs[0], matNode.inputs["Base Color"])


node_roughness_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
node_roughness_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/roughness.jpg')
node_roughness_tex.image.colorspace_settings.name = 'Non-Color'
link = links.new(node_roughness_tex.outputs[0], matNode.inputs["Roughness"])

node_metallic_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
node_metallic_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/metallic.jpg')
node_metallic_tex.image.colorspace_settings.name = 'Non-Color'
link = links.new(node_metallic_tex.outputs[0], matNode.inputs["Metallic"])


node_normal_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
node_normal_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/normal.jpg')
node_normal_tex.image.colorspace_settings.name = 'Non-Color'
link = links.new(node_normal_tex.outputs[0], matNode.inputs["Normal"])
for i, o in enumerate(node_normal_tex.outputs):
    print("node_normal_tex.outputs >>>: ", i, o.name)
