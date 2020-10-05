import ctypes
import numpy as np
from PySide2.QtGui import QMatrix4x4, QVector3D
from PolyEdit3D.Utilities import AppPaths
from PolyEdit3D.GL.Elements.PlyIMesh import PlyIObjArray
from PolyEdit3D.GL.Renderer import PlyShader, PlyVertexBufferLayout, PlyVertexBuffer, PlyVertexArray, PlyIndexBuffer


vertices = [
        #   Position             Colour
            0.0, 0.0, 0.0,       1.0, 1.0, 0.0,

            0.0, 1.0, 0.0,       0.0, 1.0, 0.0,
            0.0, 2.0, 0.0,       0.0, 1.0, 0.0,
            0.0, 3.0, 0.0,       0.0, 1.0, 0.0,
            0.0, 4.0, 0.0,       0.0, 1.0, 0.0,

            1.0, 0.0, 0.0,       1.0, 0.0, 0.0,
            2.0, 0.0, 0.0,       1.0, 0.0, 0.0,
            3.0, 0.0, 0.0,       1.0, 0.0, 0.0,
            4.0, 0.0, 0.0,       1.0, 0.0, 0.0,

            0.0, 0.0, -1.0,      0.0, 0.0, 1.0,
            0.0, 0.0, -2.0,      0.0, 0.0, 1.0,
            0.0, 0.0, -3.0,      0.0, 0.0, 1.0,
            0.0, 0.0, -4.0,      0.0, 0.0, 1.0
]


class PlySceneAxisDots(PlyIObjArray):
    """Predefined viewport scene axis dots object."""
    def __init__(self):
        self.__modelMatrix = QMatrix4x4()
        self.__vertices = vertices
        self.__vertexAmount = 0
        self.__shader = None
        self.__vertexArray = None
        self.__vertexBuffer = None

        self.initObject()

    def initObject(self):
        self.setShaders(AppPaths.SHADER_COORD_DOTS_VERTEX.value, AppPaths.SHADER_COORD_DOTS_FRAGMENT.value)
        self.__vertexArray = PlyVertexArray()
        self.__vertexBuffer = PlyVertexBuffer(self.vertices, self.vertices.nbytes)
        layout = PlyVertexBufferLayout()
        layout.pushFloat(3)
        layout.pushFloat(3)
        self.__vertexArray.addBuffer(self.__vertexBuffer, layout)

        cnt = 1
        for _ in range(0, len(self.__vertices), layout.count):
            self.__vertexAmount += cnt

        self.__vertexBuffer.unbind()
        self.__vertexArray.unbind()

    def setShaders(self, *paths: str):
        self.__shader = PlyShader(*paths)

    def passUniforms(self, projection_matrix: QMatrix4x4, view_matrix: QMatrix4x4, model_matrix: QMatrix4x4):
        self.__shader.bind()
        self.__shader.setUniformMatrix4fv("u_projectionMatrix", projection_matrix.data())
        self.__shader.setUniformMatrix4fv("u_viewMatrix", view_matrix.data())
        self.__shader.setUniformMatrix4fv("u_modelMatrix", model_matrix.data())

    @property
    def vertexAmount(self):
        return self.__vertexAmount

    @property
    def modelMatrix(self):
        return self.__modelMatrix

    @property
    def vertices(self):
        return np.array(self.__vertices, dtype=ctypes.c_float)

    @property
    def vertexArray(self):
        return self.__vertexArray
