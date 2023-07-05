#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import bpy
from bpy import context
import mathutils
from mathutils import Matrix
import time
import os


now = int(round(time.time()*1000))
currTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("\n")
print(currTime)

# 下面这三句代码用于 background 运行时，能正常载入自定义python module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )
    # print(sys.path)

import meshObjScaleUtils

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
    print("width: ", width)
    print("height: ", height)
    print("long: ", long)
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

def loadModelWithUrl(url):
    resType = url.split('.')[1]
    resType = resType.lower()
    print("######### loadModelWithUrl(), resType: ", resType)
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
        return False
    return True
    #

rootDir = "D:/dev/webProj/"
# rootDir = "D:/dev/webdev/"

scene_objectDict = {}
def queryMaterials():
    global scene_objectDict
    print("queryMaterials() init ...")
    # global rootDir

    mesh_objectDict = {}
    # create dict with meshes
    for m in bpy.data.meshes:
            mesh_objectDict[m.name] = []
    
    # for obj in bpy.context.scene.objects:
    #     # only for meshes
    #     if obj.type == 'MESH':
    #         # if this mesh exists in the dict
    #         if obj.data.name in mesh_objectDict:
    #             print("setting false.")
    #             obj.hide_set(False)
    #             obj.select_set(False)
    #             ### ###
    ### ########################################################
    # index = 0
    
    # target_file_dir = rootDir + 'voxblender/private/obj/scene01/export_test01.obj'
    # file_dir = rootDir + 'voxblender/private/obj/scene01/'
    
    context = bpy.context
    viewlayer = context.view_layer
    
    # if not os.path.exists(savingDir):
    #     os.makedirs(savingDir)
    ########################################
    for obj in bpy.context.scene.objects:
        # only for meshes
        if obj.type == 'MESH':
            # if this mesh exists in the dict
            if obj.data.name in mesh_objectDict:

                # obj.hide_set(True)
                # obj.select_set(True)
                # viewlayer.objects.active = obj
                # obj.select_set(True)
                # filePath = savingDir + "export_" + str(index) + ".obj"
                # filePath = savingDir + obj.data.name + ".obj"
                # index += 1
                print("obj.name: ", obj.name)
                print("obj.data.name: ", obj.data.name)
                scene_objectDict[obj.data.name] = obj
                # bpy.ops.export_scene.obj(filepath=filePath, use_selection = True, use_materials=False, use_triangles=True)
                # bpy.ops.export_scene.obj(filepath=filePath, use_selection = True)
                # bpy.ops.export_scene.obj(filepath=filePath, use_selection = True, use_materials=False)
                # obj.hide_set(False)
                # obj.select_set(False)
                # break
                ### ###
    #

def render():
    scaleFlag = meshObjScaleUtils.uniformScaleSceneObjs((2.0, 2.0, 2.0))
    objsFitToCamera()

    # Set the background to use an environment texture
    # bpy.context.scene.render.film_transparent = True
    bpy.context.scene.world.use_nodes = True
    bg_tree = bpy.context.scene.world.node_tree
    # bg_tree.nodes is bpy.types.Nodes type
    bg_node = bg_tree.nodes.new(type='ShaderNodeTexEnvironment')
    # bg_node.location = (-300, 300)
    bg_node.select = True
    bg_tree.nodes.active = bg_node

    # Load the environment texture file
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/box.jpg')
    bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/street.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/stinsonBeach.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/sky_cloudy.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/memorial.hdr')
    # bg_node.image = bpy.data.images.load(rootDir + 'voxblender/models/cool_white.hdr')

    # Connect the environment texture to the background output
    bg_output = bg_tree.nodes['Background']
    bg_output.inputs['Strength'].default_value = 0.5
    bg_tree.links.new(bg_node.outputs['Color'], bg_output.inputs['Color'])

    # 设置设备类型为GPU
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 64

    # print("bpy.context.scene.cycles: ", bpy.context.scene.cycles)

    output_img_resolution = 4096 // 4
    # output_img_resolution = 256
    # output_img_resolution = 4096 * 2

    renderer = bpy.context.scene.render

    renderer.engine = 'CYCLES'
    renderer.threads = 8
    # renderer.film_transparent = True
    renderer.image_settings.file_format='PNG'
    renderer.filepath = rootDir + "voxblender/renderingImg/queryCurrMaterial.png"
    #https://docs.blender.org/api/current/bpy.types.RenderEngine.html
    renderer.resolution_x = output_img_resolution
    renderer.resolution_y = output_img_resolution

    print("### renderer.pixel_aspect_x: ", renderer.pixel_aspect_x)
    print("### renderer.pixel_aspect_y: ", renderer.pixel_aspect_y)
    renderer.pixel_aspect_x = 1.0
    renderer.pixel_aspect_y = 1.0
    bpy.ops.render.render(write_still=True)

    # blend_file_path = bpy.data.filepath
    # directory = os.path.dirname(blend_file_path)
    # target_file = os.path.join(directory, '../../private/obj/export_test01.obj')
    # target_file = rootDir + 'voxblender/private/obj/export_test01.obj'
    # bpy.ops.export_scene.obj(filepath=target_file)


    # target_file = os.path.join(directory, "D:/dev/webProj/voxblender/renderingImg/glbToBld.blend")
    # bpy.ops.wm.save_as_mainfile(filepath=target_file)
    # #####################################
