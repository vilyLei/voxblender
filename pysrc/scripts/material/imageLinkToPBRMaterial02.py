import bpy

def directToTarget(obj, target):
    constraint = obj.constraints.new('TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    return constraint

meshT = bpy.ops.mesh
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


rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

links = mat.node_tree.links

uvScales = [8.0,8.0]

node_color_tex = mat_nodes.new("ShaderNodeTexImage")
# node_tex.location = [-300,300]

node_color_tex.texture_mapping.scale[0] = uvScales[0]
node_color_tex.texture_mapping.scale[1] = uvScales[1]

node_color_tex.extension = "REPEAT"
node_color_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/albedo.jpg')
link = links.new(node_color_tex.outputs[0], matNode.inputs["Base Color"])

node_metallic_tex = mat_nodes.new("ShaderNodeTexImage")
node_metallic_tex.texture_mapping.scale[0] = uvScales[0]
node_metallic_tex.texture_mapping.scale[1] = uvScales[1]

node_metallic_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/metallic.jpg')
node_metallic_tex.image.colorspace_settings.name = 'Non-Color'
# link = links.new(node_metallic_tex.outputs[0], matNode.inputs["Metallic"])
node_metallic_colorMixRGB = mat_nodes.new("ShaderNodeMixRGB")

for i, o in enumerate(node_metallic_colorMixRGB.inputs):
    print("node_metallic_colorMixRGB.inputs >>>: ", i, o.name)
for i, o in enumerate(node_metallic_colorMixRGB.outputs):
    print("node_metallic_colorMixRGB.outputs >>>: ", i, o.name)

node_metallic_colorMixRGB.inputs[0].default_value = 0.0
node_metallic_colorMixRGB.inputs[2].default_value = (1.0,1.0,1.0, 1.0)
# node_metallic_colorMixRGB.blend_type = 'ADD'
link = links.new(node_metallic_tex.outputs[0], node_metallic_colorMixRGB.inputs[1])
link = links.new(node_metallic_colorMixRGB.outputs[0], matNode.inputs["Metallic"])

node_roughness_tex = mat_nodes.new("ShaderNodeTexImage")
node_roughness_tex.texture_mapping.scale[0] = uvScales[0]
node_roughness_tex.texture_mapping.scale[1] = uvScales[1]
node_roughness_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/roughness.jpg')
node_roughness_tex.image.colorspace_settings.name = 'Non-Color'
# link = links.new(node_roughness_tex.outputs[0], matNode.inputs["Roughness"])
node_roughness_colorMixRGB = mat_nodes.new("ShaderNodeMixRGB")

for i, o in enumerate(node_roughness_colorMixRGB.inputs):
    print("node_roughness_colorMixRGB.inputs >>>: ", i, o.name)
for i, o in enumerate(node_roughness_colorMixRGB.outputs):
    print("node_roughness_colorMixRGB.outputs >>>: ", i, o.name)

node_roughness_colorMixRGB.inputs[0].default_value = 0.0
node_roughness_colorMixRGB.inputs[2].default_value = (0.0,0.0,0.0, 1.0)
# node_roughness_colorMixRGB.blend_type = 'ADD'
link = links.new(node_roughness_tex.outputs[0], node_roughness_colorMixRGB.inputs[1])
link = links.new(node_roughness_colorMixRGB.outputs[0], matNode.inputs["Roughness"])

node_normal_tex = mat_nodes.new("ShaderNodeTexImage")
node_normal_tex.texture_mapping.scale[0] = uvScales[0]
node_normal_tex.texture_mapping.scale[1] = uvScales[1]
node_normal_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/normal.jpg')
node_normal_tex.image.colorspace_settings.name = 'Non-Color'
# link = links.new(node_normal_tex.outputs[0], matNode.inputs["Normal"])

node_normalMap = mat_nodes.new("ShaderNodeNormalMap")
# node_normalMap.use_custom_color = True
node_normalMap.uv_map = 'UVMap'
node_normalMap.inputs[0].default_value = 2.0
print("node_normalMap.space: ", node_normalMap.space)
link = links.new(node_normal_tex.outputs[0], node_normalMap.inputs[1])
link_normalMap_and_notmal = links.new(node_normalMap.outputs[0], matNode.inputs["Normal"])
## method 1: remove a shader node from a nodes
# mat_nodes.remove(node_normalMap)
## method 2: remove a link from a links
# links.remove(link_normalMap_and_notmal)

for i, o in enumerate(node_normal_tex.outputs):
    print("node_normal_tex.outputs >>>: ", i, o.name)
for i, o in enumerate(node_normalMap.inputs):
    print("node_normalMap.inputs >>>: ", i, o.name)
for i, o in enumerate(node_normalMap.outputs):
    print("node_normalMap.outputs >>>: ", i, o.name)

