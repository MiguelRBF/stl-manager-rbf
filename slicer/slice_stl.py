import os
import sys

import math
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray
from stl import mesh

from geometry.vector import Vector3D
from geometry.segment import Segment
from slicer.segment_sliced import SegmentSliced
from geometry.plane import Plane

PlanesList = List[Plane]

stl_file_path = "files/example_0.stl"
stl_output_path = "files/example_0_sliced.stl"

def find_first_vertex_index(vertex: Vector3D, vertex_list: List[Vector3D]):
    '''Find first vertex index that is equal to the vertex provided. Returns None if not found'''
    return next((i for i, x in enumerate(vertex_list) if vertex.is_equal_to(x)), None)

def vertex_in_vertex_list(vertex: Vector3D, vertex_list: List[Vector3D]):
    '''Check if vertex (np.array if 3 coordinates) is already inside the list provided'''
    return any(vertex.is_equal_to(x) for x in vertex_list)

def preprocess_mesh_triangles(mesh_triangles: np.ndarray) -> Tuple[List[List[int]], List[Vector3D]]:
    '''Get:
    - an array composed of unique vertices
    - an array that points the vertex id that compose each triangle
    '''

    mesh_vertex_list: List[Vector3D] = []
    mesh_number_of_vertices = 0

    mesh_triangle_vertices_idx_list: List[List[int]] = []

    # Iterate over all the triangles
    for triangle_vertices in mesh_triangles:
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

        # Add the triangle vertex idx to global list
        mesh_triangle_vertices_idx_list.append(triangle_vertices_idx)
    
    return mesh_triangle_vertices_idx_list, mesh_vertex_list

def get_slicing_planes(
    direction_vector_unitary: Vector3D, slices_number: int, min_projection: float) -> List[Plane]:
    ''''''
    slices_plane_list = []
    for slice_idx in range(slices_number):
        # get slicing plane reference point projection
        slice_reference_point_projection = min_projection + (slice_idx * slice_thickness)
        # Gets it coordinates
        slice_reference_point = direction_vector_unitary * slice_reference_point_projection
        # Create slice plane
        slice_plane = Plane(slice_reference_point, direction_vector_unitary)
        # Add to the list of slicing planes
        slices_plane_list.append(slice_plane)

    return slices_plane_list

def get_vertex_slice_idx(
    vertex_projection: np.float64, min_projection: float, max_projection: float, slices_number: int):
    ''''''
    # get the slice index
    slice_idx = math.floor((vertex_projection - min_projection) / (max_projection - min_projection) * slices_number)
    # When the index correspond to fictitious layer index equal to the slices number (layer index 0 based)
    if (slice_idx == slices_number):
        # Set that the vertex belongs to the last slice
        slice_idx = slices_number - 1
    return slice_idx

def get_segment_endpoints_slice_idx(vertex_1_mesh_index, vertex_2_mesh_index,
                                    mesh_vertex_projections_np: NDArray[np.float64],
                                    min_projection: float, max_projection: float, slices_number: int
                                    ) -> Tuple[int, int]:
    # Get to which slice does the vertex belongs to
    vertex_1_slice_idx = get_vertex_slice_idx(mesh_vertex_projections_np[vertex_1_mesh_index],
                                              min_projection, max_projection, slices_number)
    vertex_2_slice_idx = get_vertex_slice_idx(mesh_vertex_projections_np[vertex_2_mesh_index],
                                              min_projection, max_projection, slices_number)
    return (vertex_1_slice_idx, vertex_2_slice_idx)

