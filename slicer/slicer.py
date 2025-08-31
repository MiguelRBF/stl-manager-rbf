import os
import sys

import math
from typing import List, Tuple

import numpy as np
from stl import mesh

from geometry.mesh.mesh_slices import MeshSlices
from geometry.mesh.triangle_indexed import TriangleIndexed
from geometry.mesh.triangle_stl import TriangleSTL
from geometry.mesh.mesh_indexed import MeshIndexed
from geometry.mesh.mesh_projections import MeshProjections
from geometry.plane import Plane
from geometry.segment import Segment
from geometry.vector import Vector3D
from slicer.segment_sliced import SegmentSliced

PlanesList = List[Plane]

stl_file_path = "files/example_0.stl"
stl_output_path = "files/example_0_sliced.stl"

def find_first_vertex_index(vertex: Vector3D, vertex_list: List[Vector3D]):
    """
    Find first vertex index that is equal to the vertex provided. Returns None if not found
    """
    return next((i for i, x in enumerate(vertex_list) if vertex.is_equal_to(x)), None)

def vertex_in_vertex_list(vertex: Vector3D, vertex_list: List[Vector3D]):
    """
    Check if vertex (np.array if 3 coordinates) is already inside the list provided
    """
    return any(vertex.is_equal_to(x) for x in vertex_list)

def preprocess_mesh_triangles(stl_mesh_np: mesh.Mesh) -> MeshIndexed:
    """
    Preprocess numpy-stl mesh to convert to inner indexed mesh
    """
    mesh_vertex_list: List[Vector3D] = []
    mesh_number_of_vertices = 0

    triangle_indexed_list: List[TriangleIndexed] = []

    # Iterate over all the triangles
    for triangle_idx, triangle_vertices in enumerate(stl_mesh_np.vectors):
        triangle_vertices_idx: List[int] = []
        # Iterate over all its vertex
        for vertex in triangle_vertices:
            # Transform to internal vector class
            vertex_3d = Vector3D(vertex)
            vertex_idx = find_first_vertex_index(vertex_3d, mesh_vertex_list)
            # When vertex is not already inside vertex mesh list
            if (vertex_idx == None):
                # Add it to the list of vertices
                mesh_number_of_vertices += 1
                mesh_vertex_list.append(vertex_3d)
                # Get new vertex index
                vertex_idx = mesh_number_of_vertices - 1

            # Add the vertex to triangle vertices id list
            triangle_vertices_idx.append(vertex_idx)

        # Create triangle using vertices indices and its normal index
        triangle = TriangleIndexed(triangle_idx, triangle_vertices_idx, triangle_idx)
        # Add the triangle to the list
        triangle_indexed_list.append(triangle)

    # Transform stl mesh normals vector numpy array to inner list
    triangle_normal_list: List[Vector3D] = []
    for normal_np in stl_mesh_np.normals:
        # Transform to vector 3D and append to list
        triangle_normal_list.append(Vector3D(normal_np))
    
    # Create output indexed mesh and return
    return MeshIndexed(mesh_vertex_list, triangle_normal_list, triangle_indexed_list)

def process_mesh_triangles(
    mesh_indexed: MeshIndexed, mesh_projections: MeshProjections, mesh_slices: MeshSlices):
    """
    Get new triangles mesh with triangles that belongs to only one layer
    """
    # Iterate over all the triangles
    for triangle_idx, triangle_indexed in enumerate(mesh_indexed.triangle_indexed_list):
        # Create a list to store the edges and its intersections (sorted)
        segment_sliced_list: List[SegmentSliced] = []

        # Iterate over all triangle edges
        edges_vertices = [ (0, 1), (1, 2), (2, 0) ]
        for endpoint_1_idx, endpoint_2_idx in edges_vertices:
            # Get the vertices mesh index
            vertex_1_mesh_index = triangle_indexed.vertices_index[endpoint_1_idx]
            vertex_2_mesh_index = triangle_indexed.vertices_index[endpoint_2_idx]

            # Get the coordinates of both vertices
            vertex_1 = mesh_indexed.vertex_list[vertex_1_mesh_index]
            vertex_2 = mesh_indexed.vertex_list[vertex_2_mesh_index]
            # Create a segment
            edge_segment = Segment(vertex_1, vertex_2)
            
            # Get to which slice does the vertex belongs to
            vertex_1_slice_idx = mesh_projections.get_vertex_slice_idx(
                vertex_1_mesh_index, mesh_slices.slices_number)
            vertex_2_slice_idx = mesh_projections.get_vertex_slice_idx(
                vertex_2_mesh_index, mesh_slices.slices_number)
            segment_endpoints_slice_idx = (vertex_1_slice_idx, vertex_2_slice_idx)

            # Create list to store all the intersections of the edge with slicing planes
            edge_intersection_list: List[Vector3D] = []
            # Iterate over all slices
            for slice_plane in mesh_slices.slicer_plane_list:
                intersection = slice_plane.intersect_with_segment(edge_segment)
                # Check for intersection
                if intersection is None:
                    continue
                # Add the intersection to the list
                edge_intersection_list.append(intersection)

            # Create a segment with intersections
            edge_segment_sliced = SegmentSliced(
                edge_segment, segment_endpoints_slice_idx, edge_intersection_list)
            print(edge_segment_sliced)

            # Append the edge with intersections to list
            segment_sliced_list.append(edge_segment_sliced)
        
        TriangleSTL.create_triangle_inner_mesh(
            triangle_indexed, segment_sliced_list)

def slice_stl(file_path: str, output_dir: str, slicing_direction: Vector3D, slice_thickness: float):
    """
    Slice the provided mesh file using the direction and thickness provided
    """
    # Load stl file
    stl_mesh_np = mesh.Mesh.from_file(file_path)
    
    # Normalize direction vector
    direction_vector_unitary = slicing_direction.normalize()

    # Get an array to identify each of the triangles of the mesh
    triangle_id_np = np.arange(stl_mesh_np.vectors.shape[0])

    # Preprocess stl mesh triangles
    mesh_indexed = preprocess_mesh_triangles(stl_mesh_np)
    print(f"mesh number of triangles: {len(mesh_indexed.triangle_indexed_list)}")
    print(f"mesh number of unique vertices: {len(mesh_indexed.vertex_list)}")
    print(f"mesh_triangle_vertices_idx_list: {mesh_indexed.triangle_indexed_list}")
    
    # Get mesh projections
    mesh_projections = MeshProjections(mesh_indexed, slicing_direction)
    
    # Init mesh slices
    mesh_slices = MeshSlices(mesh_projections, slice_thickness)

    # Process mesh triangles
    process_mesh_triangles(mesh_indexed, mesh_projections, mesh_slices)
    
if __name__ == "__main__":
    slicing_direction = Vector3D([1, 0, 0])
    slice_thickness = 1.0 # [mm]

    slice_stl(stl_file_path, stl_output_path, slicing_direction, slice_thickness)