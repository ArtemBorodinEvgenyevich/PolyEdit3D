import ctypes
from OpenGL import GL as gl

from .PlyViewportCamera import PlyViewportCamera
from PolyEdit3D.GL.Elements.PlyIMesh import PlyIObjArray, PlyIObjIndexed


class PlyRenderer:
    def init(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)

    def clear(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def draw(self, ply_object, camera: PlyViewportCamera, draw_type=gl.GL_TRIANGLES):
        if isinstance(ply_object, PlyIObjIndexed):
            if hasattr(ply_object, "onDraw"):
                ply_object.onDraw()
            ply_object.passUniforms(camera.projectionMatrix, camera.viewMatrix, ply_object.modelMatrix)

            va, ib = ply_object.vertexArray, ply_object.indexBuffer
            va.bind()
            ib.bind()
            gl.glDrawElements(draw_type, ib.index_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        if isinstance(ply_object, PlyIObjArray):
            if hasattr(ply_object, "onDraw"):
                ply_object.onDraw()
            ply_object.passUniforms(camera.projectionMatrix, camera.viewMatrix, ply_object.modelMatrix)

            va = ply_object.vertexArray
            va.bind()
            gl.glDrawArrays(draw_type, 0, ply_object.vertexAmount)

