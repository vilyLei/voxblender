import bpy
import os

inner_path = 'Object'
object_name = 'Sphere'


file_path = 'D:/dev/webdev/voxblender/scenes/twoSpheres.blend'

bpy.ops.wm.append(
     filepath=os.path.join(file_path, inner_path, object_name),
     directory=os.path.join(file_path, inner_path),
     filename=object_name
     )

#bpy.ops.wm.append(filepath = 'D:/dev/webdev/voxblender/scenes/twoSpheres.blend')