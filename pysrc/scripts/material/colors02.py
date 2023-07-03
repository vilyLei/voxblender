import bpy

hex_vals = (0xFDF8E2, 0xFFDDD3, 0xF3BF3B, 0x5EA9EB, 0x9ACDE0, 0xCBE1EF)
mat_names = ("yellow", "pink", "beige", "turq", "lightblue", "sky")

metallic_all = 1.0
roughness_all = 0.312

def srgb_to_linearrgb(c):
    if   c < 0:       return 0
    elif c < 0.04045: return c/12.92
    else:             return ((c+0.055)/1.055)**2.4

def hex_to_rgb(h,alpha=1):
    r = (h & 0xff0000) >> 16
    g = (h & 0x00ff00) >> 8
    b = (h & 0x0000ff)
    return tuple([srgb_to_linearrgb(c/0xff) for c in (r,g,b)] + [alpha])

for mat_name, hex_val in zip(mat_names, hex_vals):
    mat = bpy.data.materials.new(mat_name)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = hex_to_rgb(hex_val)
    mat.node_tree.nodes["Principled BSDF"].inputs[6].default_value = metallic_all
    mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = roughness_all