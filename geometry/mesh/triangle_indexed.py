from typing import List

class TriangleIndexed:
    """
    Class that stores a mesh triangle vertex and normal data using its indexes instead of values
    """

    def __init__(self,triangle_index:int, vertices_index: List[int], normal_index: int):
        self.triangle_index = triangle_index
        self.vertices_index: List[int] = vertices_index
        self.normal_index: int = normal_index

    def __repr__(self) -> str:
        return f"MeshTriangleByIndex(vertices_index: {self.vertices_index}, normal_index: {self.normal_index})"