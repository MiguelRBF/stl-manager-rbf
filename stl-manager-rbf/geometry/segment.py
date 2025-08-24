# geometry/segment.py

from typing import Optional

from typing import Tuple
import numpy as np

from geometry.vector import Vector

class Segment:
    def __init__(self, point1: Vector, point2: Vector):
        if point1.shape != (3,) or point2.shape != (3,):
            raise ValueError("Both points must be 3D vectors with shape (3,)")
        self.p1: Vector = point1
        self.p2: Vector = point2

    def length(self) -> float:
        return float(np.linalg.norm(self.p2 - self.p1))

    def direction_vector(self) -> Vector:
        return self.p2 - self.p1

    def direction_vector_unitary(self) -> Vector:
        ab = self.p2 - self.p1
        return ab / np.linalg.norm(ab)
    
    def sort_points_along_direction(self, direction: Vector) -> None:
        """
        Sorts the segment's points so that p1 is the point with smaller
        projection onto 'direction' vector (assumed to be unitary).
        """
        if direction.shape != (3,):
            raise ValueError("Direction vector must have shape (3,)")

        # Compute projections
        proj_p1 = np.dot(self.p1, direction)
        proj_p2 = np.dot(self.p2, direction)

        # Swap points if p2 is smaller along direction
        if proj_p2 < proj_p1:
            self.p1, self.p2 = self.p2, self.p1

    def __repr__(self) -> str:
        return f"Segment3D({self.p1.tolist()}, {self.p2.tolist()})"
