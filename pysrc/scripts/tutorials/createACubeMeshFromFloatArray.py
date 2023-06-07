import bpy
# 创建一个新的立方体对象
new_mesh = bpy.data.meshes.new('new_mesh')
# 定义立方体的顶点和面
vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1), (1, 0, 1)]
faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
# 使用顶点和面创建立方体网格
# from_pydata(vertices, edges, faces)
new_mesh.from_pydata(vertices, [], faces)
new_mesh.update()

# make object from mesh
new_object = bpy.data.objects.new('new_object', new_mesh)
# make collection
new_collection = bpy.data.collections.new('new_collection')
bpy.context.scene.collection.children.link(new_collection)
# add object to scene collection
new_collection.objects.link(new_object)
