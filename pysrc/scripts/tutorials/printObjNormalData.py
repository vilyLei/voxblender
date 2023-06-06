import bpy
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)


# 获取当前活动对象
cube01 = bpy.data.objects["Cube"]

## 获取网格数据
mesh = cube01.data
# 获取所有顶点法线
vertex_normals = mesh.vertex_normals

# 遍历每个顶点和其法线
for i, vertex in enumerate(mesh.vertices):
    normal = vertex_normals[i]
    print("proc normal: ", normal.vector)
#    normal = vertex_normals[i].to_tuple()
#    print(f"Vertex {i}: {normal}")

print("proc normal end.")