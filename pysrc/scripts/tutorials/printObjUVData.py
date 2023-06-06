import bpy
import time


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

cube01 = bpy.data.objects["Cube"]
uv_layer = cube01.data.uv_layers.active
print("uv_layer: ", uv_layer)
# 遍历 UV 数据
for loop in cube01.data.loops:
    uv_coords = uv_layer.data[loop.index].uv
    print("UV coordinates for loop %d: (%f, %f)" % (loop.index, uv_coords[0], uv_coords[1]))

print("proc end.")