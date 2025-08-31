import math
from typing import Dict, List

from geometry.mesh.mesh_indexed import MeshIndexed
from geometry.mesh.mesh_projections import MeshProjections
from geometry.plane import Plane
from geometry.triangle_sliced import TriangleSliced
from geometry.vector import Vector3D
from geometry.segment_sliced import SegmentSliced


class MeshSlices:
    """
    Class to manage mesh slices data
    
    Attributes:
        slice_thickness (float): the thickness of each slice [mm]
        slices_number (int): Number of slices
        direction_unitary (Vector3D): unitary direction into which the slicing is executed
        slicer_plane_list (List[Plane]): List of slicer planes
        slices_mesh_dict (Dict[int, MeshIndexed]): Dictionary to store an indexed mesh for each slice
    """

    def __init__(self, mesh_projections: MeshProjections,  slice_thickness: float):
        ''''''
        # Store the slice thickness
        self.slice_thickness = slice_thickness

        # Compute the number of slices
        self.slices_number: int = math.ceil(mesh_projections.range_projection / slice_thickness)
        print(f"Number of slices: {self.slices_number}")
        
        # Store unitary vector direction for slicing
        self.slicing_direction_unitary = mesh_projections.slicing_direction_unitary
        # Store the minimum projection
        self.min_projection = mesh_projections.min_projection
    
        # Get slicing planes planes
        self.__get_slicing_planes()
        
        # Init a dict to store each slice mesh
        self.__init_slices_mesh_dict()

    def __get_slicing_planes(self) -> None:
        """
        Create a list of planes that are going to be used to slice a mesh
        """
        # List to store the plane for each slice
        self.slicer_plane_list: List[Plane] = []

        # Iterate over all the slices to be executed
        for slice_idx in range(self.slices_number):
            # get slicing plane reference point projection
            slice_reference_point_projection = self.min_projection + (slice_idx * self.slice_thickness)
            
            # Gets it coordinates
            slice_reference_point = self.slicing_direction_unitary * slice_reference_point_projection
            
            # Create slice plane
            slice_plane = Plane(slice_reference_point, self.slicing_direction_unitary)
            # Add to the list of slicing planes
            self.slicer_plane_list.append(slice_plane)

    def __init_slices_mesh_dict(self) -> None:
        """
        Initialize an empty indexed mesh for each slice
        """
        # Create empty dictionary to store the mesh for each slice
        self.slices_mesh_dict: Dict[int, MeshIndexed] = {}
        # Iterate over all the slices to be executed
        for slice_idx in range(self.slices_number):
            # Create empty mesh for the slice
            self.slices_mesh_dict[slice_idx] = MeshIndexed([], [], [])

    def fill_mesh_slices(self,
        triangle_normal: Vector3D,
        segment_sliced_list: List[SegmentSliced]) -> None:
        """
        Fill slice mesh for the triangle provided as triangle normal and list of segments sliced.
        If:
        - triangle has intersections: Fill each slice mesh taking into account the intersections
        - triangle has NO intersection: Fill the slice mesh to which the triangle belongs to
        """
        # Boolean to indicate when the triangle has intersections
        triangle_has_intersections = False

        # Check if segments has no intersection
        for segment_sliced in segment_sliced_list:
            # When any of the segments slices has any intersection
            if (len(segment_sliced.points) > 0):
                triangle_has_intersections = True
                break
        
        # Fill the mesh depending if triangle has intersections or not
        if (triangle_has_intersections):
            self.__fill_mesh_slices_from_triangle_with_intersections(
                triangle_normal, segment_sliced_list)
        else:
            self.__fill_mesh_slices_from_triangle_without_intersections(
                triangle_normal, segment_sliced_list)

    def __fill_mesh_slices_from_triangle_without_intersections(self, 
        triangle_normal: Vector3D,
        segment_sliced_list: List[SegmentSliced]) -> None:
        """"""
        # Get the slice to which the triangle belongs. Use first sliced segment
        slice_index = segment_sliced_list[0].endpoints_slice_idx[0]

        # Get the list of vertex using the first point of the segments
        triangle_vertex_list = [
            segment_sliced_list[0].p1,
            segment_sliced_list[1].p1,
            segment_sliced_list[2].p1
        ]

        # Fill the slice mesh
        self.slices_mesh_dict[slice_index].add_triangle_to_mesh(triangle_normal, triangle_vertex_list)

    def __fill_mesh_slices_from_triangle_with_intersections(self, 
        triangle_normal: Vector3D,
        segment_sliced_list: List[SegmentSliced]) -> None:
        """"""
        # Create sliced triangle
        triangle_sliced = TriangleSliced(
            triangle_normal, segment_sliced_list, self.slicing_direction_unitary)
        # Preprocess it
        triangle_sliced.preprocess()
        # Get the the slices mesh dict for the triangle
        triangle_sliced.get_slices_mesh_dict()
        
        # Fill the slices mesh dictionary using the data computed for the triangle ...
        # TODO
        # self.slices_mesh_dict
