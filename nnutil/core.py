
import math
import re
import copy

from itertools import *

import bpy
import bmesh

CT_VERTEX = "CTVERTEX"
CT_EDGE = "CT_EDGE"
CT_FACE = "CT_FACE"
CT_AUTO = "CT_AUTO"
CT_ALL = "CT_ALL"

OBJECT = "OBJECT"
COMPONENT = "COMPONENT"

MD_OBJECT = "OBJECT"
MD_EDIT = "EDIT"
MD_SCULPT = "SCULPT"

CMD_EDIT_MESH = "EDIT_MESH"
CMD_EDIT_CURVE = "EDIT_CURVE"
CMD_POSE = "POSE"

# Space type
ST_VIEW_3D = "VIEW_3D"
ST_OUTLINER = "OUTLINER"
ST_PROPERTIES = "PROPERTIES"
ST_CONSOLE = "CONSOLE"
ST_TEXT_EDITOR = "TEXT_EDITOR"
ST_INFO = "INFO"
ST_FILE_BROWSER = "FILE_BROWSER"
ST_PREFERENCES = "PREFERENCES"

# Object type
OT_MESH = "MESH"
OT_ARMATURE = "ARMATURE"

# Modifier Types
MDT_ARMATURE = "ARMATURE"

# Pose positions
PP_REST = "REST"
PP_POSE = "POSE"



def flatten(a):
    from itertools import chain
    return list(chain.from_iterable(a))

def uniq(a):
    if not a:
        return a
    elemtype = type(a[0])
    string_types = [type(""), type(u"")] # Supports python2.x and python3.x
    if elemtype in string_types:
        elements_tuple_list = list(set([tuple(x) for x in a]))
        return ["".join(elements_tuple) for elements_tuple in elements_tuple_list]
    else:
        return list(set(a))

def uniq_flatten(a):
    return uniq(flatten(a))

def get_all_screens():
    ret = []

    for screen in bpy.context.workspace.screens:
        ret.append(screen)

    return ret

def get_all_areas():
    ret = []

    for screen in bpy.context.workspace.screens:
        for area in screen.areas:
            ret.append(area)

    return ret

def get_all_spaces():
    ret = []

    for screen in bpy.context.workspace.screens:
        for area in screen.areas:
            for space in area.spaces:
                ret.append(space)

    return ret


def get_specified_type_spaces(specified_type=ST_VIEW_3D):
    """指定したタイプのスペース取得"""
    match_spaces = []

    for screen in bpy.context.workspace.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == specified_type:
                    match_spaces.append(space)

    return match_spaces

def all_3dview_spaces():
    return get_specified_type_spaces(specified_type=ST_VIEW_3D)

def get_mode():
    if bpy.context.active_object:
        return bpy.context.active_object.mode
    else:
        return MD_OBJECT

def set_mode(mode):
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode=mode, toggle=False)

def is_object_mode():
    return bpy.context.mode == "OBJECT"

def is_edit_mode():
    return "EDIT_" in bpy.context.mode

def is_sculpt_mode():
    return bpy.context.mode == "SCULPT"

def enable_object_mode():
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

def enable_edit_mode():
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

def enable_sculpt_mode():
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode='SCULPT', toggle=False)

def enable_pose_mode():
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode='POSE', toggle=False)

def enable_select_mode():
    bpy.ops.wm.tool_set_by_id(name="builtin.select_box", space_type='VIEW_3D')

def get_select_mask_v():
    v, e, f = bpy.context.tool_settings.mesh_select_mode
    return v

def get_select_mask_e():
    v, e, f = bpy.context.tool_settings.mesh_select_mode
    return e

def get_select_mask_f():
    v, e, f = bpy.context.tool_settings.mesh_select_mode
    return f

def set_select_mask_v():
    bpy.context.tool_settings.mesh_select_mode = (True, False, False)

def set_select_mask_e():
    bpy.context.tool_settings.mesh_select_mode = (False, True, False)

def set_select_mask_f():
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)

def get_active_space():
    return bpy.context.space_data

def get_active_screen():
    return bpy.context.screen

def is_3dview():
    return bpy.context.space_data.type == "VIEW_3D"

