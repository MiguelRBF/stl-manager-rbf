
from typing import List

from geometry.mesh.triangle_indexed import TriangleIndexed
from geometry.vector import Vector3D
from geometry.vector_list import VectorList

class MeshIndexed:
    """
    Class to manage a mesh using indexed values for the vertex and triangle normals

    Attributes:
        vertex_list (List[Vector3D]): Vertex list (non duplicated values)
        normals_list (List[Vector3D]): Normals list (non duplicated values)
        triangle_indexed_list (List[TriangleIndexed]): List of indexed triangles
    """

    def __init__(self,
                 vertex_list: List[Vector3D],
                 normals_list: List[Vector3D],
                 triangle_indexed_list: List[TriangleIndexed]):
        # Vertex list (non duplicated values)
        self.vertex_list = vertex_list
        # Normals list (non duplicated values)
        self.normals_list = normals_list
        # List of indexed triangles
        self.triangle_indexed_list = triangle_indexed_list

    def append_vertex_list(self, vertex_list: List[Vector3D]) -> List[int]:
        """
        Append if needed the vertex to the list of vertices.
        Returns the indices provided to each vertex
        """
        # Get the number of vertices inside vertex list
        mesh_number_of_vertices = len(self.vertex_list)
        
        # Init vertices index list (inside the mesh)
        triangle_vertices_indices: List[int] = []

        # Iterate over vertex list
        for vertex in vertex_list:
            # Find first index inside the list that matches the vertex values
            vertex_idx = VectorList.find_first_vector_index(vertex, self.vertex_list)

            # When vertex is not already inside vertex mesh list
            if (vertex_idx == None):
                # +1 to the count of vertices
                mesh_number_of_vertices += 1
                # Add it to the list of vertices
                self.vertex_list.append(vertex)
                # Get new vertex index
                vertex_idx = mesh_number_of_vertices - 1
            
            # Append the index to the list
            triangle_vertices_indices.append(vertex_idx)
        # return the indices provided to the vertices
        return triangle_vertices_indices
    
    def append_normal(self, normal: Vector3D) -> int:
        """
        Append if needed the normal to the list of indices.
        Returns the index provided to the normal
        """
        # Find first index inside the list that matches the vertex values
        normal_idx = VectorList.find_first_vector_index(normal, self.normals_list)

        # When normal is not already inside normals mesh list
        if (normal_idx == None):
            # Add it to the list of normals
            self.normals_list.append(normal)
            # Get new normal index
            normal_idx = len(self.normals_list) - 1
        # Return the index provided to the normal
        return normal_idx

    def add_triangle_to_mesh(self, triangle_normal: Vector3D, triangle_vertex_list: List[Vector3D]):
        """
        Add the triangle (provided as triangle normal and vertex list) to the mesh
        """
        # Append the vertices to the mesh
        triangle_vertices_indices = self.append_vertex_list(triangle_vertex_list)
        # Add the normal to the list
        normal_idx = self.append_normal(triangle_normal)

        # Get triangle index
        triangle_index = len(self.triangle_indexed_list)
        
        # Create triangle indexed, append it to the list of indexed triangles
        triangle_indexed = TriangleIndexed(triangle_index, triangle_vertices_indices, normal_idx)
        self.triangle_indexed_list.append(triangle_indexed)
