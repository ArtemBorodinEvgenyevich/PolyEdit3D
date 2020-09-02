from OpenGL import GL as gl
import ctypes


class IndexBuffer:
    def __init__(self, data, size):
        self.__rendererID = None

        self.__initBuffer(size, data)

    def __initBuffer(self, size, data):
        self.__rendererID = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.__rendererID)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, size, data, gl.GL_STATIC_DRAW)

    def bind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.__rendererID)

    def unbind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    def getCount(self):
        return 0

    #def __del__(self):
    #    gl.glDeleteBuffers(self.__rendererID)