def objsFitToCamera():
    global scene_objectDict
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
def createUVShaderNode(mat_nodes, mat_links):
    node_texCoord = mat_nodes.new("ShaderNodeTexCoord")
    for i, o in enumerate(node_texCoord.outputs):
        print("node_texCoord.outputs >>>: ", i, o.name)
    # node_texCoord.outputs[2], UV
    node_texCoord_mapping = mat_nodes.new("ShaderNodeMapping")
    # node_texCoord_mapping.inputs[0], uv vtx data
    # uv scale
    node_texCoord_mapping.inputs[3].default_value = (1.0,1.0, 1.0)
    link = mat_links.new(node_texCoord.outputs[2], node_texCoord_mapping.inputs[0])
    for i, o in enumerate(node_texCoord_mapping.inputs):
        print("node_texCoord_mapping.inputs >>>: ", i, o.name)
    for i, o in enumerate(node_texCoord_mapping.outputs):
        print("node_texCoord_mapping.outputs >>>: ", i, o.name)

    # link = mat_links.new(node_texCoord_mapping.outputs[0], srcNode.inputs[0])
    return node_texCoord_mapping


def getShaderNodeFromNodeAt(currNode, linkIndex = 0):
    currLinks = currNode.links
    linksTotal = len(currLinks)
    # print("getShaderNodeFromNode(), A currNode          ###: ", currNode)
    # print("getShaderNodeFromNode(), A currNode.type          ###: ", currNode.type, ", linksTotal: ", linksTotal)
    if linksTotal > 0:
        currLink = currLinks[linkIndex]
        return currLink.from_node
    return None
def getSrcOriginNode(currNode):
    
    currLinks = currNode.links
    linksTotal = len(currLinks)
    # print("getSrcOriginNode(), A currNode          ###: ", currNode)
    # print("getSrcOriginNode(), A currNode.type          ###: ", currNode.type, ", linksTotal: ", linksTotal)
    if linksTotal > 0:
        currLink = currLinks[0]
        fromNode = currLink.from_node
        if fromNode is not None:
            # print("getSrcOriginNode(), B fromNode.type          ###: ", fromNode.type)
            pnode = fromNode.inputs[0]
            originNode = getSrcOriginNode(pnode)
            if originNode is not None:
                return originNode
            else:
                inputsTotal = len(fromNode.inputs)
                if inputsTotal > 1:
                    for i in range(1, inputsTotal):
                        pnode = fromNode.inputs[i]
                        originNode = getSrcOriginNode(pnode)
                        if originNode is not None:
                            return originNode

                return fromNode
        else:
            return currNode
    return None

def uvMappingLinkTexNode(mat_links, uvMappingNode, texNode):
    if texNode is not None:
        if texNode.type == "TEX_IMAGE":
            link = mat_links.new(uvMappingNode.outputs[0], texNode.inputs[0])
            return True
    return False

