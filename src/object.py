import numpy as np
from stl import mesh

class Object():
    def __init__(self,object):
        self.mesh = mesh.Mesh.from_file(object)
        self._normalize()
        self.obj = self.setObj()
        self.vectors = self.mesh.vectors 

    def _normalize(self):
        """Centraliza no centroide e escala para caber em [-1, 1]."""
        verts = self.mesh.vectors.reshape(-1, 3)
        centroid = verts.mean(axis=0)
        self.mesh.translate(-centroid)
        max_extent = np.abs(self.mesh.vectors).max()
        if max_extent > 0:
            self.mesh.vectors /= max_extent

    def setObj(self):
        x = self.mesh.x.flatten()
        y = self.mesh.y.flatten()
        z = self.mesh.z.flatten()
        obj = np.array([x.T,y.T,z.T,np.ones(x.size)])

        return obj