# nn_edit_cursor_by_gizmo
Addon to edit cursor by gizmo in Blender

## installation

Download the zip file from the release page and install it from Blender.
https://github.com/ichiyonnana/nn_edit_cursor_by_gizmo/releases

## usage

This add-on provides three operators:

- bpy.ops.view3d.nncursorutil_edit_cursor_by_gizmo_begin()

  Start editing the cursor.
  
- bpy.ops.view3d.nncursorutil_edit_cursor_by_gizmo_end()

  Finish editing the cursor.
  
- bpy.ops.view3d.nncursorutil_edit_cursor_by_gizmo_toggle()

  Starts editing the cursor or ends editing depending on the situation.

Assign a shortcut. Basically, you only need to register toggle(). Register begin()/end() only if you want to explicitly call the start and end.
