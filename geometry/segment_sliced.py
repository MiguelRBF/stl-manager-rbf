# geometry/segment_with_points.py

from typing import List, Tuple

import numpy as np

from geometry.segment import Segment
from geometry.vector import Vector3D

class SegmentSliced(Segment):
    def __init__(self,
                 segment: Segment, endpoints_slices_idx: Tuple[int],
                 points: List[Vector3D] = None, tol: float = 1e-8):
        # Init father class attributes
        super().__init__(segment.p1, segment.p2)
        self.endpoints_slices_idx: Tuple[int] = endpoints_slices_idx
        self.points: List[Vector3D] = []
        self.tol = tol

        if points is not None:
            for pt in points:
                self.add_point(pt)

    def _is_point_on_segment(self, point: Vector3D) -> bool:
        """
        Check if the point lies on the segment within a tolerance.
        Uses the parametric form and verifies:
            - The projection parameter t ∈ [0,1]
            - The perpendicular distance is small (close to 0)
        """
        a = self.p1
        b = self.p2
        ab = b - a
        ap = point - a
        ab_norm_sq = np.dot(ab, ab)

        if ab_norm_sq < self.tol:
            # Degenerate segment (zero length)
            return np.linalg.norm(ap) < self.tol

        t = np.dot(ap, ab) / ab_norm_sq

        if t < -self.tol or t > 1 + self.tol:
            return False  # Outside segment bounds

        closest_point = a + t * ab
        dist = np.linalg.norm(point - closest_point)
        return dist < self.tol

    def add_point(self, point: Vector3D) -> None:
        """
        Adds a point
        """
        self.points.append(point)

    def add_point_if_is_in_segment(self, point: Vector3D) -> None:
        """
        Adds a point if it lies on the segment (within tolerance),
        raises ValueError otherwise.
        """
        if point.shape != (3,):
            raise ValueError("Point must be a 3D vector")

        if not self._is_point_on_segment(point):
            raise ValueError("Point does not lie on the segment")

        self.points.append(point)

    def sort_points_along_segment(self) -> None:
        """
        Sorts the internal points in-place along the segment direction.
        """
        # get segment unitary direction (vector)
        segment_direction_unitary = self.direction_vector_unitary()
        # Sort the points along the segment direction
        self.points.sort(key=lambda pt: np.dot(pt, segment_direction_unitary))

    def get_all_points(self) -> List[Vector3D]:
        """
        Returns all points: segment endpoints + interior points,
        sorted along the segment direction.
        """
        all_points = [self.p1] + self.points + [self.p2]

        # Sort points by projection on segment direction
        ab = self.p2 - self.p1
        ab_unit = ab / np.linalg.norm(ab)

        all_points.sort(key=lambda pt: np.dot(pt, ab_unit))
        return all_points

    def __repr__(self) -> str:
        pts = self.get_all_points()
        pts_str = ', '.join([str(p.tolist()) for p in pts])
        return f"SegmentSliced(segment_end_points=({self.p1, self.p2}), endpoints_slice_idx={self.endpoints_slices_idx} all_points=[{pts_str}])"
