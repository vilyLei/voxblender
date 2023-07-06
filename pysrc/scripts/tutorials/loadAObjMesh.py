import bpy
import os

rootDir = "D:/dev/webdev/"
if not os.path.exists(rootDir):
    rootDir = "D:/dev/webProj/"

def loadAObjMesh(obj_file):
    # 加载OBJ模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
    obj_object = bpy.context.selected_objects[0]
    # obj_object.scale = (0.1,0.1,0.1)
    print("obj_object: ", obj_object)
    #
### #### #### #### ### ### ### #### ###


resUrl = rootDir + "voxblender/models/box01.obj"

loadAObjMesh( resUrl )