def is_localview(space=None):
    if not space:
        space = bpy.context.space_data

    return space.local_view

def enable_localview(space=None):
    if not space:
        space = bpy.context.space_data

    if not space.local_view:
        bpy.ops.view3d.localview(frame_selected=False)

def disable_localview(space=None):
    if not space:
        space = bpy.context.space_data

    if space.local_view:
        bpy.ops.view3d.localview(frame_selected=False)

def toggle_localview(space=None):
    if not space:
        space = bpy.context.space_data

    bpy.ops.view3d.localview(frame_selected=False)

def get_selections(component_type=CT_AUTO):
    current_mode = get_mode()

    if is_object_mode():
        return bpy.context.selected_objects

    if is_edit_mode():
        set_mode(MD_OBJECT)
        components = []
        active_object = get_active_object()
        selected_objects = get_selected_objects()
        target_objects = list(set(selected_objects + [active_object]))

        v = flatten([[x for x in obj.data.vertices if x.select] for obj in target_objects])
        e = flatten([[x for x in obj.data.edges if x.select]  for obj in target_objects])
        f = flatten([[x for x in obj.data.polygons if x.select]  for obj in target_objects])

        if component_type == CT_VERTEX:
            components = v

        elif component_type == CT_EDGE:
            components = e

        elif component_type == CT_FACE:
            components = f

        elif component_type == CT_AUTO:
            if get_select_mask_v():
                components.extend(v)

            if get_select_mask_e():
                components.extend(e)

            if get_select_mask_f():
                components.extend(f)

        set_mode(current_mode)

        return components

def add_custom_property(obj, key, value):
    obj[key] = value

def has_custom_property(obj, key):
    return key in dict(obj).keys()


def activate_object(object):
    bpy.context.view_layer.objects.active = object

def select_objects(objects):
    for obj in objects:
        obj.select_set(True)

def select_components(components):
    current_mode = get_mode()
    enable_object_mode()

    for x in components:
        x.select = True

    set_mode(current_mode)

def select_faces_bm(components):
    if is_edit_mode():
        for comp in components:
            obj = get_active_object()#to_object(comp)
            meshdata = obj.data
            bm = bmesh.from_edit_mesh(meshdata)
            bm.faces.ensure_lookup_table()

            if isinstance(comp, bpy.types.MeshPolygon):
                bm.faces[comp.index].select = True

            bmesh.update_edit_mesh(meshdata, True)

def select_all():
    if is_object_mode():
        bpy.ops.object.select_all(action='SELECT')

    elif bpy.context.mode == CMD_EDIT_MESH:
        bpy.ops.mesh.select_all(action='SELECT')

    elif bpy.context.mode == CMD_EDIT_CURVE:
        bpy.ops.curve.select_all(action='SELECT')

    elif bpy.context.mode == CMD_POSE:
        bpy.ops.pose.select_all(action='SELECT')

def deselect_all():
    if is_object_mode():
        bpy.ops.object.select_all(action='DESELECT')

    elif bpy.context.mode == CMD_EDIT_MESH:
        bpy.ops.mesh.select_all(action='DESELECT')

    elif bpy.context.mode == CMD_EDIT_CURVE:
        bpy.ops.curve.select_all(action='DESELECT')

def all_components(obj):
    return list(obj.data.vertices) + list(obj.data.edges) + list(obj.data.polygons)

def to_object(component):
    """
    引数のコンポーネントが所属するオブジェクトを取得する
    インスタンスコピーがある場合は最初にヒットしたオブジェクトが返される
    検索順は アクティブオブジェクト、選択オブジェクト、シーンすべてのオブジェクトの順番でヒット次第打ち切り
    """

    active_object = get_active_object()
    selected_objects = get_selected_objects()
    all_objects = bpy.data.objects

    if component in all_components(active_object):
        return active_object

    for obj in selected_objects:
        if component in all_components(obj):
            return obj

    for obj in all_objects:
        if component in all_components(obj):
            return obj

    return None

def get_active_object():
    return bpy.context.active_object

def get_selected_objects():
    return bpy.context.selected_objects

def is_vertex(component):
    return isinstance(component, bpy.types.MeshVertex)

