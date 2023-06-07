import sys
import bpy
import time

def renderAObj() :
    obj_file = "D:/dev/webProj/voxblender/models/box02.obj"
    output_file = "D:/dev/webProj/voxblender/renderingImg/rendering01.png"

    print("bpy.data.objects: ", bpy.data.objects)
    print("lsit(bpy.data.objects): ", list(bpy.data.objects))

    cube01 = bpy.data.objects["Cube"]
    if cube01:
        bpy.data.objects.remove(cube01)
    else:
        print("has not the default Cube.")

    print("###  ###  ###  ###  ###")
    # 加载OBJ模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    print("list(bpy.context.selected_objects): ", list(bpy.context.selected_objects))
    obj_object = bpy.context.selected_objects[0]
    print("obj_object: ", obj_object)

    # 设置渲染引擎
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'

    # 设置输出路径和文件格式
    bpy.context.scene.render.filepath = output_file
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512

    # 等待1秒钟
    time.sleep(0.5)

    # 渲染并保存图片
    bpy.ops.render.render(write_still=True)
    print("rendering task end ...")

# D:\programs\blender\blender.exe -b -P  .\loadAndRendering_default.py -- path\a path\bli
if __name__ == "__main__":
    # 获取命令行参数
    argv = sys.argv
    print("argv: \n", argv)
    # argv = argv[argv.index("--") + 1:]
    print("rendering task init ...")
    renderAObj()