from PolyEdit3D.Utilities import AppPaths
from PolyEdit3D.Widgets import PlyViewportToolPanel
from PolyEdit3D.Widgets import PlyBtnSetWireView
from PolyEdit3D.GL.Renderer import VertexBuffer, IndexBuffer, VertexBufferLayout, VertexArray, Shader, Renderer


from OpenGL import GL as gl
from PySide2 import QtWidgets, QtCore, QtGui

import ctypes
import numpy as np


class PlyViewportWidget(QtWidgets.QOpenGLWidget):
    """Main 3D scene viewer."""

    def __init__(self):
        super(PlyViewportWidget, self).__init__(parent=None)

        # --- Setup widget attributes ---
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)

        # -- Init viewport tool panel --
        self.toolPanel = PlyViewportToolPanel(self)

        # - Wireframe button setup -
        self.btnWire = PlyBtnSetWireView(parent=self)
        self.btnWire.geoModeStateChanged.connect(self.onGeoModeChanged)
        self.toolPanel.addButton(self.btnWire, hasSpacer=True)

        # --- Setup View Projection matrices
        self.m_projectionMatrix = QtGui.QMatrix4x4()
        self.m_viewMatrix = QtGui.QMatrix4x4()

        self.m_mouseZoom = -10.0
        self.m_mousePos = QtGui.QVector2D()
        self.m_viewRotation = QtGui.QQuaternion()

        self.renderer = Renderer()

        self.__initUI()

    def __initUI(self):
        """Setup user interface inside the viewport."""
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.layout().addWidget(self.toolPanel)

    def initializeGL(self):
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.renderer.clear()

        vertices = np.array(
            [
                 # Vertex positions     # UVs
                 0.5,  0.5, 0.0,        1.0, 1.0,
                 0.5, -0.5, 0.0,        1.0, 0.0,
                -0.5, -0.5, 0.0,        0.0, 0.0,
                -0.5,  0.5, 0.0,        0.0, 1.0
            ], dtype=ctypes.c_float
        )
        indices = np.array(
            [
                0, 1, 3,
                1, 2, 3
            ], dtype=ctypes.c_uint
        )

        self.shaderProg = Shader(AppPaths.SHADER_ENTITY_BASIC_VERTEX.value, AppPaths.SHADER_ENTITY_BASIC_FRAGMENT.value)
        self.vao = VertexArray()

        self.vbo = VertexBuffer(vertices, vertices.nbytes, gl.GL_STATIC_DRAW)
        layout = VertexBufferLayout()
        layout.pushFloat(3)
        layout.pushFloat(2)
        self.vao.addBuffer(self.vbo, layout)
        self.ebo = IndexBuffer(indices, indices.nbytes, gl.GL_STATIC_DRAW)

        self.vbo.unbind()
        self.ebo.unbind()
        self.vao.unbind()


    def paintGL(self):
        self.renderer.clear()

        # TODO: Put model matrix into model entity
        # This is a *grid* model matrix
        modelMatrix = QtGui.QMatrix4x4()
        modelMatrix.setToIdentity()
        modelMatrix.rotate(90, QtGui.QVector3D(1.0, 0.0, 0.0))
        modelMatrix.scale(1000)

        self.m_viewMatrix.setToIdentity()
        self.m_viewMatrix.translate(0.0, 0.0, self.m_mouseZoom)
        self.m_viewMatrix.rotate(15, QtGui.QVector3D(1.0, 0.0, 0.0))
        self.m_viewMatrix.rotate(self.m_viewRotation)

        self.shaderProg.bind()
        self.shaderProg.setUniformMatrix4fv("u_projectionMatrix", self.m_projectionMatrix.data())
        self.shaderProg.setUniformMatrix4fv("u_viewMatrix", self.m_viewMatrix.data())
        self.shaderProg.setUniformMatrix4fv("u_modelMatrix", modelMatrix.data())

        self.renderer.draw(self.vao, self.ebo, self.shaderProg)

    def resizeGL(self, w: int, h: int):
        aspect = w / h
        self.m_projectionMatrix.setToIdentity()
        self.m_projectionMatrix.perspective(45, aspect, 0.1, 1000.0)

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
        if event.buttons() == QtCore.Qt.LeftButton:
            diff = QtGui.QVector2D(event.localPos()) - self.m_mousePos
            self.m_mousePos = QtGui.QVector2D(event.localPos())
            angle = diff.length() / 2.0
            axis = QtGui.QVector3D(diff.y(), diff.x(), 0.0)
            self.m_viewRotation = QtGui.QQuaternion.fromAxisAndAngle(axis, angle) * self.m_viewRotation
            self.update()
        event.accept()

    def wheelEvent(self, event:QtGui.QWheelEvent):
        if event.delta() > 0:
            self.m_mouseZoom += 0.5
        elif event.delta() < 0:
            self.m_mouseZoom -= 0.5
        self.update()
        event.accept()


    # TODO: Draw wireframe as a texture
    @QtCore.Slot(bool)
    def onGeoModeChanged(self, is_wireframe: bool):
        """Action to perform on 'Wireframe' button click.
        Change viewport' s polygone mode fill."""
        self.makeCurrent()

        if is_wireframe:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            self.update()
            return

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.update()
