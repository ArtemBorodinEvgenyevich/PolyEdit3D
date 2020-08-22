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
        #     ...

        # --- Setup Model View Projection matrices
        self.m_projectionMatrix = QtGui.QMatrix4x4()

        self.m_mousePos = QtGui.QVector2D()
        self.m_viewRotation = QtGui.QQuaternion()

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

        modelViewMatrix = QtGui.QMatrix4x4()
        modelViewMatrix.setToIdentity()
        modelViewMatrix.translate(0.0, 0.0, -3.0)
        modelViewMatrix.rotate(self.m_viewRotation)

        gl.glUseProgram(self.shaderProg)

        mvp_loc = gl.glGetUniformLocation(self.shaderProg, "mvp")
        mvp = self.m_projectionMatrix * modelViewMatrix
        gl.glUniformMatrix4fv(mvp_loc, 1, gl.GL_FALSE, mvp.data())

        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

    def resizeGL(self, w: int, h: int):
        aspect = w / h
        self.m_projectionMatrix.setToIdentity()
        self.m_projectionMatrix.perspective(45, aspect, 0.1, 10.0)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            self.setFocus()
        elif event.type() == QtCore.QEvent:
            self.clearFocus()

        return super(PlyViewportWidget, self).eventFilter(watched, event)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.m_mousePos = QtGui.QVector2D(event.localPos())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() != QtCore.Qt.LeftButton:
            event.ignore()

        diff = QtGui.QVector2D(event.localPos()) - self.m_mousePos
        self.m_mousePos = QtGui.QVector2D(event.localPos())

        angle = diff.length() / 2.0
        axis = QtGui.QVector3D(diff.y(), diff.x(), 0.0)
        self.m_viewRotation = QtGui.QQuaternion.fromAxisAndAngle(axis, angle) * self.m_viewRotation

        self.update()
        event.accept()
