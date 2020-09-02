from OpenGL import GL as gl
import ctypes


class VertexBuffer:
    def __init__(self, data, count):
        self.__m_RendererID = None
        self.__count = count
        self.__initBuffer(count, data)

    def __initBuffer(self, count, data):
        self.__m_RendererID = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__m_RendererID)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, count * ctypes.sizeof(ctypes.c_uint), data, gl.GL_STATIC_DRAW)

    def bind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__m_RendererID)

    def unbind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    #def __del__(self):
    #    gl.glDeleteBuffers(self.__m_RendererID)

