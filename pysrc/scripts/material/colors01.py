import bpy

hex_val1 = 0xFDF8E2
hex_val2 = 0xFFDDD3
hex_val3 = 0xF3BF3B
hex_val4 = 0x5EA9EB
hex_val5 = 0x9ACDE0
hex_val6 = 0xCBE1EF

metallic_all = 1.0
roughness_all = 0.312

mat_1 = bpy.data.materials.new("yellow")
mat_1.use_nodes = True
mat_2 = bpy.data.materials.new("pink")
mat_2.use_nodes = True
mat_3 = bpy.data.materials.new("beige")
mat_3.use_nodes = True
mat_4 = bpy.data.materials.new("turq")
mat_4.use_nodes = True
mat_5 = bpy.data.materials.new("lightblue")
mat_5.use_nodes = True
mat_6 = bpy.data.materials.new("sky")
mat_6.use_nodes = True

def srgb_to_linearrgb(c):
    if   c < 0:       return 0
    elif c < 0.04045: return c/12.92
    else:             return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h,alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])

bpy.data.materials[str(mat_1.name)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val1)
bpy.data.materials[str(mat_2.name)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val2)
bpy.data.materials[str(mat_3.name)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val3)
bpy.data.materials[str(mat_4.name)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val4)
bpy.data.materials[str(mat_5.name)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val5)
bpy.data.materials[str(mat_6.name)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val6)

bpy.data.materials[str(mat_1.name)].node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all
bpy.data.materials[str(mat_2.name)].node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all 
bpy.data.materials[str(mat_3.name)].node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all 
bpy.data.materials[str(mat_4.name)].node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all 
bpy.data.materials[str(mat_5.name)].node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all 
bpy.data.materials[str(mat_6.name)].node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all 

bpy.data.materials[str(mat_1.name)].node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all
bpy.data.materials[str(mat_2.name)].node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all
bpy.data.materials[str(mat_3.name)].node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all
bpy.data.materials[str(mat_4.name)].node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all
bpy.data.materials[str(mat_5.name)].node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all
bpy.data.materials[str(mat_6.name)].node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all