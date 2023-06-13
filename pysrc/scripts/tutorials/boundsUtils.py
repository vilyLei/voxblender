#!/usr/bin/python
# -*- coding: UTF-8 -*-

import bpy
import mathutils
import bmesh
from bpy_extras import object_utils

# from blender templates
def add_box(width, height, depth):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = [(+1.0, +1.0, -1.0),
             (+1.0, -1.0, -1.0),
             (-1.0, -1.0, -1.0),
             (-1.0, +1.0, -1.0),
             (+1.0, +1.0, +1.0),
             (+1.0, -1.0, +1.0),
             (-1.0, -1.0, +1.0),
             (-1.0, +1.0, +1.0),
             ]

    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7),
            ]

    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces


def createBoundsFrameBox(minV, maxV):
    minx = minV[0]
    miny = minV[1]
    minz = minV[2]
    maxx = maxV[0]
    maxy = maxV[1]
    maxz = maxV[2]
    verts_loc, faces = add_box((maxx-minx)/2, (maxz-minz)/2, (maxy-miny)/2)
    mesh = bpy.data.meshes.new("BoundingBox")
    bm = bmesh.new()
    for v_co in verts_loc:
        bm.verts.new(v_co)

    bm.verts.ensure_lookup_table()

    for f_idx in faces:
        bm.faces.new([bm.verts[i] for i in f_idx])

    bm.to_mesh(mesh)
    mesh.update()
    
    location = [0.0,]*3
    location[0] = minx+((maxx-minx)/2)
    location[1] = miny+((maxy-miny)/2)
    location[2] = minz+((maxz-minz)/2)
    bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)
    # does a bounding box need to display more than the bounds??
    bbox.location = location
    bbox.display_type = 'BOUNDS'
    bbox.hide_render = True