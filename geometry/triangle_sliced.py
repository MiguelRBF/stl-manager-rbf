
from typing import Dict, List
from geometry.mesh.mesh_indexed import MeshIndexed
from geometry.segment_sliced import SegmentSliced
from geometry.vector import Vector3D

class TriangleSliced:
    """"""
    def __init__(self,
                 triangle_normal: Vector3D,
                 segment_sliced_list: List[SegmentSliced],
                 slices_number: int,
                 slicing_direction_unitary: Vector3D):
        self.triangle_normal = triangle_normal
        self.segment_sliced_list = segment_sliced_list
        self.slices_number = slices_number
        self.slicing_direction_unitary = slicing_direction_unitary
        
    def preprocess(self):
        """
        """
        # Get max min slices indices
        self.__get_min_max_slice_indices()
        # Get triangle orientation
        self.__get_triangle_orientation()
        
        
    def __get_min_max_slice_indices(self):
        """
        """
        # Init triangle minimum and maximum slices idx
        self.min_slice_idx: int = self.slices_number - 1
        self.max_slice_idx: int = 0

        # Iterate over all the sliced segments
        for segment_idx, segment_sliced in enumerate(self.segment_sliced_list):
            # Sort all its points along the slicing direction
            segment_sliced.sort_all_points_along_slicing_direction(self.slicing_direction_unitary)

            # get the start and end slices of the segment
            (segment_min_slice_idx, segment_max_slice_idx) = segment_sliced.endpoints_slice_idx
            
            # Check if stored triangle minimum/maximum slice index must be updated
            if (self.min_slice_idx > segment_min_slice_idx):
                self.min_slice_idx = segment_min_slice_idx
            if (self.max_slice_idx < segment_max_slice_idx):
                self.max_slice_idx = segment_max_slice_idx
    
    def __get_triangle_orientation(self):
        """
        """
        # In case that any segmented segment belongs only to one slice, 
        # this will store its index inside the list of segmented segments
        self.single_slice_segment_index = None
        # Stores true when previous segment is in the bottom or top part
        self.single_slice_segment_at_the_bottom = False
        self.single_slice_segment_at_the_top = False
        
        # Index to store the segment with the bigger number of slices
        self.segment_idx_with_all_the_slices = None

        # Iterate over all the sliced segments
        for segment_idx, segment_sliced in enumerate(self.segment_sliced_list):
            # get the start and end slices of the segment
            (segment_min_slice_idx, segment_max_slice_idx) = segment_sliced.endpoints_slice_idx
                
            # Check if both endpoints belong to the same slice
            if (segment_min_slice_idx == segment_max_slice_idx):
                if (self.single_slice_segment_index != None):
                    raise Exception("No more than 1 segment can belong to one slice!")
                # Store the segment index
                self.single_slice_segment_index = segment_idx
                
            # If the segment has all the slices of the triangle, store its index
            if ((segment_max_slice_idx - segment_min_slice_idx) == self.slices_number):
                self.segment_idx_with_all_the_slices = segment_idx
        
        # When there is a segment that belongs to just one slice
        if (self.single_slice_segment_index != None):
            # The segment is in the bottom part (with regards to slicing direction)
            if (self.single_slice_segment_index == self.min_slice_idx):
                self.single_slice_segment_at_the_bottom = True
            # The segment is in the top part (with regards to slicing direction)
            elif (self.single_slice_segment_index == self.max_slice_idx):
                self.single_slice_segment_at_the_top = True
            else:
                raise Exception("Segment that belongs to one slice must be on the bottom or top!")

    def get_slices_mesh_dict(self) -> Dict[int, MeshIndexed]:
        """
        """
        # init output dictionary
        self.__init_slices_mesh_dict(self.min_slice_idx, self.max_slice_idx)
        
        # When there is a single slice element at the bottom
        if (self.single_slice_segment_at_the_bottom):
            return self.__get_bottom_triangle_slices_mesh_dict()
        # When there is a single slice element at the top 
        elif (self.single_slice_segment_at_the_top):
            return self.__get_top_triangle_slices_mesh_dict()
        # For any other type of triangle
        else:
            self.__get_general_triangle_slices_mesh_dict()

    def __init_slices_mesh_dict(self, min_slice_idx: int, max_slice_idx: int
                                ) -> None:
        """
        Initialize an empty indexed mesh for each slice
        """
        # Create empty dictionary to store the mesh for each slice
        self.slices_mesh_dict: Dict[int, MeshIndexed] = {}

        # Iterate over all the slices the triangle belongs to
        for slice_idx in range(min_slice_idx, max_slice_idx + 1):
            # Create empty mesh for the slice
            self.slices_mesh_dict[slice_idx] = MeshIndexed([], [], [])

    def __get_bottom_triangle_slices_mesh_dict(self) -> Dict[int, MeshIndexed]:
        """
        """
        # Iterate over all the slices the triangle belongs to
        for slice_plane_idx in range(self.min_slice_idx, self.max_slice_idx + 1):
            ''''''

    def __get_top_triangle_slices_mesh_dict(self) -> Dict[int, MeshIndexed]:
        """
        """
        # Iterate over all the slices the triangle belongs to
        for slice_plane_idx in range(self.min_slice_idx, self.max_slice_idx + 1):
            ''''''
            
    def __get_general_triangle_slices_mesh_dict(self) -> Dict[int, MeshIndexed]:
        """
        """
        # Iterate over all the slices the triangle belongs to
        for slice_plane_idx in range(self.min_slice_idx, self.max_slice_idx + 1):
            ''''''