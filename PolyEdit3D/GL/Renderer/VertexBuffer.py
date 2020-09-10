from OpenGL import GL as gl
import ctypes


class VertexBuffer:
    def __init__(self, data, count, draw_state=gl.GL_STATIC_DRAW):
        self.__m_RendererID = gl.glGenBuffers(1)
        self.__count = count
        self.__initBuffer(count, data, draw_state)

    def __initBuffer(self, count, data, draw_state):
        self.bind()
        gl.glBufferData(gl.GL_ARRAY_BUFFER, count * ctypes.sizeof(ctypes.c_uint), data, draw_state)

    def bind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.__m_RendererID)

    def unbind(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
