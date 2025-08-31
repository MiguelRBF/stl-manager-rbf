
from typing import List

class TriangleByMeshIndex:
    def __init__(self, vertices_index: List[int], normal_index: int):
        self.vertices_index: List[int] = vertices_index
        self.normal_index: int = normal_index

    def __repr__(self) -> str:
        return f"MeshTriangleByIndex(vertices_index: {self.vertices_index}, normal_index: {self.normal_index})"