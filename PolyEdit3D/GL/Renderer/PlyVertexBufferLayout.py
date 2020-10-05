from OpenGL import GL as gl
import ctypes


class VertexAttributeElement:
    def __init__(self, gl_type: gl.GLenum, count: int, offset: int, normalized: bool):
        self.__mType = gl_type
        self.__mCount = count
        self.__mNormalized = gl.GL_TRUE if normalized else gl.GL_FALSE
        self.__mOffset = offset

    @property
    def count(self):
        return self.__mCount

    @property
    def offset(self):
        return self.__mOffset

    @property
    def normalized(self):
        return self.__mNormalized

    @property
    def type(self):
        return self.__mType

    @staticmethod
    def getTypeSize(gl_type: gl.GLenum):
        gl_type_size = {
            gl.GL_FLOAT: ctypes.sizeof(ctypes.c_float),
            gl.GL_UNSIGNED_INT: ctypes.sizeof(ctypes.c_uint),
            gl.GL_UNSIGNED_BYTE: ctypes.sizeof(ctypes.c_ubyte)
        }
        return gl_type_size[gl_type]


class PlyVertexBufferLayout:
    def __init__(self):
        self.__mElements = []
        self.__mElementsCount = 0
        self.__mStride = 0

    def __getOffset(self):
        if self.__mElementsCount != 0:
            return self.__mElementsCount * ctypes.sizeof(ctypes.c_float)
        return self.__mElementsCount

    def pushFloat(self, elements_count: int):
        self.__mElements.append(VertexAttributeElement(gl.GL_FLOAT, elements_count, self.__getOffset(), False))
        self.__mElementsCount += elements_count
        self.__mStride += elements_count * ctypes.sizeof(ctypes.c_float)

    @property
    def count(self):
        return self.__mElementsCount

    @property
    def stride(self):
        return self.__mStride

    @property
    def elements(self):
        return self.__mElements
