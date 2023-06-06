import bpy

# Set the render engine to Cycles
bpy.context.scene.render.engine = 'CYCLES'

# Add a camera to the scene
bpy.ops.object.camera_add(location=(0, 0, 10), rotation=(0, 0, 0))

# Add a light to the scene
bpy.ops.object.light_add(type='POINT', location=(0, 0, 5))

# Set the camera as the active object
bpy.context.view_layer.objects.active = bpy.context.scene.camera

# obj_filePath = "D:/dev/blender/modules/apple_01.obj"
# imported_object = bpy.ops.import_scene.obj(filepath=obj_filePath)
# obj_object = bpy.context.selected_objects[0]
# print('Imported the apple obj name: ', obj_object.name)

# Set the render settings
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.resolution_percentage = 100

# Set the output file format and path
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = "D:/dev/blender/renderingImg/cyclesRendering.png"

# Render the scene
bpy.ops.render.render(write_still=True)