import bpy
import json

def write_some_data(context, filepath, export_items):
    print("Exporting Godot Curves")
    f = open(filepath, "w", encoding='utf-8')
    
    data = {"curve_list": []}
    curve_list = data["curve_list"]
    iter_list = []
    if export_items == "SELECTED":
       iter_list = context.selected_objects
    elif export_items == "COLLECTION":
        iter_list = context.view_layer.active_layer_collection.collection.objects
    else:
        iter_list = bpy.data.objects
    for curve in iter_list:
        if curve.type == "CURVE":
            data_name = curve.name
            curve_list.extend(parse_curve(curve.data, data_name))

    f.write(json.dumps(data, indent=4))
    f.close()

    return {'FINISHED'}

# returns array of splines in curve
def parse_curve(obj, name):
    if not type(obj) is bpy.types.Curve:
        return [str(type(obj))]
    list = []
    for index in range(len(obj.splines)):
        spline = obj.splines[index]
        if spline.type != "BEZIER":
            continue
        item_name = name
        if index != 0:
            item_name = f"{name}_{index}"
        is_closed = spline.use_cyclic_u
        list.append({
            "name": item_name,
            "is_closed": is_closed,
            "data": parse_spline(spline)
        })
    return list
    
# returns data set for single spline
def parse_spline(obj):
    if not type(obj) is bpy.types.Spline:
        return []
    point_list = []
    for point in obj.bezier_points:
        point_list.append({
            "pos": [point.co.x, point.co.y, point.co.z],
            "left": [point.handle_left.x, point.handle_left.y, point.handle_left.z],
            "right": [point.handle_right.x, point.handle_right.y, point.handle_right.z],
            "tilt": point.tilt
        })
    return point_list

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class GodotCurveExport(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "godot_curve_export.file_export"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Godot Curve Export for Bezier Curves ONLY"

    # ExportHelper mix-in class uses this.
    filename_ext = ".godot_curve"

    filter_glob: StringProperty(
        default="*.godot_curve",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
#    use_setting: BoolProperty(
#        name="Example Boolean",
#        description="Example Tooltip",
#        default=True,
#    )

#    type: EnumProperty(
#        name="Example Enum",
#        description="Choose between two items",
#        items=(
#            ('OPT_A', "First Option", "Description one"),
#            ('OPT_B', "Second Option", "Description two"),
#        ),
#        default='OPT_A',
#    )
    
    items: EnumProperty(
        name="Export",
        description="Which items to export",
        items=(
            ("SELECTED", "Selected Items", "Export only selected items"),
            ("COLLECTION", "Collection", "Export curves in selected collection"),
            ("ALL", "All", "Export all curves in this file"),
        ),
        default="SELECTED",
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.items)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(GodotCurveExport.bl_idname, text="Godot Curve (.godot_curve)")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(GodotCurveExport)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(GodotCurveExport)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

bl_info = {
    "name": "Happy Golem Blender Utilities",
    "blender": (4, 4, 1),
    "category": "Utilities"
}

if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.godot_curve_export.file_export('INVOKE_DEFAULT')
