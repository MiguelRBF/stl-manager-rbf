from typing import List

from geometry.vector import Vector3D


class VectorList:
    """
    Class for methods related with Vector3D and List[Vector3D]
    """

    @staticmethod
    def find_first_vector_index(vertex: Vector3D, vertex_list: List[Vector3D]):
        """
        Find first vector index that is equal to the vertex provided. Returns None if not found
        """
        return next((i for i, x in enumerate(vertex_list) if vertex.is_equal_to(x)), None)

    @staticmethod
    def vector_in_vector_list(vertex: Vector3D, vertex_list: List[Vector3D]):
        """
        Check if vertex (np.array if 3 coordinates) is already inside the list provided
        """
        return any(vertex.is_equal_to(x) for x in vertex_list)