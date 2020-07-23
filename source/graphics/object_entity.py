import glm


class ObjectEntity:
    def __init__(self):
        self._vertices = []
        self._normals  = []
        self._indices  = []

        self._position = [0, 0, 0]

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertex_array: list):
        self._vertices = vertex_array

    @property
    def normals(self):
        return self._normals

    @normals.setter
    def normals(self, normal_array: list):
        self._normals = normal_array

    @property
    def indices(self):
        return self.indices

    @indices.setter
    def indices(self, index_array: list):
        self._indices = index_array

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, n_position: list):
        self._position = n_position



