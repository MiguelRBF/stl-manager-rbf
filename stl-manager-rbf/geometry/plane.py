# geometry/plane.py

from typing import Optional

import numpy as np

from geometry.vector import Vector
from geometry.segment import Segment

class Plane:
    def __init__(self, point: Vector, normal: Vector):
        if point.shape != (3,) or normal.shape != (3,):
            raise ValueError("Both point and normal must be 3D vectors with shape (3,)")
        self.point: Vector = point
        self.normal: Vector = normal

    def equation(self) -> tuple[float, float, float, float]:
        d = -float(np.dot(self.normal, self.point))
        a, b, c = self.normal
        return (float(a), float(b), float(c), d)

    def intersect_with_segment(self, segment: Segment) -> Optional[Vector]:
        '''Computes the intersection point between the segment and the plane, if it exists within the segment bounds.
        Return:
        - The intersection point as a Vector (i.e. NDArray[np.float64])
        - None if there's no intersection (e.g. segment is parallel or doesn't cross the plane within its endpoints)
        '''
        a = segment.p1
        b = segment.p2
        ab = b - a
        numerator = np.dot(self.normal, self.point - a)
        denominator = np.dot(self.normal, ab)

        # Check if line is parallel (no intersection or lies in plane)
        if np.isclose(denominator, 0.0):
            return None  # Parallel or lies in plane (infinite intersection)

        t = numerator / denominator

        if 0.0 <= t <= 1.0:
            intersection = a + t * ab
            return intersection.astype(np.float64)
        else:
            return None  # Intersection exists outside the segment bounds

    def __repr__(self) -> str:
        a, b, c, d = self.equation()
        return f"Plane({a}x + {b}y + {c}z + {d} = 0)"
