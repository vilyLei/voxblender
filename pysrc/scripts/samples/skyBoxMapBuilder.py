import bpy
import math
import mathutils
import os

name = "shape";
imageSize = 512
savePath = "D:/dev/blender/skyBox/"

scene = bpy.context.scene

cam_data = bpy.data.cameras.new('SkyBoxCamera')
cam = bpy.data.objects.new('SkyBoxCamera', cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

bpy.context.scene.render.resolution_x = imageSize
bpy.context.scene.render.resolution_y = imageSize
cam.data.lens_unit = 'FOV'
#cam.data.angle = 1.5708
cam.data.angle = math.pi/2

#cam.rotation_clear(clear_delta=False)0
#scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.file_format = 'JPEG'

cam.rotation_euler = mathutils.Euler((0, 0, 0))
#scene.render.filepath = os.path.join(savePath, name+"_Down.png")
scene.render.filepath = os.path.join(savePath, name+"_dn.png")
bpy.ops.render.render(write_still = 1)

cam.rotation_euler = mathutils.Euler((math.pi/2, 0, 0))
#scene.render.filepath = os.path.join(savePath, name+"_Front.png")
scene.render.filepath = os.path.join(savePath, name+"_ft.png")
bpy.ops.render.render(write_still = 1)

#cam.rotation_euler = mathutils.Euler((math.pi, 0, 0))
cam.rotation_euler = mathutils.Euler((math.pi, 0, 0))
#scene.render.filepath = os.path.join(savePath, name+"_Up.png")
scene.render.filepath = os.path.join(savePath, name+"_up.png")
bpy.ops.render.render(write_still = 1)

cam.rotation_euler = mathutils.Euler((math.pi*3/2, math.pi, 0))
#scene.render.filepath = os.path.join(savePath, name+"_Back.png")
scene.render.filepath = os.path.join(savePath, name+"_bk.png")
bpy.ops.render.render(write_still = 1)

cam.rotation_euler = mathutils.Euler((-math.pi/2, math.pi,-math.pi/2))
#scene.render.filepath = os.path.join(savePath, name+"_Right.png")
scene.render.filepath = os.path.join(savePath, name+"_rt.png")
bpy.ops.render.render(write_still = 1)

cam.rotation_euler = mathutils.Euler((math.pi/2,0,-math.pi/2))
#scene.render.filepath = os.path.join(savePath, name+"_Left.png")
scene.render.filepath = os.path.join(savePath, name+"_lf.png")
bpy.ops.render.render(write_still = 1)

objs = bpy.data.objects
objs.remove(cam, do_unlink=True)