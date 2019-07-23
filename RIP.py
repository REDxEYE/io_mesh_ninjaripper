import os
import sys
from pprint import pprint

try:
    from .ByteIO_nr import ByteIO
    from .RIP_DATA import *
except:
    from ByteIO_nr import ByteIO
    from RIP_DATA import *

class RIP:

    def __init__(self,filepath):
        self.reader = ByteIO(path = filepath)
        print("Impotring",os.path.basename(filepath))
        self.header = RIPHeader()

    def read(self):
        self.header.read(self.reader)

if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            a = RIP(filepath=r"F:\randon_files\2019.07.22_22.30.52_DivinityEngine2.exe\Mesh_0129.rip")
            # a = RIP(filepath=r"./test_data/Mesh_0113.rip")
            a.read()
            verts, uvs, norms, colors, blend_ind, blend_weight = a.header.get_flat_verts()
            a = 0
            # for vert in uv:
            #     pprint(vert)
            # for vert in norm:
            #     pprint(vert)
            # pprint(a.header.vertexes)

