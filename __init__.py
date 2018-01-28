bl_info = {
    "name": "NinjaRipper rip importer",
    "author": "RED_EYE",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "location": "File > Import-Export > NinjaRipper RIP (.rip) ",
    "description": "Addon allows to import NinjaRippper meshes",
    #'warning': 'May crash blender',
    # "wiki_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    # "tracker_url": "http://www.barneyparker.com/blender-json-import-export-plugin",
    "category": "Import-Export"}
from . import io_RIP

if "bpy" in locals():
    import importlib

    # if "export_json" in locals():
    #    importlib.reload(export_json)
    if "io_RIP" in locals():
        importlib.reload(io_RIP)
else:
    import bpy

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ExportHelper


class RIPImporter(bpy.types.Operator):
    """Load Source Engine MDL models"""
    bl_idname = "import_mesh.rip"
    bl_label = "Import rip"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )


    def execute(self, context):
        from . import io_RIP
        io_RIP.IO_RIP(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(RIPImporter.bl_idname, text="RIP mesh (.RIP)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_import.append(menu_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