def is_edge(component):
    return isinstance(component, bpy.types.MeshEdge)

def is_polygon(component):
    return isinstance(component, bpy.types.MeshPolygon)

def to_index(components):
    """
    コンポーネントを頂点インデックスの Set に変換する
    """
    if not components:
        return []

    if is_vertex(components[0]):
        return [x.index for x in components]
    if is_edge(components[0]):
        return [set(x.vertices) for x in components]
    if is_polygon(components[0]):
        return [set(x.vertices) for x in components]

def vertex_from_index(index, obj=None):
    if not obj:
        obj = get_active_object()

    return obj.data.vertices[index]

def edge_from_index_pair(index_pair, obj=None):
    if not obj:
        obj = get_active_object()

    for e in obj.data.edges:
        if set(e.vertices) == set(index_pair):
            return e

def face_from_index_pair(index_pair, obj=None):
    if not obj:
        obj = get_active_object()

    for p in obj.data.polygons:
        if set(p.vertices) == set(index_pair):
            return p

def to_vertex(components, obj=None, greedy=True):
    """
    from v
        components をそのまま返す
    from e
        エッジの構成頂点を返す
    from f
        フェースの構成頂点を返す
    """
    if not obj:
        obj = get_active_object()

    vertices = [x for x in components if type(x) == bpy.types.MeshVertex]
    edges = [x for x in components if type(x) == bpy.types.MeshEdge]
    polygons = [x for x in components if type(x) == bpy.types.MeshPolygon]

    ret = []

    # v to v
    ret.extend(vertices)
    # e to v
    ret.extend(uniq(flatten([[obj.data.vertices[vi] for vi in e.vertices] for e in edges])))
    # f to v
    ret.extend(uniq(flatten([[obj.data.vertices[vi] for vi in p.vertices] for p in polygons])))

    return ret

def to_edge(components, obj=None, greedy=True):
    """
    from v
        構成頂点として components を一つでも含むエッジを返す
    from e
        components をそのまま返す
    from f
        フェースの構成エッジをすべて返す
    """
    if not obj:
        obj = get_active_object()

    vertices = [x for x in components if type(x) == bpy.types.MeshVertex]
    edges = [x for x in components if type(x) == bpy.types.MeshEdge]
    polygons = [x for x in components if type(x) == bpy.types.MeshPolygon]

    ret = []

    # v to e
    ret.extend([x for x in obj.data.edges if set(x.vertices) & set(to_index(vertices))])
    # e to e
    ret.extend(edges)
    # f to e
    ret.extend(uniq(flatten([[edge_from_index_pair(edge_keys) for edge_keys in p.edge_keys] for p in polygons])))

    return ret

def to_face(components, obj=None, greedy=True):
    """
    from v
        構成頂点として components を一つでも含むフェースを返す
    from e
        構成エッジとして components を一つでも含むフェースを返す
    from f
        components をそのまま返す
    """
    if not obj:
        obj = get_active_object()

    vertices = [x for x in components if type(x) == bpy.types.MeshVertex]
    edges = [x for x in components if type(x) == bpy.types.MeshEdge]
    polygons = [x for x in components if type(x) == bpy.types.MeshPolygon]

    ret = []

    # v to f
    ret.extend([p for p in obj.data.polygons if set(p.vertices) & set(to_index(vertices))])
    # e to f
    ret.extend([p for p in obj.data.polygons if set([edge_from_index_pair(index_pair) for index_pair in p.edge_keys]) & set(edges)])
    # f to f
    ret.extend(polygons)

    return ret


def edges_to_vertices(edges, obj):
    vertex_indicies = edges_to_vertex_indicies(edges)

    return [vertex_from_index(i, obj) for i in vertex_indicies]

def edges_to_vertex_indicies(edges):
    vertex_indicies = []
    first_vtx = list(set(edges[0].vertices) - set(edges[1].vertices))[0]
    last_vtx = list(set(edges[-1].vertices) - set(edges[-2].vertices))[0]

    for i in range(len(edges)-1):
        vertex_indicies.append(list(set(edges[i].vertices) & set(edges[i+1].vertices))[0])

    vertex_indicies = [first_vtx] + vertex_indicies + [last_vtx]

    return vertex_indicies

