import math
from typing import List

from geometry.mesh.mesh_projections import MeshProjections
from geometry.plane import Plane
from geometry.vector import Vector3D


class MeshSlices:
    """
    Class to manage mesh slices data
    """

    def __init__(self, mesh_projections: MeshProjections,  slice_thickness: float):
        ''''''
        # Store the slice thickness
        self.slice_thickness = slice_thickness

        # Compute the number of slices
        self.slices_number: int = math.ceil(mesh_projections.range_projection / slice_thickness)
        print(f"Number of slices: {self.slices_number}")
    
        # Get slices minimum and maximum projected value
        self.slicer_plane_list: List[Plane] = MeshSlices.get_slicing_planes(
            mesh_projections.slicing_direction_unitary,
            self.slices_number, slice_thickness,
            mesh_projections.min_projection)

    @staticmethod
    def get_slicing_planes(direction_vector_unitary: Vector3D,
                           slices_number: int, slice_thickness: float,
                           min_projection: float) -> List[Plane]:
        """
        Create a list of planes that are going to be used to slice a mesh
        """
        # List of planes for used for slicing
        slices_plane_list: List[Plane] = []
        # Iterate over all the slices to be executed
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