from typing import List

import numpy as np
from numpy.typing import NDArray

from geometry.mesh.triangle_indexed import TriangleIndexed
from geometry.vector import Vector3D
from slicer.segment_sliced import SegmentSliced

class TriangleSTL:
    def __init__(self, vertex_list: List[Vector3D], normal: Vector3D):
        self.vertex_list: List[Vector3D] = vertex_list
        self.normal: Vector3D = normal
    
    def compute_triangle_inner_mesh(
        triangle_normal: Vector3D, segment_sliced_list: List[SegmentSliced]):
        ''''''
        # get the 
        
    def create_triangle_inner_mesh(
        triangle_indexed: TriangleIndexed, triangle_normal: Vector3D,
        segment_sliced_list: List[SegmentSliced]) -> List[TriangleIndexed]:
        ''''''
        triangle_has_intersections = False
        # Check if segments has no intersection
        for segment_sliced in segment_sliced_list:
            # When any of the segments slices has any intersection
            if (len(segment_sliced.points) > 0):
                triangle_has_intersections = True
                break
        
        if (triangle_has_intersections):
            ''''''
        else:
            # get the list of vertex using the first point of the segments
            vertex_list = [
                segment_sliced_list[0].segment.p1,
                segment_sliced_list[1].segment.p1,
                segment_sliced_list[2].segment.p1
            ]
            return TriangleSTL(vertex_list, triangle_normal)
    