def get_adjacent_edges(edge, edges):
    return [e for e in edges if set(edge.vertices) & set(e.vertices)]

def get_all_polyedges(edges):
    """
    edges を連続するエッジのまとまりとしてエッジリストを一つ返す
    """

    obj = to_object(edges[0])
    all_edges = obj.data.edges

    # detect end edge
    end_edges = []
    for e in edges:
        other_edges = list(set(edges) - set([e]))
        other_vertices = uniq_flatten([e.vertices for e in other_edges])

        if len(set(e.vertices) & set(other_vertices)) == 1:
            end_edges.append(e)

    rest_edges = copy.copy(edges)
    polyedge_list = []

    for end_edge in end_edges:
        if not end_edge in rest_edges:
            continue

        polyedge = [end_edge]
        rest_edges.remove(end_edge)

        adjacent_edges = get_adjacent_edges(end_edge, rest_edges)

        while(adjacent_edges):
            adjacent_edge = adjacent_edges[0]
            polyedge.append(adjacent_edge)
            rest_edges.remove(adjacent_edge)
            adjacent_edges = get_adjacent_edges(adjacent_edge, rest_edges)

        polyedge_list.append(polyedge)

    return polyedge_list

def reset_normal(objects=[]):
    """
    ノーマルを初期化する
    """
    active_object = get_active_object()
    selected_objects = get_selected_objects()

    if not objects:
        objects = selected_objects
        if active_object:
            objects.append(active_object)

    current_mode = get_mode()

    for obj in objects:
        if not obj.type == OT_MESH:
            continue

        activate_object(obj)
        obj.data.use_auto_smooth = True
        obj.data.auto_smooth_angle = 3.14159
        enable_edit_mode()
        set_select_mask_f()
        select_all()
        bpy.ops.mesh.faces_shade_smooth()

    deselect_all()
    set_mode(current_mode)
    select_objects(selected_objects)
    activate_object(active_object)


def is_center_shapekey(name):
    return re.search(r"_C$", name)

def get_left_keyname(name):
    return re.sub(r"_C$", "_L", name)

def get_right_keyname(name):
    return re.sub(r"_C$", "_R", name)

def get_shapekey_index_from_name(obj, name):
    return obj.data.shape_keys.key_blocks.keys().index(name)

def activate_shapekey_from_name(obj, name):
    obj.active_shape_key_index =  get_index_from_name(obj, name)

def exists_shapekey(obj, name):
    return name in obj.data.shape_keys.key_blocks

def add_shapekey(obj, name):
    if not exists_key(obj=obj, name=name):
        return obj.shape_key_add(name=name)
    
    return None
    
def is_armature(obj):
    return obj.type == OT_ARMATURE

def get_all_armatures():
    return [obj for obj in bpy.data.objects if is_armature(obj)]

def get_all_modifires(obj):
    return obj.modifiers

def get_bound_armatures(obj):
    if is_armature(obj):
        return [obj]

    armature_modifier_list = [obj for obj in obj.modifiers if obj.type == MDT_ARMATURE]
    armature_object_list = [modifier.object for modifier in armature_modifier_list if not modifier.object == None]

    return armature_object_list

def toggle_armature_pose_position(armature):
    if armature.data.pose_position == PP_POSE:
        armature.data.pose_position = PP_REST
    else:
        armature.data.pose_position = PP_POSE

def toggle_object_pose_position(obj=None):

    if not obj:
        obj = get_active_object()

        if not obj:
            return

    armatures = []

    if is_armature(obj):
        armatures = [obj]
    else:
        armatures = get_bound_armatures(obj)

    for armature in armatures:
        toggle_armature_pose_position(armature)

def go_to_bindpose(obj=None):
    current_mode = get_mode()

    if not obj:
        obj = get_active_object()

        if not obj:
            return

    armatures = get_bound_armatures(obj)

    for armature in armatures:
        enable_object_mode()
        deselect_all()
        activate_object(armature)
        enable_pose_mode()
        select_all()
        bpy.ops.pose.transforms_clear()

    set_mode(current_mode)

