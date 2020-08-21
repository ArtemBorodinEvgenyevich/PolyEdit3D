from PolyEdit3D.Utilities import AppPaths
from OpenGL import GL as gl
from OpenGL.GL.shaders import compileShader, compileProgram
import ctypes
import numpy as np


# FIXME: fix problem with vertex attributes and entity translate matrix
class Grid:
    """Viewport main grid entity."""
    def __init__(self, parent=None):
        self.parent = parent

        self.vertices = np.array(
            [
                 0.5,  0.5, 0.0,
                 0.5, -0.5, 0.0,
                -0.5, -0.5, 0.0,
                -0.5,  0.5, 0.0
            ], dtype=ctypes.c_float
        )

        self.indices = np.array(
            [
                0, 1, 3,
                1, 2, 3
            ], dtype=ctypes.c_uint
        )

        # TODO: Create separate Buffer to store scene entities
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.shaderProg = None

    # TODO: De-attach shader program after using once
    # TODO: Use separate shader for grid
    def compileShaders(self):
        """Compile given shaders and use globally."""
        self.parent.accessViewportGLContext()

        with open(AppPaths.SHADER_ENTITY_BASIC_FRAGMENT.value, "r") as source:
            fragment = compileShader(source.read(), gl.GL_FRAGMENT_SHADER)
        with open(AppPaths.SHADER_ENTITY_BASIC_VERTEX.value, "r") as source:
            vertex = compileShader(source.read(), gl.GL_VERTEX_SHADER)

        self.shaderProg = compileProgram(vertex, fragment)

    def setupBuffers(self):
        """Setup and bind basic buffers."""
        self.parent.accessViewportGLContext()

        self.VAO = gl.glGenVertexArrays(1)
        self.VBO = gl.glGenBuffers(1)
        self.EBO = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.VAO)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.VBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))

        # Unbind buffers except EBO (must be bind)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def __str__(self):
        return f"Grid Object:\n" \
               f"Vertices: {self.vertices}\n" \
               f"Indices: {self.indices}\n"
