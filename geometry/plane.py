# geometry/plane.py

from typing import Optional

import numpy as np

from geometry.vector import Vector3D
from geometry.segment import Segment

class Plane:
    def __init__(self, point: Vector3D, normal: Vector3D):
        self.point: Vector3D = point
        self.normal: Vector3D = normal

    def equation(self) -> tuple[float, float, float, float]:
        d = -float(np.dot(self.normal, self.point))
        a, b, c = self.normal
        return (float(a), float(b), float(c), d)

    def intersect_with_segment(self, segment: Segment) -> Optional[Vector3D]:
        '''Computes the intersection point between the segment and the plane, if it exists within the segment bounds.
        Return:
        - The intersection point
        - None if there's no intersection (e.g. segment is parallel or doesn't cross the plane within its endpoints)
        '''
        segment_vector = segment.direction_vector()
        numerator = np.dot(self.normal, self.point - segment.p1)
        denominator = np.dot(self.normal, segment_vector)

        # Check if line is parallel (no intersection or lies in plane)
        if np.isclose(denominator, 0.0):
            return None  # Parallel or lies in plane (infinite intersection)

        t = numerator / denominator

        if 0.0 <= t <= 1.0:
            intersection = segment.p1 + t * segment_vector
            return intersection
        else:
            return None  # Intersection exists outside the segment bounds

    def __repr__(self) -> str:
        a, b, c, d = self.equation()
        return f"Plane({a}x + {b}y + {c}z + {d} = 0)"
