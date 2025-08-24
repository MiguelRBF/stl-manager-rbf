import os
import math
from typing import List

import numpy as np
from numpy.typing import NDArray
from stl import mesh

from geometry.segment import Segment
from geometry.segment_with_points import SegmentWithPoints
from geometry.plane import Plane

PlanesList = List[Plane]

stl_file_path = "stl-manager-rbf/stl_files/example_0.stl"
stl_output_path = "stl-manager-rbf/stl_files/example_0_sliced.stl"

def normalize(vector: np.ndarray):
    ''''''
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise Exception("Norm of provided vector is equal to 0.")
    return vector / norm if norm !=0 else vector

def find_first_vertex_index(vertex: np.ndarray, vertex_list: list):
    '''Find first vertex index that is equal to the vertex provided. Returns None if not found'''
    return next((i for i, x in enumerate(vertex_list) if np.array_equal(vertex, x)), None)

def vertex_in_vertex_list(vertex: np.ndarray, vertex_list: list):
    '''Check if vertex (np.array if 3 coordinates) is already inside the list provided'''
    return any(np.array_equal(vertex, x) for x in vertex_list)

def preprocess_mesh_triangles(mesh_triangles: np.ndarray):
    '''Get:
    - an array composed of unique vertices
    - an array that points the vertex id that compose each triangle
    '''

    mesh_vertex_list = []
    mesh_number_of_vertices = 0

    mesh_triangle_vertices_id_list = []

    # Iterate over all the triangles
    for triangle_vertices in mesh_triangles:
        triangle_vertices_id = []
        # Iterate over all its vertex
        for vertex in triangle_vertices:
            vertex_idx = find_first_vertex_index(vertex, mesh_vertex_list)
            # When vertex is not already inside vertex mesh list
            if (vertex_idx == None):
                # Add it to the list of vertices
                mesh_number_of_vertices += 1
                mesh_vertex_list.append(vertex)
                # Get new vertex index
                vertex_idx = mesh_number_of_vertices - 1

            # Add the vertex to triangle vertices id list
            triangle_vertices_id.append(vertex_idx)

        # Add the triangle vertex ids to global list
        mesh_triangle_vertices_id_list.append(np.array(triangle_vertices_id, dtype="uint64"))
    
    return np.array(mesh_triangle_vertices_id_list), np.array(mesh_vertex_list)

def get_slicing_planes(direction_vector_unitary: np.ndarray, slices_number: int, min_projection: float) -> PlanesList:
    ''''''
    slices_plane_list = []
    for slice_idx in range(slices_number):
        # get slicing plane reference point projection
        slice_reference_point_projection = min_projection + (slice_idx * thickness)
        # Gets it coordinates
        slice_reference_point = direction_vector_unitary * slice_reference_point_projection
        # Create slice plane
        slice_plane = Plane(slice_reference_point, direction_vector_unitary)
        # Add to the list of slicing planes
        slices_plane_list.append(slice_plane)

    return slices_plane_list

def get_vertex_slice_idx(vertex_projection: np.float64, min_projection: float, max_projection: float, slices_number: int):
    ''''''
    # get the slice index
    slice_idx = math.floor((vertex_projection - min_projection) / (max_projection - min_projection) * slices_number)
    # When the index correspond to fictitious layer index equal to the slices number (layer index 0 based)
    if (slice_idx == slices_number):
        # Set that the vertex belongs to the last slice
        slice_idx = slices_number - 1
    return slice_idx

def process_mesh_triangles(
    mesh_triangles_vertices_idx_np: np.ndarray, mesh_vertex_np: np.ndarray,
    mesh_vertex_projections_np: np.ndarray,
    min_projection: float, max_projection: float, slices_number: int,
    slices_plane_list: PlanesList):
    '''Get new triangles mesh with triangles that belongs to only one layer'''
    # Iterate over all the triangles
    for triangle_vertices_idx in mesh_triangles_vertices_idx_np:
        # List of tuples (vertex_idx-slice_idx)
        triangle_vertex_slices = []
        # List of slices for 3 vertex
        vertex_slices = []
        
        # Create a list to store all the points of the edges and its intersections (sorted)
        edges_points_list = []
        # Iterate over all triangle edges
        edges_vertices = [ (0, 1), (1, 2), (2, 0) ]
        for edge_vertex_1, edge_vertex_2 in edges_vertices:
            # get the coordinates of both vertices
            edge_vertex_1_coordinates = mesh_vertex_np[triangle_vertices_idx[edge_vertex_1]]
            edge_vertex_2_coordinates = mesh_vertex_np[triangle_vertices_idx[edge_vertex_2]]
            # Create a segment
            edge_segment = Segment(edge_vertex_1_coordinates, edge_vertex_2_coordinates)

            # Create list to store all the intersections of the edge with slicing planes
            edge_slices_intersections = []
            # Iterate over all slices
            for slice_plane in slices_plane_list:
                intersection_point = slice_plane.intersect_with_segment(edge_segment)
                # Check for intersection
                if intersection_point == None:
                    continue
                # Add the intersection to the list
                edge_slices_intersections.append(intersection_point)
            
            # Crete a segment with points
            edge_segment_with_intersections = SegmentWithPoints(edge_segment, intersection_point)
            # Sort the points by the segment direction...
            edge_segment_with_intersections.sort_points_along_segment()
            
            

def slice_stl(file_path: str, output_dir: str, direction_vector: np.ndarray, thickness: float):
    ''''''
    # Load stl file
    stl_model = mesh.Mesh.from_file(file_path)
    
    # Normalize direction vector
    direction_vector_unitary = normalize(direction_vector)

    # Get an array to identify each of the triangles of the mesh
    triangle_id_np = np.arange(stl_model.vectors.shape[0])
    
    # Preprocess mesh triangles
    mesh_triangles_vertices_idx_np, mesh_vertex_np = preprocess_mesh_triangles(stl_model.vectors)
    print(f"mesh number of triangles: {mesh_triangles_vertices_idx_np.shape[0]}")
    print(f"mesh number of unique vertices: {mesh_vertex_np.shape[0]}")
    print(f"mesh_triangles_vertices_idx_np: {mesh_triangles_vertices_idx_np}")
    print(f"mesh_vertex_np: {mesh_vertex_np}")
    
    # get the projection of all the vertices into slicing direction
    mesh_vertex_projections_np = np.dot(mesh_vertex_np, direction_vector_unitary)
    
    # obtain projections range
    min_projection = mesh_vertex_projections_np.min()
    max_projection = mesh_vertex_projections_np.max()
    range_projection = max_projection - min_projection
    
    # Compute the number of slices
    slices_number = math.ceil(range_projection / thickness)
    print(f"Number of slices: {slices_number}")
    
    # Get slices minimum and maximum projected value
    slices_plane_np = get_slicing_planes(direction_vector_unitary, slices_number, min_projection)
    # print(slices_ranges_np)
    
    # 
    process_mesh_triangles(
        mesh_triangles_vertices_idx_np, mesh_vertex_np,
        mesh_vertex_projections_np,
        min_projection, max_projection, slices_number,
        slices_plane_np)
    
if __name__ == "__main__":
    direction_vector = np.array([1, 0, 0])
    thickness = 1.0 # [mm]

    slice_stl(stl_file_path, stl_output_path, direction_vector, thickness)