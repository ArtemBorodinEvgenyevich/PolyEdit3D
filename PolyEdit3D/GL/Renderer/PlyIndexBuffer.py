from OpenGL import GL as gl


class PlyIndexBuffer:
    def __init__(self, data, size, draw_state=gl.GL_STATIC_DRAW):
        self.__rendererID = gl.glGenBuffers(1)
        self.__index_count = len(data)
        self.__initBuffer(size, data, draw_state)

    def __initBuffer(self, size, data, draw_state):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.__rendererID)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, size, data, draw_state)

    def bind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.__rendererID)

    def unbind(self):
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

    # FIXME
    @property
    def index_count(self):
        return self.__index_count
