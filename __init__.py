# import RIP_Utilities
from pathlib import Path

from .ByteIO_nr import ByteIO

bl_info = {
    "name": "NinjaRipper rip importer",
    "author": "RED_EYE",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "location": "File > Import-Export > NinjaRipper RIP (.rip) ",
    "description": "Addon allows to import NinjaRippper meshes",
    # 'warning': 'May crash blender',
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

from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy_extras.io_utils import ExportHelper
import os


class RIPImporter(bpy.types.Operator):
    """Load Source Engine MDL models"""
    bl_idname = "import_mesh.rip"
    bl_label = "Import rip"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    files = CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)

    uv_scale = bpy.props.FloatProperty(name='UV scale', default=1.0)
    invert_uv = bpy.props.BoolProperty(name='Invert UV', default=False)
    vertex_scale = bpy.props.FloatProperty(name='Vertex scale', default=1.0)
    auto_center = bpy.props.BoolProperty(name='Auto center model?', default=True)

    def execute(self, context):
        from . import io_RIP
        directory = Path(self.filepath).parent.absolute()
        for file in self.files:
            io_RIP.IO_RIP(str(directory / file.name), uv_scale=self.uv_scale, vertex_scale=self.vertex_scale,
                          auto_center=self.auto_center, invert_uv=self.invert_uv)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


class RIPImporterBatch(bpy.types.Operator):
    """Load RIP models"""
    bl_idname = "import_mesh.rip_batch"
    bl_label = "Import rip batch"
    bl_options = {'UNDO'}

    filepath = StringProperty(
        subtype='FILE_PATH',
    )
    uv_scale = bpy.props.FloatProperty(name='UV scale', default=1.0)
    invert_uv = bpy.props.BoolProperty(name='Invert UV', default=False)
    vertex_scale = bpy.props.FloatProperty(name='Vertex scale', default=1.0)
    auto_center = bpy.props.BoolProperty(name='Auto center model?', default=True)

    def execute(self, context):
        from . import io_RIP
        files = []
        sizes = {}
        directory = Path(self.filepath).parent.absolute()
        for file in os.listdir(os.path.dirname(self.filepath)):
            if file.endswith('.rip'):
                files.append(file)
        for file in files:
            a = ByteIO(path=str(directory / file))
            if a.size() not in sizes:
                sizes[a.size()] = file
        for file in sizes.values():
            io_RIP.IO_RIP(str(directory / file), uv_scale=self.uv_scale,
                          vertex_scale=self.vertex_scale, auto_center=self.auto_center,invert_uv=self.invert_uv)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}


def menu_import(self, context):
    self.layout.operator(RIPImporter.bl_idname, text="RIP mesh (.RIP)")
    self.layout.operator(RIPImporterBatch.bl_idname, text="RIP mesh batch(.RIP)")


def register():
    bpy.utils.register_module(__name__)
    # bpy.utils.register_class(RIP_Utilities.RIPRemoveDups)
    bpy.types.INFO_MT_file_import.append(menu_import)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_import.remove(menu_import)


if __name__ == "__main__":
    register()
