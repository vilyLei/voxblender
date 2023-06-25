#!/usr/bin/python
# -*- coding: UTF-8 -*-
# import os
# import time
import sys
import json
import bpy
import time
from bpy import context
import mathutils
from mathutils import Matrix

# # 下面这三句代码用于 background 运行时，能正常载入自定义python module
# dir = os.path.dirname(bpy.data.filepath)
# if not dir in sys.path:
#     sys.path.append(dir )
#     # print(sys.path)

# import meshObjScaleUtils


def toTuplesByStep4(datals):
    ds = tuple(datals)
    n = 4
    rds = tuple(ds[i:i + n] for i in range(0, len(ds), n))
    return rds

def getJsonObjFromFile(path):
    file = open(path,'rb')
    jsonDataStr = file.read()
    print("jsonDataStr: \n", jsonDataStr)
    jsonObj = json.loads(jsonDataStr)
    return jsonObj

class RenderingCfg:
    name = ""
    taskRootDir = ""
    rootDir = ""
    configPath = ""
    configObj = {}
    outputPath = ""
    outputResolution = [1024, 1024]
    bgTransparent = False
    def __init__(self, root_path):
        self.taskRootDir = root_path
        #
    def setRootDir(self, dir):
        self.taskRootDir = dir
        self.rootDir = dir
        #
    def getConfigData(self):
        print("getConfigData() init ...")
        self.configPath = self.taskRootDir + "config.json"
        self.configObj = getJsonObjFromFile(self.configPath)
        cfg = self.configObj
        taskObj = cfg["task"]
        self.outputPath = self.taskRootDir + taskObj["outputPath"]
        
        if "bgTransparent" in taskObj:
            self.bgTransparent = taskObj["bgTransparent"]
        if "outputResolution" in taskObj:
            self.outputResolution = taskObj["outputResolution"]
        ### get sys info
        if "sys" in cfg:
            sysObj = cfg["sys"]
            self.rootDir = sysObj["rootDir"]
            print("### self.rootDir: ", self.rootDir)
            #
        # print("getConfigData() self.configObj: ", self.configObj)
        #

sysRenderingCfg = RenderingCfg("")

def updateCamWithCfg(cfg):
    taskObj = cfg.configObj["task"]
    cdvs = taskObj["camdvs"]
    print("updateCamWithCfg(), cdvs: ", cdvs)
    cdvsList = toTuplesByStep4(cdvs)
    cam_world_matrix = Matrix()
    cam_world_matrix[0] = cdvsList[0]
    cam_world_matrix[1] = cdvsList[1]
    cam_world_matrix[2] = cdvsList[2]
    cam_world_matrix[3] = cdvsList[3]


    camera_object = bpy.data.objects["Camera"]
    camera_object.matrix_world = cam_world_matrix
    #

def getSceneObjsBounds():
    print("getObjsBounds() init ...")
    
    minx, miny, minz = (999999.0,) * 3
    maxx, maxy, maxz = (-999999.0,) * 3
    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
            mesh_objectDict[m.name] = []
    
    # sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                # print("getSceneObjsBounds() list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)
                for v in obj.bound_box:
                    v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))

                    if v_world[0] < minx:
                        minx = v_world[0]
                    if v_world[0] > maxx:
                        maxx = v_world[0]

                    if v_world[1] < miny:
                        miny = v_world[1]
                    if v_world[1] > maxy:
                        maxy = v_world[1]

                    if v_world[2] < minz:
                        minz = v_world[2]
                    if v_world[2] > maxz:
                        maxz = v_world[2]
    
    # for obj in meshObjs:
    #     # print("mesh obj: ", obj)
    #     print("mesh list(obj.bound_box[0]): ", list(obj.bound_box[0]), obj.dimensions)        

    minV = (minx, miny, minz)
    maxV = (maxx, maxy, maxz)
    width = maxV[0] - minV[0]
    height = maxV[1] - minV[1]
    long = maxV[2] - minV[2]
    # print("minV: ", minV)
    # print("maxV: ", maxV)
    # print("width: ", width)
    # print("height: ", height)
    # print("long: ", long)
    print("getObjsBounds() end ...")

    # for debug
    # boundsUtils.createBoundsFrameBox(minV, maxV)
    return (minV,  maxV, (width, height, long))
