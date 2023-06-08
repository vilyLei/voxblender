import bpy
from bpy import context

# Select objects that will be rendered
for obj in context.scene.objects:
    obj.select_set(False)
for obj in context.visible_objects:
    if not (obj.hide_get() or obj.hide_render):
        obj.select_set(True)
#
print("ops ...")
bpy.ops.view3d.camera_to_view_selected()