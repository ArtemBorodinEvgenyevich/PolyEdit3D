from OpenGL import GL as gl
from .PlyVertexBuffer import PlyVertexBuffer
from .PlyVertexBufferLayout import PlyVertexBufferLayout
import ctypes


class PlyVertexArray:
    def __init__(self):
        self.__mRendererId = gl.glGenVertexArrays(1)
        self.bind()

    def addBuffer(self, vb: PlyVertexBuffer, layout: PlyVertexBufferLayout):
        self.bind()

        vb.bind()
        layout_elements = layout.elements

        for i in range(len(layout_elements)):
            element = layout_elements[i]
            gl.glEnableVertexAttribArray(i)
            gl.glVertexAttribPointer(i, element.count, element.type,
                                     element.normalized, layout.stride, ctypes.c_void_p(element.offset))

    def bind(self):
        gl.glBindVertexArray(self.__mRendererId)

    def unbind(self):
        gl.glBindVertexArray(0)