###
def uniformScaleSceneObjs(dstSizeV):
    print("uniformScaleSceneObjs() init ...")
    boundsData = getSceneObjsBounds()
    sizeV = boundsData[2]

    # sx = dstSizeV[0] / sizeV[0]
    # sy = dstSizeV[1] / sizeV[1]

    if sizeV[0] > 0.0001:
        sx = dstSizeV[0] / sizeV[0]
    else:
        sx = 1.0
    if sizeV[1] > 0.0001:
        sy = dstSizeV[1] / sizeV[1]
    else:
        sy = 1.0
    if sizeV[2] > 0.0001:
        sz = dstSizeV[2] / sizeV[2]
    else:
        sz = 1.0
    # 等比缩放
    sx = sy = sz = min(sx, min(sy, sz))

    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
        mesh_objectDict[m.name] = []
    
    # sizeValue = 0
    # attach objects to dict keys
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:
                location = obj.location
                location[0] *= sx
                location[1] *= sy
                location[2] *= sz
                obj.location = location
                scale = obj.scale
                scale[0] *= sx
                scale[1] *= sy
                scale[2] *= sz
                obj.scale = scale
                #
    print("uniformScaleSceneObjs() end ...")
    return True

taskRootDir = "D:/dev/webProj/"
# taskRootDir = "D:/dev/webdev/"

def clearAllMeshesInScene():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    #
def clearScene():    
    obj = bpy.data.objects["Cube"]
    if obj:
        bpy.data.objects.remove(obj)
    else:
        print("has not the default Cube object in the current scene.")
################################################################################
    
def loadAObjMesh(obj_file):
    # 加载OBJ模型
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    #    
def loadAFbxMesh(fbx_file):
    # 加载FBX模型
    imported_object = bpy.ops.import_scene.fbx(filepath=fbx_file)
    #
def loadAGlbMesh(glb_file):
    # 加载glb模型
    imported_object = bpy.ops.import_scene.gltf(filepath=glb_file)
    #
def loadAUsdMesh(usd_file):
    # 加载usd模型
    imported_object = bpy.ops.wm.usd_import(filepath=usd_file)
    #

def loadAObjMeshFromCfg():    
    cfgJson = sysRenderingCfg.configObj
    if "resource" in cfgJson:
        res = cfgJson["resource"]
        modelUrls = res["models"]
        url = modelUrls[0]
        print("model url: ", url)
        loadAObjMesh(url)
        return True
    else:
        print("has not mesh data ...")
    return False

envFilePath = ""
def loadMeshAtFromCfg(index):   
    global envFilePath
    global sysRenderingCfg
    cfgJson = sysRenderingCfg.configObj
    url = ""
    res = None
    resType = ""
    if "resources" in cfgJson:
        resList = cfgJson["resources"]
        res = resList[index]
        modelUrls = res["models"]
        url = sysRenderingCfg.taskRootDir + modelUrls[0]
        print("loadMeshAtFromCfg(), A model url: ", url)
        
    elif "resource" in cfgJson:
        res = cfgJson["resource"]
        modelUrls = res["models"]
        url = sysRenderingCfg.taskRootDir + modelUrls[0]
        # print("loadMeshAtFromCfg(), B model url: ", url)
    else:
        print("has not mesh data ...")
        return False
    if (res is not None) and url != "":
        resType = res["type"] + ""
        if "env" in res:
            envFilePath = res["env"] + ""
        print("Fra:1 Model load begin ...")
        sys.stdout.flush()
        if resType == "obj":
            loadAObjMesh(url)
        elif resType == "fbx":
            loadAFbxMesh(url)
        elif resType == "glb":
            loadAGlbMesh(url)
        elif resType == "usdc":
            loadAUsdMesh(url)
        elif resType == "usdz":
            loadAUsdMesh(url)
        else:
            print("has not correct mesh data type ...")
            return False
        
        print("Fra:1 Model load end ...")
        sys.stdout.flush()
        return True
    else:
        return False

def objsFitToCamera():
    # Select objects that will be rendered
    for obj in context.scene.objects:
        obj.select_set(False)
    for obj in context.visible_objects:
        if not (obj.hide_get() or obj.hide_render):
            obj.select_set(True)
    #
    print("objsFitToCamera ops ...")
    bpy.ops.view3d.camera_to_view_selected()
    #

def load_handler(dummy):
    print("### Load Handler:", bpy.data.filepath)
    print("### Load dummy:", dummy)

bpy.app.handlers.load_post.append(load_handler)

