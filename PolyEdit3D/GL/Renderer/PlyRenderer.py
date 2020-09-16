from OpenGL import GL as gl
import ctypes

from .PlyVertexArray import PlyVertexArray
from .PlyIndexBuffer import PlyIndexBuffer
from .PlyShader import PlyShader


class PlyRenderer:
    def init(self):
        gl.glEnable(gl.GL_DEPTH_TEST)

    def clear(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def draw(self, va: PlyVertexArray, ib: PlyIndexBuffer, shader: PlyShader):
        shader.bind()
        va.bind()
        ib.bind()
        gl.glDrawElements(gl.GL_TRIANGLES, ib.index_count , gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
