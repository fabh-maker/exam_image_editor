from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
from typing import Optional


@dataclass
class TupleRC:
    r: int
    c: int

class GraphicalElement(ABC):

    # R1
    @property
    def name(self):
        pass

    @property
    def dims(self) -> TupleRC:
        pass

    @property
    @abstractmethod
    def bitmap(self) -> List[List[int]]:
        pass

    # R4
    def overlay(self, layer: "GraphicalElement", pos: TupleRC) -> None:
        upper_layer = layer.bitmap
        for i in range(len(upper_layer)):
            for j in range(len(upper_layer[0])):
                corrected_row = pos.r + i
                corrected_column = pos.c + j
                if 0 <= corrected_row < self._dims.r and 0 <= corrected_column < self._dims.c:
                    self._grid[corrected_row][corrected_column] = upper_layer[i][j]


class Matrix(GraphicalElement):
    def __init__(self,name,dims:TupleRC,color:int):
        self._dims = dims
        self._name = name
        self._grid = [[color for _ in range(dims.c)] for _ in range(dims.r)]
    @property
    def name(self):
        return self._name
    @property
    def dims(self) -> TupleRC:
        return self._dims
    @property
    def bitmap(self) -> List[List[int]]:
        return self._grid


class DifferentPMatrix(GraphicalElement):
    def __init__(self,name,colour_tab,rows,columns):
        self._dims = TupleRC(rows,columns)
        self._name = name
        self._grid = colour_tab

    @property
    def name(self):
        return self._name

    @property
    def dims(self) -> TupleRC:
        return self._dims

    @property
    def bitmap(self) -> List[List[int]]:
        return self._grid


class Layer:
    
    # R2
    def __init__(self,element,vertex:TupleRC,prev=None,next_=None):
        self._graphical_element = element
        self._pos = vertex
        self._previous = prev
        self._next = next_

    def set_next(self,new_next):
        self._next = new_next
    @property
    def elm(self) -> GraphicalElement:
        return self._graphical_element
    
    @property
    def pos(self) -> TupleRC:
        return self._pos

    @property
    def below(self) -> Optional["Layer"]:
        return self._previous
    @below.setter
    def below(self,below):
        self._previous = below
    @property
    def above(self) -> Optional["Layer"]:
        return self._next
    @above.setter
    def above(self,above):
        self._next = above
    
    # R4
    def render(self, dims: TupleRC) -> GraphicalElement:
        result = Matrix("render", dims, 0)
        layers = []
        layer = self
        while layer is not None:
            layers.append(layer)
            layer = layer.below
        for lay in reversed(layers):
            result.overlay(lay.elm, lay.pos)
        return result
   