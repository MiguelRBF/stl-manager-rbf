import math
import numpy as np

from geometry.mesh.mesh_indexed import MeshIndexed
from geometry.vector import Vector3D

class MeshProjections:
    """
    Class to manage the mesh vertex projections into one slicing direction
    """

    def __init__(self, mesh_indexed: MeshIndexed, slicing_direction: Vector3D):
        # Normalize direction vector and store as attribute
        self.slicing_direction_unitary = slicing_direction.normalize()
        
        # Convert to numpy array the vertex list to use numpy methods on it
        mesh_vertex_np = np.array(mesh_indexed.vertex_list)
        
        # get the projection of all the vertices into slicing direction
        self.vertex_projections_np = np.dot(mesh_vertex_np, self.slicing_direction_unitary)
        
        # obtain projections minimum, maximum and range
        self.min_projection = self.vertex_projections_np.min()
        self.max_projection = self.vertex_projections_np.max()
        self.range_projection = self.max_projection - self.min_projection
    
    def get_vertex_slice_idx(self, vertex_mesh_index: int, slices_number: int):
        """
        Get the slice idx to which the vertex belongs to
        """
        # Get projections for vertex
        vertex_projection = self.vertex_projections_np[vertex_mesh_index]
        # get the slice index
        slice_idx = math.floor((vertex_projection - self.min_projection) /
                               (self.max_projection - self.min_projection) * slices_number)
        # When the index correspond to fictitious layer index equal to the slices number (layer index 0 based)
        if (slice_idx == slices_number):
            # Set that the vertex belongs to the last slice
            slice_idx = slices_number - 1
        return slice_idx