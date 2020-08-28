import numpy as np
import ctypes


class VertexData:
    def __init__(self, vertex_pos: list, tex_coord: list,):
        if len(vertex_pos) != 3 or len(tex_coord) != 2:
            raise RuntimeWarning("Incorrect or missing vertex data!")

        self.__vertexPosition = vertex_pos
        self.__textureCoords = tex_coord

    @property
    def vertexPosition(self):
        return np.array(self.__vertexPosition, dtype=ctypes.c_float)

    @property
    def textureCoords(self):
        return np.array(self.__textureCoords, dtype=ctypes.c_float)

    @property
    def byteSize(self):
        return self.vertexPosition.nbytes + self.textureCoords.nbytes


class VertexArray:
    def __init__(self, *args: VertexData):

        self.__elements = []
        self.__size_float = ctypes.sizeof(ctypes.c_float)

        if args:
            for vertex in args:
                self.append(vertex)

    def append(self, vertex_data: VertexData):
        data = [*vertex_data.vertexPosition, *vertex_data.textureCoords]
        self.__elements += data

    @property
    def data(self):
        if len(self.__elements) == 0:
            return self.__elements
        return np.array(self.__elements, dtype=ctypes.c_float)

    @property
    def byteSize(self):
        return len(self.__elements) * self.__size_float

    def __add__(self, other):
        new_vertex_array = VertexArray()
        new_vertex_array.__elements += self.__elements
        new_vertex_array.__elements += other.__elements
        return new_vertex_array

    def __iadd__(self, other):
        self.__elements += other.__elements
        return self

    def __len__(self):
        return len(self.__elements)

    def __repr__(self):
        return f"PlyVertexArray({self.__elements})"

    def __iter__(self):
        self.__iter_index = 0
        return self

    def __next__(self):
        if self.__iter_index < len(self.__elements):
            self.__iter_index += 1
            return self.__elements[self.__iter_index - 1]
        raise StopIteration


class IndexArray:
    def __init__(self, *args: list):
        self.__indices = []
        self.__size_uint = ctypes.sizeof(ctypes.c_uint)

        if args:
            self.__indices = [*args]

    def append(self, index: int):
        self.__indices.append(index)

    @property
    def data(self):
        if len(self.__indices) == 0:
            return self.__indices
        return np.array(self.__indices, dtype=ctypes.c_uint)

    @property
    def byteSize(self):
        return len(self.__indices) * self.__size_uint

    def __repr__(self):
        return f"PlyIndexArray({self.__indices})"



if __name__ == '__main__':
    v1 = VertexData([1.1, 1.2, 1.3], [1.1, 1.1])
    v2 = VertexData([2.1, 2.2, 2.3], [1.1, 1.0])
    i1 = IndexArray()

    print(v1.vertexPosition, v1.textureCoords, v1.byteSize)
    print(v2.vertexPosition, v2.textureCoords, v2.byteSize)

    ar = VertexArray()
    print(ar)
    ar.append(v1)
    print(ar)

    ar1 = VertexArray(v2)
    print(ar1)

    print(ar1.data)
    d = ar1.data

    print(i1, i1.data, i1.byteSize)

    for i in range(4):
        i1.append(i)

    print(i1.data, i1.byteSize)