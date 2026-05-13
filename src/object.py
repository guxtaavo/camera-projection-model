import numpy as np
from stl import mesh

def load_mesh(stl_path):
    return mesh.Mesh.from_file(str(stl_path))

def normalize_mesh(stl_mesh):
    verts = stl_mesh.vectors.reshape(-1, 3)

    centroid = verts.mean(axis=0)

    stl_mesh.translate(-centroid)

    max_extent = np.abs(stl_mesh.vectors).max()

    if max_extent > 0:
        stl_mesh.vectors /= max_extent

    return stl_mesh

def mesh_to_homogeneous(stl_mesh):
    x = stl_mesh.x.flatten()
    y = stl_mesh.y.flatten()
    z = stl_mesh.z.flatten()

    obj = np.array([
        x,
        y,
        z,
        np.ones(x.size)
    ])

    return obj


def load_object(stl_path, normalize=True):
    stl_mesh = load_mesh(stl_path)

    if normalize:
        stl_mesh = normalize_mesh(stl_mesh)

    obj = mesh_to_homogeneous(stl_mesh)

    vectors = stl_mesh.vectors

    return obj, vectors, stl_mesh