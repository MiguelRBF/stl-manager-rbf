from typing import Union, Tuple, List

import numpy as np

class Vector3D(np.ndarray):
    def __new__(cls, x: Union[List[float], Tuple[float, float, float], np.ndarray]):
        # Convert input to ndarray and ensure it has shape (3,)
        array_np = np.asarray(x, dtype=np.float64).reshape(3)
        # Cast numpy array into current class
        obj = array_np.view(cls)
        return obj

    def __array_finalize__(self, obj):
        """
        Called automatically by NumPy when a new Vector3D instance is created
        from an existing array (e.g., via view(), slicing, or operations).

        This method ensures that any metadata or subclass-specific behavior
        is correctly inherited. If no custom attributes are used, this
        function can be left as a pass-through.

        Parameters:
            obj: The source object from which the new array is derived.
        """
        if obj is None:
            return

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        self[0] = value

    @property
    def y(self) -> float:
        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value

    @property
    def z(self) -> float:
        return self[2]

    @z.setter
    def z(self, value: float):
        self[2] = value

    def norm(self) -> float:
        return np.linalg.norm(self)

    def normalize(self):
        n = self.norm()
        if n == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector3D(self / n)
    
    def is_equal_to(self, vector: 'Vector3D'):
        return np.array_equal(self, vector)

    def dot(self, other: 'Vector3D') -> float:
        return float(np.dot(self, other))

    def cross(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(np.cross(self, other))