def process_mesh_triangles(
    mesh_triangle_vertices_idx_list: List[List[int]], mesh_vertex_np: NDArray,
    mesh_vertex_projections_np: NDArray[np.float64],
    min_projection: float, max_projection: float, slices_number: int,
    slices_plane_list: List[Plane]):
    '''Get new triangles mesh with triangles that belongs to only one layer'''
    # Iterate over all the triangles
    for triangle_vertices_idx in mesh_triangle_vertices_idx_list:
        # List of tuples (vertex_idx-slice_idx)
        triangle_vertex_slices = []
        # List of slices for 3 vertex
        vertex_slices = []
        
        # Create a list to store all the points of the edges and its intersections (sorted)
        edges_with_intersections_list = []
        # Iterate over all triangle edges
        edges_vertices = [ (0, 1), (1, 2), (2, 0) ]
        for endpoint_1, endpoint_2 in edges_vertices:
            # Get the vertices mesh index
            vertex_1_mesh_index = triangle_vertices_idx[endpoint_1]
            vertex_2_mesh_index = triangle_vertices_idx[endpoint_2]

            # Get the coordinates of both vertices
            vertex_1: Vector3D = mesh_vertex_np[vertex_1_mesh_index]
            vertex_2: Vector3D = mesh_vertex_np[vertex_2_mesh_index]
            # Create a segment
            edge_segment = Segment(vertex_1, vertex_2)
            
            # Get to which slice does the vertex belongs to
            segment_endpoints_slice_idx = get_segment_endpoints_slice_idx(
                vertex_1_mesh_index, vertex_2_mesh_index,
                mesh_vertex_projections_np,
                min_projection, max_projection, slices_number)

            # Create list to store all the intersections of the edge with slicing planes
            edge_slices_intersections: List[Vector3D] = []
            # Iterate over all slices
            for slice_plane in slices_plane_list:
                intersection_point = slice_plane.intersect_with_segment(edge_segment)
                # Check for intersection
                if intersection_point is None:
                    continue
                # Add the intersection to the list
                edge_slices_intersections.append(intersection_point)

            # Crete a segment with intersections
            edge_segment_with_intersections = SegmentSliced(
                edge_segment, segment_endpoints_slice_idx, edge_slices_intersections)
            print(edge_segment_with_intersections)
            # # Sort the points by the segment direction...
            # edge_segment_with_intersections.sort_points_along_segment()
            
            # Append the edge with intersections to list
            edges_with_intersections_list.append(edge_segment_with_intersections)
            
        

def slice_stl(file_path: str, output_dir: str, direction_vector: Vector3D, slice_thickness: float):
    ''''''
    # Load stl file
    stl_model = mesh.Mesh.from_file(file_path)
    
    # Normalize direction vector
    direction_vector_unitary = direction_vector.normalize()

    # Get an array to identify each of the triangles of the mesh
    triangle_id_np = np.arange(stl_model.vectors.shape[0])
    
    # Preprocess mesh triangles
    mesh_triangle_vertices_idx_list, mesh_vertex_list = preprocess_mesh_triangles(stl_model.vectors)
    print(f"mesh number of triangles: {len(mesh_triangle_vertices_idx_list)}")
    print(f"mesh number of unique vertices: {len(mesh_vertex_list)}")
    
    # Convert to numpy array the vertex list to use numpy methods on it
    mesh_vertex_np = np.array(mesh_vertex_list)
    print(f"mesh_triangle_vertices_idx_list: {mesh_triangle_vertices_idx_list}")
    print(f"mesh_vertex_np: {mesh_vertex_np}")
    
    # get the projection of all the vertices into slicing direction
    mesh_vertex_projections_np = np.dot(mesh_vertex_np, direction_vector_unitary)
    
    # obtain projections range
    min_projection = mesh_vertex_projections_np.min()
    max_projection = mesh_vertex_projections_np.max()
    range_projection = max_projection - min_projection
    
    # Compute the number of slices
    slices_number = math.ceil(range_projection / slice_thickness)
    print(f"Number of slices: {slices_number}")
    
    # Get slices minimum and maximum projected value
    slices_plane_np = get_slicing_planes(direction_vector_unitary, slices_number, min_projection)
    # print(slices_ranges_np)
    
    # 
    process_mesh_triangles(
        mesh_triangle_vertices_idx_list, mesh_vertex_np,
        mesh_vertex_projections_np,
        min_projection, max_projection, slices_number,
        slices_plane_np)
    
if __name__ == "__main__":
    direction_vector = Vector3D([1, 0, 0])
    slice_thickness = 1.0 # [mm]

    slice_stl(stl_file_path, stl_output_path, direction_vector, slice_thickness)