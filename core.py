import bpy

from .nnutil import *

# object name
name = "NNCursorEditor"

# property key name
kn_active_object = "active_object"
kn_selected_objects = "selected_objects"
kn_current_mode = "current_mode"
kn_current_orientation = "current_orientation"
kn_current_pivot = "current_pivot"

class NNCURSORUTIL_OT_EditCursorByGizmoBegin(bpy.types.Operator):
    """
    begin cursor editing
    """
    bl_idname = "view3d.nncursorutil_edit_cursor_by_gizmo_begin"
    bl_label = "edit cursor by gizmo"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if name in bpy.data.objects:
            empty_object = bpy.data.objects[name]
            bpy.data.objects.remove(empty_object)

        # get current status
        active_object = get_active_object()
        selected_objects = get_selected_objects()
        current_mode = get_mode()
        current_orientation = bpy.context.scene.transform_orientation_slots[0].type
        current_pivot = bpy.context.scene.tool_settings.transform_pivot_point
        enable_object_mode()

        # create empty and hide cursor
        bpy.context.space_data.overlay.show_cursor = False
        bpy.ops.object.empty_add(type='ARROWS', align='CURSOR')
        empty_object = bpy.context.active_object
        empty_object.name = name

        # save status to empty
        add_custom_property(empty_object, kn_active_object, active_object)
        add_custom_property(empty_object, kn_selected_objects, selected_objects)
        add_custom_property(empty_object, kn_current_mode, current_mode)
        add_custom_property(empty_object, kn_current_orientation, current_orientation)
        add_custom_property(empty_object, kn_current_pivot, current_pivot)

        # set select-tool
        bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
        bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
        bpy.ops.wm.tool_set_by_id(name="builtin.move")

        return {"FINISHED"}


class NNCURSORUTIL_OT_EditCursorByGizmoEnd(bpy.types.Operator):
    """
    end cursor editing
    """
    bl_idname = "view3d.nncursorutil_edit_cursor_by_gizmo_end"
    bl_label = "edit cursor by gizmo"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    restore : bpy.props.BoolProperty(default=False)

    def execute(self, context):
        if not name in bpy.data.objects:
            return {"FINISHED"}

        # set transform to cursor
        bpy.context.space_data.overlay.show_cursor = True
        empty_object = bpy.data.objects[name]
        bpy.context.scene.cursor.matrix = empty_object.matrix_world

        # get saved status
        active_object = empty_object[kn_active_object]
        selected_objects = empty_object[kn_selected_objects]
        current_mode = empty_object[kn_current_mode]

        # restore status
        activate_object(empty_object[kn_active_object])
        select_objects(empty_object[kn_selected_objects])
        set_mode(empty_object[kn_current_mode])

        if self.restore:
            bpy.context.scene.transform_orientation_slots[0].type = empty_object[kn_current_orientation]
            bpy.context.scene.tool_settings.transform_pivot_point = empty_object[kn_current_pivot]

        else:
            bpy.context.scene.transform_orientation_slots[0].type = 'CURSOR'
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'

        bpy.data.objects.remove(empty_object)

        return {"FINISHED"}


class NNCURSORUTIL_OT_EditCursorByGizmoToggle(bpy.types.Operator):
    """
    toggle cursor editing
    """
    bl_idname = "view3d.nncursorutil_edit_cursor_by_gizmo_toggle"
    bl_label = "edit cursor by gizmo"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    restore : bpy.props.BoolProperty(default=False)

    def execute(self, context):
        # object name
        name = "NNCursorEditor"

        # property key name
        kn_active_object = "active_object"
        kn_selected_objects = "selected_objects"
        kn_current_mode = "current_mode"
        kn_current_orientation = "current_orientation"
        kn_current_pivot = "current_pivot"

        if not name in bpy.data.objects:
            # begin editing
            bpy.ops.view3d.nncursorutil_edit_cursor_by_gizmo_begin()

        else:
            # end editing
            bpy.ops.view3d.nncursorutil_edit_cursor_by_gizmo_end(restore=self.restore)

        return {"FINISHED"}

