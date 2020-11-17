import ctypes
import numpy as np
from PySide2.QtGui import QMatrix4x4, QVector3D
from PolyEdit3D.Utilities import AppPaths
from PolyEdit3D.GL.Elements.PlyIMesh import PlyIObjIndexed
from PolyEdit3D.GL.Renderer import PlyShader, PlyVertexBufferLayout, PlyVertexBuffer, PlyVertexArray, PlyIndexBuffer

vertices = [
             1.0,  1.0, 0.0,
             1.0, -1.0, 0.0,
            -1.0, -1.0, 0.0,
            -1.0,  1.0, 0.0
]
indices = [
            0, 1, 3,
            1, 2, 3
]


class TMPPlane(PlyIObjIndexed):
    """Predefined scene grid object."""
    def __init__(self):
        self.__modelMatrix = QMatrix4x4()
        self.__vertices = vertices
        self.__indices = indices
        self.__shader = None
        self.__vertexArray = None
        self.__indexBuffer = None
        self.__vertexBuffer = None

        self.__translate = QVector3D()
        self.__scale = QVector3D(1.0, 0.0, 1.0)

        self.initObject()

    def initObject(self):
        self.setShaders(AppPaths.SHADER_BASIC_VERTEX.value, AppPaths.SHADER_BASIC_FRAGMENT.value)
        self.__vertexArray = PlyVertexArray()
        self.__vertexBuffer = PlyVertexBuffer(self.vertices, self.vertices.nbytes)
        self.__indexBuffer = PlyIndexBuffer(self.indices, self.indices.nbytes)
        layout = PlyVertexBufferLayout()
        layout.pushFloat(3)
        self.__vertexArray.addBuffer(self.__vertexBuffer, layout)

        self.__vertexBuffer.unbind()
        self.__indexBuffer.unbind()
        self.__vertexArray.unbind()

    def setShaders(self, *paths: str):
        self.__shader = PlyShader(*paths)

    def passUniforms(self, projection_matrix: QMatrix4x4, view_matrix: QMatrix4x4, model_matrix: QMatrix4x4):
        self.__shader.bind()
        self.__shader.setUniformMatrix4fv("u_projectionMatrix", projection_matrix.data())
        self.__shader.setUniformMatrix4fv("u_viewMatrix", view_matrix.data())
        self.__shader.setUniformMatrix4fv("u_modelMatrix", model_matrix.data())

    def onDraw(self):
        self.__modelMatrix.setToIdentity()

        self.__modelMatrix.translate(self.__translate)
        self.__modelMatrix.scale(self.__scale)
        self.__modelMatrix.rotate(90, QVector3D(1.0, 0.0, 0.0))

    @property
    def translateVector(self):
        return self.__translate

    @translateVector.setter
    def translateVector(self, vector: QVector3D):
        self.__translate = vector

    @property
    def scaleVector(self):
        return self.__scale

    @scaleVector.setter
    def scaleVector(self, vector: QVector3D):
        self.__scale = vector

    @property
    def modelMatrix(self):
        return self.__modelMatrix

    @property
    def vertices(self):
        return np.array(self.__vertices, dtype=ctypes.c_float)

    @property
    def indices(self):
        return np.array(self.__indices, dtype=ctypes.c_uint)

    @property
    def vertexArray(self):
        return self.__vertexArray

    @property
    def indexBuffer(self):
        return self.__indexBuffer