def updateMetalAndRoughness(mat_nodes, mat_links, metallicNode, roughnessNode, uvMappingNode,  metallic, roughness):
    ###
    metallic_origin_Node = getSrcOriginNode( metallicNode )
    roughness_origin_Node = getSrcOriginNode( roughnessNode )
    # print("metallic_origin_Node: ", metallic_origin_Node)
    # print(" metallic_origin_Node.type: ", metallic_origin_Node.type)
    # print("roughness_origin_Node: ", roughness_origin_Node)
    # print(" roughness_origin_Node.type: ", roughness_origin_Node.type)
    if metallic_origin_Node is not None and roughness_origin_Node is not None:
        print("has src origin node ...")
        if metallic_origin_Node == roughness_origin_Node:
            print("has same src origin node ...")
            uvMappingLinkTexNode(mat_links, uvMappingNode, metallic_origin_Node)
        else:
            uvMappingLinkTexNode(mat_links, uvMappingNode, metallic_origin_Node)
            uvMappingLinkTexNode(mat_links, uvMappingNode, roughness_origin_Node)
    elif metallic_origin_Node is not None:
        uvMappingLinkTexNode(mat_links, uvMappingNode, metallic_origin_Node)
        roughnessNode.default_value = roughness
    elif roughness_origin_Node is not None:        
        uvMappingLinkTexNode(mat_links, uvMappingNode, roughness_origin_Node)
        metallicNode.default_value = metallic
    else:
        metallicNode.default_value = metallic
        roughnessNode.default_value = roughness
    ###
    if metallic_origin_Node is not None and metallic_origin_Node.type == "TEX_IMAGE":
        print("add a multiply node for metallic node.")
        metallic_from_Node = getShaderNodeFromNodeAt(metallicNode, 0)
        print("metallic_from_Node >>>: ", metallic_from_Node)
        print("metallic_from_Node.type >>>: ", metallic_from_Node.type)
        # operation
        node_metallicMult = mat_nodes.new("ShaderNodeMath")
        node_metallicMult.operation = 'MULTIPLY'
        node_metallicMult.inputs[1].default_value = metallic
        prependInsertShaderNodeLink(mat_links, metallicNode, 0, node_metallicMult, 0,0, 0)
        # for i, o in enumerate(node_metallicMult.inputs):
        #     print("node_metallicMult.inputs >>>: ", i, o.name)
        # for i, o in enumerate(node_metallicMult.outputs):
        #     print("node_metallicMult.outputs >>>: ", i, o.name)
        # #prependInsertShaderNodeLink
    
    if roughness_origin_Node is not None and roughness_origin_Node.type == "TEX_IMAGE":
        print("add a multiply node for roughness node.")
        roughness_from_Node = getShaderNodeFromNodeAt(roughnessNode, 0)
        print("roughness_from_Node >>>: ", roughness_from_Node)
        print("roughness_from_Node.type >>>: ", roughness_from_Node.type)
        # operation
        node_roughnessMult = mat_nodes.new("ShaderNodeMath")
        node_roughnessMult.operation = 'MULTIPLY'
        node_roughnessMult.inputs[1].default_value = roughness
        prependInsertShaderNodeLink(mat_links, roughnessNode, 0, node_roughnessMult, 0,0, 0)

        # for i, o in enumerate(node_roughnessMult.inputs):
        #     print("node_roughnessMult.inputs >>>: ", i, o.name)
        # for i, o in enumerate(node_roughnessMult.outputs):
        #     print("node_roughnessMult.outputs >>>: ", i, o.name)
        # #prependInsertShaderNodeLink

def prependInsertShaderNodeLink(mat_links, currentNode, currNodeLinkIndex, newNode, outputIndex0, inputIndex0, outputIndex1):
    currLink = currentNode.links[currNodeLinkIndex]
    fromNode = currLink.from_node
    mat_links.remove(currLink)
    link0 = mat_links.new(fromNode.outputs[outputIndex0], newNode.inputs[inputIndex0])
    link1 = mat_links.new(newNode.outputs[outputIndex1], currentNode)

