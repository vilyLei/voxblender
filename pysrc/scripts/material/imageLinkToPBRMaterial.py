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

# thanks: https://blenderartists.org/t/assign-image-texture-for-material-in-script/1392848/3

node_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
# node_tex.location = [-300,300]
node_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/albedo.jpg')
# LINK NODES
links = mat.node_tree.links
link = links.new(node_tex.outputs[0], matNode.inputs["Base Color"])

node_normal_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
node_normal_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/normal.jpg')
# LINK NODES
links = mat.node_tree.links
link = links.new(node_normal_tex.outputs[0], matNode.inputs["Normal"])

node_roughness_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
node_roughness_tex.image = bpy.data.images.load(rootDir + 'voxblender/models/pbrtex/wall/roughness.jpg')
# LINK NODES
links = mat.node_tree.links
link = links.new(node_roughness_tex.outputs[0], matNode.inputs["Roughness"])