import sys
from pprint import pprint

try:
    from .ByteIO import ByteIO
    from .RIP_DATA import *
except:
    from ByteIO import ByteIO
    from RIP_DATA import *

class RIP:

    def __init__(self,filepath):
        self.reader = ByteIO(path = filepath)
        self.header = RIPHeader()

    def read(self):
        self.header.read(self.reader)

if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            a = RIP(filepath=r"./test_data/Mesh_0113.rip")
            a.read()
            for vertex in a.header.vertexes:
                pprint(vertex.__dict__)
            # pprint(a.header.vertexes)