def appendInsertShaderNodeLink(mat_links, currentNode, currNodeLinkIndex, newNode, inputIndex0, outputIndex1, inputIndex1):
    currLink = currentNode.links[currNodeLinkIndex]
    toNode = currLink.to_node
    mat_links.remove(currLink)
    link0 = mat_links.new(currentNode, newNode.inputs[inputIndex0])
    link1 = mat_links.new(newNode.outputs[outputIndex1], toNode.inputs[inputIndex1])

def updateBaseColor(mat_nodes,mat_links, baseColorNode, uvMappingNode, baseColorRGB, baseColorAlpha):
    baseColorNode_origin_Node = getSrcOriginNode( baseColorNode )
    print("baseColorNode_origin_Node: ", baseColorNode_origin_Node)
    print("baseColorNode_origin_Node.type: ", baseColorNode_origin_Node.type)
    if uvMappingLinkTexNode(mat_links, uvMappingNode, baseColorNode_origin_Node):
        print("base color src data is a tex")
        node_colorMult = mat_nodes.new("ShaderNodeVectorMath")
        # node_colorMult = mat_nodes.new("ShaderNodeMath")

        # link = mat_links.new(srcNode.outputs[0], node_colorMult.inputs[0])
        # link_colorMult_and_baseColor = mat_links.new(node_colorMult.outputs[0], matNode.inputs["Base Color"])
        node_colorMult.operation = 'MULTIPLY'
        node_colorMult.inputs[1].default_value = baseColorRGB
        print("node_colorMult.type >>>: ", node_colorMult.type)
        print("node_colorMult.operation >>>: ", node_colorMult.operation)
        prependInsertShaderNodeLink(mat_links, baseColorNode, 0, node_colorMult, 0,0, 0)
    else:
        baseColorNode.default_value = (baseColorRGB, baseColorAlpha)

