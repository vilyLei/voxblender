import bpy
from math import sin, cos, pi
from mathutils import Euler

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

# cam_data = bpy.data.cameras.new('camera')
# cam = bpy.data.objects.new('camera', cam_data)
# cam.location=(6,-6,6)
# bpy.context.collection.objects.link(cam)

# Create camera
bpy.ops.object.add(type='CAMERA', location=(0, -3.0, 0))
# camera = bpy.context.object
camera = bpy.context.active_object
camera.data.lens = 35
camera.rotation_euler = Euler((pi/2, 0, 0), 'XYZ')

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
