import bpy

def map_correct_materials(obj):
    print("Obj name: {}".format(obj.name))
    for m in obj.material_slots:
        print("Material name: {}".format(m.name))
        
        mat = m.material
        if mat.use_nodes == True:
            
            image_texture = mat.node_tree.nodes.get('Image Texture')
            roughness = mat.node_tree.nodes.get('Image Texture.001')
            normal_map = mat.node_tree.nodes.get('Normal Map')
#            displacement = mat.node_tree.nodes.get('Displacement')
            material_output = mat.node_tree.nodes.get('Material Output')
            diffuse = mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
            
            uv_map_node = mat.node_tree.nodes.new('ShaderNodeUVMap')
            uv_map_node.uv_map = "UVMap"
            normal_map.uv_map = "UVMap"


            # remap links and connect the diffuse shader to material
            mat.node_tree.links.new(uv_map_node.outputs['UV'], image_texture.inputs['Vector'])
            mat.node_tree.links.new(diffuse.inputs['Color'], image_texture.outputs['Color'])
            mat.node_tree.links.new(diffuse.inputs['Roughness'], roughness.outputs['Color'])
            mat.node_tree.links.new(diffuse.inputs['Normal'], normal_map.outputs['Normal'])
            mat.node_tree.links.new(material_output.inputs[0], diffuse.outputs[0])
            
            # Remove default
            mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Principled BSDF')) #title of the existing node when materials.new

            # set activer material to your new material
            obj.active_material = mat
            

objs = [o for o in bpy.data.objects
    if o.type == 'MESH' and "Floor" in o.name and not "Light" in o.name]
    
for obj in objs:
    map_correct_materials(obj)