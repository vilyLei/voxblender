import bpy
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)


# Get all objects in selection
# selection = bpy.context.selected_objects

# # Get the active object
# active_object = bpy.context.active_object

currentObj = bpy.data.objects["Cube"]
# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

obj = currentObj
# Select each object
obj.select_set(True)
# Make it active
bpy.context.view_layer.objects.active = obj
# Toggle into Edit Mode
bpy.ops.object.mode_set(mode='EDIT')
# Select the geometry
bpy.ops.mesh.select_all(action='SELECT')
# Call the smart project operator
bpy.ops.uv.smart_project()
# Toggle out of Edit Mode
bpy.ops.object.mode_set(mode='OBJECT')
# Deselect the object
obj.select_set(False)

# Restore the selection
obj.select_set(True)

# Restore the active object
bpy.context.view_layer.objects.active = currentObj

print("proc smart uv project end, for a obj.")