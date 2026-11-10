"""Small Blender helpers for the Roblox art pipeline. Import them; this file does nothing when run.

Use from a Blender Python console, a Blender MCP `execute` call, or another script:

    import sys; sys.path.append("<path to this skill>/scripts/blender")
    import modeling_helpers as mh
    mh.make_col(bpy.data.objects["SM_Prop_Barrel_A"])           # adds SM_Prop_Barrel_A_COL
    mh.palette_uv(obj, {"M_Wood": (0, 0), "M_Metal": (3, 1)})    # snap faces to palette cells
    print(mh.spend_report(obj), mh.symmetry_error(obj), mh.tri_count(obj))

Functions
  tri_count(obj)        triangles after modifiers
  make_col(obj)         convex-hull collision proxy named <obj>_COL, parented to obj, no material
  palette_uv(obj, ...)  collapse a multi-material mesh onto one palette-atlas material
  spend_report(obj)     (triangles, {"up": %, "down": %, "side": %}) by face area
  symmetry_error(obj)   worst X-mirror mismatch as a fraction of the largest dimension
  thin_triangles(obj)   count of triangles with an aspect ratio above 8:1
  open_edges(obj)       count of non-manifold edges (0 means watertight)

Safety: no network access, no file writes, nothing beyond bpy, bmesh and mathutils.
make_col and palette_uv change the open scene (they add an object or edit UVs and materials);
the others only read.

Tested 2026-11-10 with the standalone `bpy` 5.2.3 LTS module: every function was called on
test meshes (bevelled cube, 12-sided cylinder, icosphere) and the results checked by hand
(a size-2 cube with a 0.1 one-segment bevel reports 44 triangles and 19/19/62 % up/down/side; a mirrored build reports
symmetry error 0.0; an open-bottomed cylinder reports 12 open edges).
Not tested: the Blender desktop binary, other Blender versions, meshes with shape keys.
"""
import bmesh
import bpy
from mathutils import Vector, kdtree


def _evaluated_bmesh(obj, triangulate=False):
    bm = bmesh.new()
    bm.from_object(obj, bpy.context.evaluated_depsgraph_get())
    if triangulate:
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
    return bm


def tri_count(obj):
    bm = _evaluated_bmesh(obj)
    n = sum(len(f.verts) - 2 for f in bm.faces)
    bm.free()
    return n


def make_col(obj, angle=0.09):
    """Convex-hull proxy for convex props. Studio side: CollisionFidelity = Hull on the proxy.
    `angle` (radians) merges near-coplanar hull faces. Concave assets need hand-made pieces."""
    bm = _evaluated_bmesh(obj)
    bmesh.ops.delete(bm, geom=bm.faces[:], context="FACES_ONLY")
    bmesh.ops.convex_hull(bm, input=bm.verts[:])
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
    bmesh.ops.dissolve_limit(bm, angle_limit=angle, verts=bm.verts[:], edges=bm.edges[:])
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(obj.name + "_COL")
    bm.to_mesh(mesh)
    bm.free()
    col = bpy.data.objects.new(obj.name + "_COL", mesh)
    obj.users_collection[0].objects.link(col)
    col.parent = obj
    col.display_type = "WIRE"
    return col


def palette_uv(obj, swatch, grid=16, material="M_Palette"):
    """Snap every face's UVs to the centre of its material's palette cell, then keep one material.
    swatch maps material name -> (column, row), counted from the top-left of a grid x grid atlas.
    The material named `material` must already exist."""
    uv = obj.data.uv_layers.active.data
    for poly in obj.data.polygons:
        column, row = swatch[obj.material_slots[poly.material_index].material.name]
        for loop_index in poly.loop_indices:
            uv[loop_index].uv = ((column + 0.5) / grid, 1 - (row + 0.5) / grid)
        poly.material_index = 0
    obj.data.materials.clear()
    obj.data.materials.append(bpy.data.materials[material])


def spend_report(obj):
    """Where the triangles face. A grounded prop should show about 0 % down."""
    bm = _evaluated_bmesh(obj, triangulate=True)
    area = {"up": 0.0, "down": 0.0, "side": 0.0}
    for f in bm.faces:
        key = "up" if f.normal.z > 0.5 else "down" if f.normal.z < -0.5 else "side"
        area[key] += f.calc_area()
    total = sum(area.values()) or 1.0
    tris = len(bm.faces)
    bm.free()
    return tris, {k: round(100 * v / total) for k, v in area.items()}


def symmetry_error(obj):
    """0.0 for a half-plus-mirror build. Above about 0.01 a symmetric-by-design prop is lopsided."""
    coords = [v.co.copy() for v in obj.data.vertices]
    tree = kdtree.KDTree(len(coords))
    for i, co in enumerate(coords):
        tree.insert(co, i)
    tree.balance()
    worst = max(tree.find(Vector((-co.x, co.y, co.z)))[2] for co in coords)
    return worst / max(max(obj.dimensions), 1e-9)


def thin_triangles(obj, max_aspect=8.0):
    bm = _evaluated_bmesh(obj, triangulate=True)
    count = 0
    for f in bm.faces:
        lengths = sorted(e.calc_length() for e in f.edges)
        if lengths[0] <= 1e-9 or lengths[2] / lengths[0] > max_aspect:
            count += 1
    bm.free()
    return count


def open_edges(obj):
    bm = _evaluated_bmesh(obj)
    count = sum(1 for e in bm.edges if not e.is_manifold)
    bm.free()
    return count