def renderingStart():


    global sysRenderingCfg
    global envFilePath
    cfg = sysRenderingCfg
    # cfg.ttf = 0
    # print("cfg.ttf: ", cfg.ttf)

    clearAllMeshesInScene()
    loadMeshAtFromCfg(0)

    scaleFlag = uniformScaleSceneObjs((2.0, 2.0, 2.0))
    objsFitToCamera()

    updateCamWithCfg(cfg)
    print("####### modelFileRendering envFilePath: ", envFilePath)
    # time.sleep(3.0)

    # Set the background to use an environment texture
    bpy.context.scene.render.film_transparent = cfg.bgTransparent
    bpy.context.scene.world.use_nodes = True

    envHdrFilePath = ""
    if envFilePath == "":
        print("### cfg.rootDir: ", cfg.rootDir)
        envHdrFilePath = cfg.rootDir + "static/common/env/default.hdr"
        print("### envFilePath: ", envFilePath)
    else:
        envHdrFilePath = taskRootDir + 'street.hdr'

    if envHdrFilePath != "":
        bg_tree = bpy.context.scene.world.node_tree
        # bg_tree.nodes is bpy.types.Nodes type
        bg_node = bg_tree.nodes.new(type='ShaderNodeTexEnvironment')
        # bg_node.location = (-300, 300)
        bg_node.select = True
        bg_tree.nodes.active = bg_node
        # Load the environment texture file
        # bg_node.image = bpy.data.images.load(taskRootDir + 'voxblender/models/box.jpg')
        bg_node.image = bpy.data.images.load(envHdrFilePath)
        # Connect the environment texture to the background output
        bg_output = bg_tree.nodes['Background']
        bg_output.inputs['Strength'].default_value = 0.5
        bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

    # 设置设备类型为GPU
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 512

    # print("bpy.context.scene.cycles: ", bpy.context.scene.cycles)


    # output_img_resolution = 512
    # output_img_resolution = 4096 * 2

    renderer = bpy.context.scene.render

    renderer.engine = 'CYCLES'
    renderer.threads = 8
    # renderer.film_transparent = True
    if cfg.bgTransparent:
        renderer.image_settings.file_format='PNG'
        if cfg.outputPath == "":
            renderer.filepath = taskRootDir + "bld_rendering.png"
        else:
            if "." in cfg.outputPath:
                renderer.filepath = cfg.outputPath
            else:
                renderer.filepath = cfg.outputPath + "bld_rendering.png"
    else:
        renderer.image_settings.file_format='JPEG'
        if cfg.outputPath == "":
            renderer.filepath = taskRootDir + "bld_rendering.jpg"
        else:
            if "." in cfg.outputPath:
                renderer.filepath = cfg.outputPath
            else:
                renderer.filepath = cfg.outputPath + "bld_rendering.jpg"
    #################################################################################
    
    renderer.resolution_x = cfg.outputResolution[0]
    renderer.resolution_y = cfg.outputResolution[1]
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    # sys.stdout.write("modelFileRendering ######################### ...\n")
    print("Fra:1 modelFileRendering ######################### ...")
    print("Fra:1 modelFileRendering init ...")
    sys.stdout.flush()
    argv = sys.argv
    # print("modelFileRendering argv: \n", argv)
    # sys.stdout.write("modelFileRendering init ...\n")
    try:
        if "--" in argv:
            argv = argv[argv.index("--") + 1:]
            # print("sub0 argv: \n", argv)
            if len(argv) > 0:
                taskRootDir = argv[0].split("=")[1]
                sysRenderingCfg.setRootDir(taskRootDir)
                sysRenderingCfg.getConfigData()
                print("taskRootDir: ", taskRootDir)            
                renderingStart()
                i = 0
        else:
            argv = []
    except Exception as e:
        print("Error: rendering task has a error: ", e)
    # ### for test
    # renderingStart()
    print("####### modelFileRendering end ...")
# D:\programs\blender\blender.exe -b -P .\modelFileRendering.py -- rtaskDir=D:/dev/webProj/voxblender/models/model01/
# D:\programs\blender\blender.exe -b -P .\modelFileRendering.py -- rtaskDir=D:/dev/webProj/minirsvr/src/renderingsvr/static/sceneres/v1ModelRTask2001/
# D:\programs\blender\blender.exe -b -P .\modelFileRendering.py -- rtaskDir=D:/dev/webProj/minirsvr/src/renderingsvr/static/sceneres/v1ModelRTask2001/