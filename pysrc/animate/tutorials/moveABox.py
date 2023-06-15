import bpy
cubeSpeed = 0.1
scene = bpy.context.scene
cube = scene.objects.get('Cube')

def update_scene(sc):
    global cubeSpeed
    global cube
    if cube is not None:
        pos = cube.location
        pos.x += cubeSpeed
        cube.location = pos
        if pos.x >= 2.0 and cubeSpeed > 0.0:
            cubeSpeed *= -1.0
        elif pos.x <= -2.0 and cubeSpeed < 0.0:
            cubeSpeed *= -1.0
        ################
        rot = cube.rotation_euler
        rot[1] += 0.02
        rot[2] += 0.02
    #
print("init...")


handlers = bpy.app.handlers.frame_change_post
handlers.clear()
handlers.append(update_scene)

scene.render.fps = 60

# 停止当前动画播放
bpy.ops.screen.animation_cancel(restore_frame=False)
# 将当前帧设置为动画的起始帧
scene.frame_current = scene.frame_start
# 重新启动动画播放
bpy.ops.screen.animation_play()
    