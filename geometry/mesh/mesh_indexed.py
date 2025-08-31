
from typing import List

from geometry.mesh.triangle_indexed import TriangleIndexed
from geometry.vector import Vector3D

class MeshIndexed:
    """
    Class to manage a mesh using indexed values for the vertex and triangle normals
    """

    def __init__(self,
                 vertex_list: List[Vector3D],
                 normals_list: List[Vector3D],
                 triangle_indexed_list: List[TriangleIndexed]):
        self.vertex_list = vertex_list
        self.normals_list = normals_list
        self.triangle_indexed_list = triangle_indexed_list