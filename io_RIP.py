import random,os.path

import bpy
try:
    from .ByteIO import ByteIO
    from .RIP_DATA import *
    from .RIP import RIP
except:
    from ByteIO import ByteIO
    from RIP_DATA import *
    from RIP import RIP

class IO_RIP:
    def __init__(self, path: str = None, import_textures:bool=False):
        self.rip = RIP(filepath=path)
        self.rip.read()
        self.rip_header = self.rip.header
        self.name = os.path.basename(path)
        self.create_mesh()
    @staticmethod
    def get_material(mat_name, model_ob):
        if mat_name:
            mat_name = mat_name
        else:
            mat_name = "Material"

        md = model_ob.data
        mat = None
        for candidate in bpy.data.materials:  # Do we have this material already?
            if candidate.name == mat_name:
                mat = candidate
        if mat:
            if md.materials.get(mat.name):  # Look for it on this mesh
                for i in range(len(md.materials)):
                    if md.materials[i].name == mat.name:
                        mat_ind = i
                        break
            else:  # material exists, but not on this mesh
                md.materials.append(mat)
                mat_ind = len(md.materials) - 1
        else:  # material does not exist
            # print("- New material: {}".format(mat_name))
            mat = bpy.data.materials.new(mat_name)
            md.materials.append(mat)
            # Give it a random colour
            randCol = []
            for i in range(3):
                randCol.append(random.uniform(.4, 1))
            mat.diffuse_color = randCol

            mat_ind = len(md.materials) - 1

        return mat_ind

    def create_mesh(self):
        verts, uvs, norms, colors = self.rip_header.get_flat_verts()
        self.mesh_obj = bpy.data.objects.new(self.name, bpy.data.meshes.new(self.name+"_mesh"))
        bpy.context.scene.objects.link(self.mesh_obj)
        self.mesh = self.mesh_obj.data
        self.mesh.from_pydata(verts, [], self.rip_header.indexes)
        self.mesh.uv_textures.new()
        uv_data = self.mesh.uv_layers[0].data
        for i in range(len(uv_data)):
            u = uvs[self.mesh.loops[i].vertex_index]
            uv_data[i].uv = u