#
def updateAModelMaterialByName(modelName):
    # print("updateMeshesMaterial ops ...")
    # currObj = scene_objectDict["apple_body_model"]
    currObj = scene_objectDict[modelName]
    # currObj = bpy.context.scene.objects["apple_body"]
    print("         currObj: ", currObj)
    materials = currObj.data.materials
    print("         materials: ", materials)
    print("         materials[0]: ", materials[0])
    currMaterial = currObj.active_material
    print("         currMaterial: ", currMaterial)
    # print("updateMeshesMaterial currObj: ", currObj)
    currMaterial.use_nodes = True
    # nodes = currMaterial.node_tree.nodes
    
    mat_nodes = currMaterial.node_tree.nodes
    mat_links = currMaterial.node_tree.links
    principled_bsdf = mat_nodes.get("Principled BSDF")
    if principled_bsdf is None:
        principled_bsdf = mat_nodes.new(type="ShaderNodeBsdfPrincipled")
        print("         create a new Principled BSDF, principled_bsdf: ", principled_bsdf)
        material_output = mat_nodes.get("Material Output")
        if material_output is None:
            material_output = mat_nodes.new(type="ShaderNodeOutputMaterial")
        link = mat_links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])
    
    print("         principled_bsdf: ", principled_bsdf)
    matNode = mat_nodes[0]
    
    baseColorRGB = (1.0,0.2,2.1)
    baseColorAlpha = 1.0
    uvScales = (2.0,2.0, 1.0)
    metallicValue = 15.0
    roughnessValue = 0.2
    specularValue = 0.8

    baseColorNode = matNode.inputs['Base Color']
    metallicNode = matNode.inputs['Metallic']
    roughnessNode = matNode.inputs['Roughness']
    specularNode = matNode.inputs['Specular']
    normalNode = matNode.inputs['Normal']
    print("A 01 >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>")
    
    uvMappingNode = createUVShaderNode(mat_nodes, mat_links)
    uvMappingNode.inputs[3].default_value = uvScales

    # currLink = baseColorNode.links[0]
    # print("currLink >>>: ", currLink)
    # print("currLink.from_node >>>: ", currLink.from_node)
    # print("currLink.from_socket >>>: ", currLink.from_socket)
    print("A 02 >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>")
    updateBaseColor(mat_nodes,mat_links, baseColorNode, uvMappingNode, baseColorRGB, baseColorAlpha)

    # baseColorNode_origin_Node = getSrcOriginNode( baseColorNode )
    # print("baseColorNode_origin_Node: ", baseColorNode_origin_Node)
    # print("baseColorNode_origin_Node.type: ", baseColorNode_origin_Node.type)
    # if uvMappingLinkTexNode(mat_links, uvMappingNode, baseColorNode_origin_Node):
    #     print("base color src data is a tex")
    #     node_colorMult = mat_nodes.new("ShaderNodeVectorMath")
    #     # node_colorMult = mat_nodes.new("ShaderNodeMath")

    #     # link = mat_links.new(srcNode.outputs[0], node_colorMult.inputs[0])
    #     # link_colorMult_and_baseColor = mat_links.new(node_colorMult.outputs[0], matNode.inputs["Base Color"])
    #     node_colorMult.operation = 'MULTIPLY'
    #     node_colorMult.inputs[1].default_value = baseColorRGB
    #     print("node_colorMult.type >>>: ", node_colorMult.type)
    #     print("node_colorMult.operation >>>: ", node_colorMult.operation)
    #     # prependInsertShaderNodeLink(mat_links, currentNode, beginNodeLinkIndex, newNode, outputIndex0, inputIndex0, outputIndex1, inputIndex1)
    #     prependInsertShaderNodeLink(mat_links, baseColorNode, 0, node_colorMult, 0,0, 0)
    # else:
    #     baseColorNode.default_value = (baseColorRGB, baseColorAlpha)

    updateMetalAndRoughness(mat_nodes, mat_links, metallicNode, roughnessNode, uvMappingNode, metallicValue, roughnessValue)

    specularNode_origin_Node = getSrcOriginNode( specularNode )
    if not uvMappingLinkTexNode(mat_links, uvMappingNode, specularNode_origin_Node):
        specularNode.default_value = specularValue

    print("A 03 >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>> >>>")

    notmalStrength = 1.0
    normalNode_origin_Node = getSrcOriginNode( normalNode )
    print("normalNode_origin_Node: ", normalNode_origin_Node)
    print("normalNode_origin_Node.type: ", normalNode_origin_Node.type)
    if uvMappingLinkTexNode(mat_links, uvMappingNode, normalNode_origin_Node):
        normalMapNode = getShaderNodeFromNodeAt(normalNode, 0)
        if normalMapNode:
            # Strength
            # print("normalMapNode Strength: ", normalMapNode.inputs[0].default_value)
            normalMapNode.inputs[0].default_value = notmalStrength
            # for i, o in enumerate(normalMapNode.inputs):
            #     print("normalMapNode.inputs >>>: ", i, o.name)

    # blend_file_path = bpy.data.filepath
    # directory = os.path.dirname(blend_file_path)
    # target_file = os.path.join(directory, "D:/dev/webProj/voxblender/renderingImg/queryCurrMaterial.blend")
    # bpy.ops.wm.save_as_mainfile(filepath=target_file)
    
    # for i, o in enumerate(matNode.inputs):
    #     print("matNode.inputs >>>: ", i, o.name)
    # return
    # 金色
    # matNode.inputs['Base Color'].default_value = (0.8,0.3,0.0,1.0)
    # 紫水晶
    # matNode.inputs['Base Color'].default_value = (0.3,0.2,0.7,1.0)
    # matNode.inputs['Base Color'].default_value = (0.3,0.9,0.2,1.0)
    # matNode.inputs['Metallic'].default_value = 0.5
    
    # for i, o in enumerate(baseColorNode):
    # for k in baseColorNode:
    #     print("baseColorNode >>>: ", k, )

    # for i, o in enumerate(matNode.inputs):
    #     print("matNode.inputs >>>: ", i, o.name)

def updateMaterial():
    queryMaterials()
    # updateMeshesMaterial()
    updateAModelMaterialByName('apple_body_model')

if __name__ == "__main__":

    clearAllMeshesInScene()
    # modelUrl = rootDir + "voxblender/models/apple02.glb"
    modelUrl = rootDir + "voxblender/models/apple03.glb"
    loadModelWithUrl(modelUrl)
    print("#### ### #### ### ### ### ### ### ### ### ###")
    updateMaterial()
    render()
    print("queryCurrMaterial exec finish ...")

# D:\programs\blender\blender.exe -b -P .\queryCurrMaterial3.py