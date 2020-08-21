from PolyEdit3D.Utilities import AppPaths
from PolyEdit3D.Widgets import PlyViewportToolPanel
from PolyEdit3D.Widgets import PlyBtnSetWireView
from PolyEdit3D.GL.Entities import Grid

from OpenGL import GL as gl
from OpenGL.GL.shaders import compileShader, compileProgram
from PySide2 import QtWidgets, QtCore, QtGui

import glm
import ctypes
import numpy as np


class PlyViewportWidget(QtWidgets.QOpenGLWidget):
    """Main 3D scene viewer."""
    def __init__(self):
        super(PlyViewportWidget, self).__init__(parent=None)

        # --- Setup widget attributes ---
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)

        # --- Setup widget UI ---

        # -- Init viewport toolpanel --
        self.toolPanel = PlyViewportToolPanel(self)

        # - Wireframe button setup -
        self.btnWire = PlyBtnSetWireView(parent=self)
        self.btnWire.geoModeStateChanged.connect(self.onGeoModeChanged)
        self.toolPanel.addButton(self.btnWire, hasSpacer=True)

        # --- Setup scene entities ---

        # --- Setup Model View Projection matrices
        self.m_modelMatrix = glm.rotate(glm.mat4(1.0), glm.radians(0), glm.vec3(1.0, 0.0, 0.0))
        self.m_viewMatrix = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -3.0))
        self.m_projectionMatrix = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 100.0)

        self.v_mousePosition = glm.vec2()
        self.m_viewRotation = glm.quat()

        self.__initUI()

        # TODO: create new buffer for individual object
        # TODO: Or use batch rendering
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.shaderProg = None

    def accessViewportGLContext(self):
        """Simple alias for `::makeCurrent()` to improve readability."""
        self.makeCurrent()

    def __initUI(self):
        """Setup user interface inside the viewport."""
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.layout().addWidget(self.toolPanel)

    @QtCore.Slot(bool)
    def onGeoModeChanged(self, isWireframe: bool):
        """Action to perform on 'Wireframe' button click.
        Change viewport' s polygone mode fill."""
        self.accessViewportGLContext()

        if isWireframe:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            self.update()
            return

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.update()

    def initializeGL(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(0.4, 0.4, 0.4, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT, gl.GL_DEPTH_BUFFER_BIT)

        with open(AppPaths.SHADER_ENTITY_BASIC_FRAGMENT.value, 'r') as f:
            fragment = compileShader(f.read(), gl.GL_FRAGMENT_SHADER)
        with open(AppPaths.SHADER_ENTITY_BASIC_VERTEX.value, "r") as f:
            vertex = compileShader(f.read(), gl.GL_VERTEX_SHADER)
        self.shaderProg = compileProgram(vertex, fragment)

        vertices = np.array(
            [
                0.5, 0.5, 0.0,
                0.5, -0.5, 0.0,
                -0.5, -0.5, 0.0,
                -0.5, 0.5, 0.0
            ], dtype=ctypes.c_float
        )
        indices = np.array(
            [
                0, 1, 3,
                1, 2, 3
            ], dtype=ctypes.c_uint
        )

        self.vao = gl.glGenVertexArrays(1)
        self.vbo = gl.glGenBuffers(1)
        self.ebo = gl.glGenBuffers(1)

        gl.glBindVertexArray(self.vao)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)

        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def paintGL(self):
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glUseProgram(self.shaderProg)

        #self.m_viewMatrix = glm.rotate(s)

        # Apply MVP transformation
        model_loc = gl.glGetUniformLocation(self.shaderProg, "model")
        gl.glUniformMatrix4fv(model_loc, 1, gl.GL_FALSE, glm.value_ptr(self.m_modelMatrix))
        view_loc = gl.glGetUniformLocation(self.shaderProg, "view")
        gl.glUniformMatrix4fv(view_loc, 1, gl.GL_FALSE, glm.value_ptr(self.m_viewMatrix))
        projection_loc = gl.glGetUniformLocation(self.shaderProg, "projection")
        gl.glUniformMatrix4fv(projection_loc, 1, gl.GL_FALSE, glm.value_ptr(self.m_projectionMatrix))

        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

    def resizeGL(self, w: int, h: int):
        gl.glViewport(0, 0, w, h)

    def eventFilter(self, watched:QtCore.QObject, event:QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            self.setFocus()
        elif event.type() == QtCore.QEvent:
            self.clearFocus()
            
        return super(PlyViewportWidget, self).eventFilter(watched, event)

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.v_mousePosition = glm.vec2(event.localPos().x(), event.localPos().y())
        event.accept()

    def mouseMoveEvent(self, event:QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            pos_diff = glm.vec2(event.localPos().x(), event.localPos().y()) - self.v_mousePosition
            self.v_mousePosition = glm.vec2(event.localPos().x(), event.localPos().y())

            # Calculate viewport rotation axis and angle
            rot_angle = glm.length(pos_diff) / 2.0
            rot_axis = glm.vec3(pos_diff, 0.0)
            self.m_viewMatrix = glm.rotate(self.m_viewMatrix, glm.radians(rot_angle), rot_axis)
            self.update()

        event.accept()

    def keyPressEvent(self, event:QtGui.QKeyEvent):
        event.accept()

