# geometry/segment.py

import numpy as np

from geometry.vector import Vector3D

class Segment:
    def __init__(self, point1: Vector3D, point2: Vector3D):
        self.p1: Vector3D = point1
        self.p2: Vector3D = point2

    def length(self) -> float:
        return float(np.linalg.norm(self.p2 - self.p1))

    def direction_vector(self) -> Vector3D:
        return self.p2 - self.p1

    def direction_vector_unitary(self) -> Vector3D:
        ab = self.p2 - self.p1
        return ab / np.linalg.norm(ab)
    
    def sort_points_along_direction(self, direction: Vector3D) -> None:
        """
        Sorts the segment's points so that p1 is the point with smaller
        projection onto 'direction' vector (assumed to be unitary).
        """
        # Compute projections
        proj_p1 = np.dot(self.p1, direction)
        proj_p2 = np.dot(self.p2, direction)

        # Swap points if p2 is smaller along direction
        if proj_p2 < proj_p1:
            self.p1, self.p2 = self.p2, self.p1

    def __repr__(self) -> str:
        return f"Segment3D({self.p1.tolist()}, {self.p2.tolist()})"
