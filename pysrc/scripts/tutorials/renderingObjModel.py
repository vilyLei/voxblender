import bpy
# import mathutils
# # 创建一个cube
# bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0,0, 0), scale=(1, 1, 1))
# # 获取这个cube
# cube = bpy.data.objects["Cube"]
# print("a cube: ", cube)
# # v0 = mathutils.Vector((2.0, 0.0, 0.0))
# # # 设置这个cube的坐标(X轴坐标为2.0,Y轴和轴为0.0), 移动这个cube
# # cube.location = v0

# obj_filePath = "D:/dev/blender/modules/apple_01.obj"
# imported_object = bpy.ops.import_scene.obj(filepath=obj_filePath)
# obj_object = bpy.context.selected_objects[0]
# print('Imported the apple obj name: ', obj_object.name)

obj_filePath = "D:/dev/blender/modules/box01.obj"
imported_object = bpy.ops.import_scene.obj(filepath=obj_filePath)
obj_object = bpy.context.selected_objects[0]
print('Imported the apple obj name: ', obj_object.name)

# import bpy
renderer = bpy.context.scene.render
renderer.image_settings.file_format='JPEG'
renderer.filepath = "D:/dev/blender/renderingImg/apple01Rendering.jpg"
renderer.resolution_x = 512 #perhaps set resolution in code
renderer.resolution_y = 512
bpy.ops.render.render(write_still=True)

# D:\programs\blender\blender.exe -b -P .\renderingObjModel.py