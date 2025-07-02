from image_editor.elements import TupleRC, GraphicalElement, Layer, Matrix, DifferentPMatrix
from image_editor.exceptions import ImageEditorException


class ImageEditor:
    
    # R1
    def __init__(self):
        self._graphic_elements = {}
        self._layers = []

    def new_rectangle(self, name: str, dims: TupleRC, color: int) -> GraphicalElement:
        if name not in self._graphic_elements:
            element = Matrix(name,dims,color)
            self._graphic_elements[name] = element
            return element
        raise ImageEditorException

    def new_image(self, name: str, fname: str) -> GraphicalElement:
        if name not in self._graphic_elements:
            try:
                with open(fname,'r',encoding='UTF-8') as fin:
                    tab = []
                    for row in fin:
                        row = [int(x) for x in row.strip().split()]
                        tab.append(row)
                    rows = len(tab)
                    columns = len(tab[0])
                    element = DifferentPMatrix(name,tab,rows,columns)
            except Exception():
                raise ImageEditorException
            self._graphic_elements[name] = element
            return element
        raise ImageEditorException

    # R2
    def add_layer(self, elm_name: str, pos: TupleRC) -> Layer:
        if elm_name in self._graphic_elements:
            #if len(self._layers) == 0:
            layer = Layer(self._graphic_elements[elm_name],pos,None,None)
            #else:
                #layer = Layer(self._graphic_elements[elm_name],pos,self._layers[-1],None)
                #self._layers[-1].set_next(layer)
            self._layers.append(layer)
            self._set_layers() if len(self._layers) > 1 else None
            return layer
        raise ImageEditorException

    def _set_layers(self):
        for i, lay in enumerate(self._layers):
                lay.below = self._layers[i-1] if i > 0 else None
                lay.above = self._layers[i+1] if i < len(self._layers)-1 else None

    # R3
    def move_below(self, layer: Layer) -> None:
        id = self._layers.index(layer)
        if id == 0:
            return ImageEditorException('Already at the bottom')
        self._layers[id-1],self._layers[id] = self._layers[id],self._layers[id-1]
        self._set_layers()
