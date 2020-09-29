from OpenGL import GL as gl
import ctypes

from .PlyVertexArray import PlyVertexArray
from .PlyIndexBuffer import PlyIndexBuffer
from .PlyShader import PlyShader


class PlyRenderer:
    def init(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)

    def clear(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def drawElements(self, va: PlyVertexArray, ib: PlyIndexBuffer, shader: PlyShader, draw_type=gl.GL_TRIANGLES):
        shader.bind()
        va.bind()
        ib.bind()
        gl.glDrawElements(draw_type, ib.index_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

    def drawArrays(self, va: PlyVertexArray, shader: PlyShader, draw_type=gl.GL_POINTS, number_of_dots=1, start_index=0):
        shader.bind()
        va.bind()
        gl.glDrawArrays(draw_type, start_index, number_of_dots)


