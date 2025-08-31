import os
import sys

from typing import List

from stl import mesh

from geometry.mesh.mesh_slices import MeshSlices
from geometry.mesh.triangle_indexed import TriangleIndexed
from geometry.mesh.mesh_indexed import MeshIndexed
from geometry.mesh.mesh_projections import MeshProjections
from geometry.plane import Plane
from geometry.segment import Segment
from geometry.vector import Vector3D
from geometry.vector_list import VectorList
from geometry.segment_sliced import SegmentSliced

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
    # Create empty indexed mesh
    mesh_indexed = MeshIndexed([], [], [])
    
    # Zip stl vertex and normals list
    zipped_stl = zip(stl_mesh_np.vectors, stl_mesh_np.normals)

    # Iterate over all the triangles and its normals
    for triangle_vertices_np, triangle_normal_np in zipped_stl:
        # triangle_vertices_idx: List[int] = []
        # Transform normal to internal vector class
        triangle_normal = Vector3D(triangle_normal_np)
        triangle_vertex_list: List[Vector3D] = []
        # Iterate over all its vertex
        for vertex_np in triangle_vertices_np:
            # Transform to internal vector class
            vertex = Vector3D(vertex_np)
            # Append to list of triangle vertex
            triangle_vertex_list.append(vertex)
        
        # Add the triangle to the mesh
        mesh_indexed.add_triangle_to_mesh(triangle_normal, triangle_vertex_list)

    return mesh_indexed

def process_mesh_triangles(
    mesh_indexed: MeshIndexed, mesh_projections: MeshProjections, mesh_slices: MeshSlices):
    """
    Get new triangles mesh with triangles that belongs to only one layer
    """
    # Iterate over all the triangles
    for triangle_indexed in mesh_indexed.triangle_indexed_list:
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
            edge_intersection_idx_list: List[int] = []
            # Iterate over all slices
            for slice_idx, slice_plane in enumerate(mesh_slices.slicer_plane_list):
                intersection = slice_plane.intersect_with_segment(edge_segment)
                # Check for intersection
                if intersection is None:
                    continue
                # Add the intersection to the list
                edge_intersection_list.append(intersection)
                # Add the index to the list of intersection index
                edge_intersection_idx_list.append(slice_idx)

            # Create a segment with intersections
            edge_segment_sliced = SegmentSliced(
                edge_segment, segment_endpoints_slice_idx,
                edge_intersection_list, edge_intersection_idx_list)
            print(edge_segment_sliced)

            # Append the edge with intersections to list
            segment_sliced_list.append(edge_segment_sliced)
        
        # Get triangle normal
        triangle_normal = mesh_indexed.normals_list[triangle_indexed.normal_index]
        # Fill the mesh slices
        mesh_slices.fill_mesh_slices(triangle_normal, segment_sliced_list)


def slice_stl(file_path: str, output_dir: str, slicing_direction: Vector3D, slice_thickness: float):
    """
    Slice the provided mesh file using the direction and thickness provided
    """
    # Load stl file
    stl_mesh_np = mesh.Mesh.from_file(file_path)

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