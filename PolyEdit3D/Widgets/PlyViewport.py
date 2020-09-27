from PolyEdit3D.Utilities import AppPaths
from PolyEdit3D.Widgets import PlyViewportToolPanel
from PolyEdit3D.Widgets import PlyBtnSetWireView
from PolyEdit3D.GL.Renderer import PlyVertexBuffer, PlyIndexBuffer, PlyVertexBufferLayout, PlyVertexArray, PlyShader
from PolyEdit3D.GL.Renderer import PlyRenderer, PlyViewportCamera

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

        self.m_mousePos = QtGui.QVector2D()

        self.renderer = PlyRenderer()
        self.camera = PlyViewportCamera()

        # TODO: move to object entity
        self.vao = None
        self.ebo = None
        self.vbo = None
        self.shaderProg = None

        self.__initUI()

    def __initUI(self):
        """Setup user interface inside the viewport."""
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.layout().addWidget(self.toolPanel)

    def initializeGL(self):

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

        self.shaderProg = PlyShader(AppPaths.SHADER_ENTITY_BASIC_VERTEX.value, AppPaths.SHADER_ENTITY_BASIC_FRAGMENT.value)
        self.vao = PlyVertexArray()

        self.vbo = PlyVertexBuffer(vertices, vertices.nbytes, gl.GL_STATIC_DRAW)
        self.ebo = PlyIndexBuffer(indices, indices.nbytes, gl.GL_STATIC_DRAW)

        layout = PlyVertexBufferLayout()
        layout.pushFloat(3)
        layout.pushFloat(2)
        self.vao.addBuffer(self.vbo, layout)

        self.vbo.unbind()
        self.ebo.unbind()
        self.vao.unbind()

    def paintGL(self):
        self.renderer.init()
        self.renderer.clear()

        # TODO: Put model matrix into model entity
        # This is a *grid* model matrix
        modelMatrix = QtGui.QMatrix4x4()
        modelMatrix.setToIdentity()
        modelMatrix.rotate(90, QtGui.QVector3D(1.0, 0.0, 0.0))
        modelMatrix.scale(1000)

        self.camera.updateCamera()

        self.shaderProg.bind()
        self.shaderProg.setUniformMatrix4fv("u_projectionMatrix", self.camera.projectionMatrix.data())
        self.shaderProg.setUniformMatrix4fv("u_viewMatrix", self.camera.viewMatrix.data())
        self.shaderProg.setUniformMatrix4fv("u_modelMatrix", modelMatrix.data())

        self.renderer.draw(self.vao, self.ebo, self.shaderProg)

    def resizeGL(self, w: int, h: int):
        self.camera.setProjection(w, h)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            self.setFocus()
        elif event.type() == QtCore.QEvent:
            self.clearFocus()
        return super(PlyViewportWidget, self).eventFilter(watched, event)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.m_mousePos = QtGui.QVector2D(event.localPos())

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.camera.rotate(self.m_mousePos, QtGui.QVector2D(event.localPos()))
            self.m_mousePos = QtGui.QVector2D(event.localPos())
        if event.buttons() == QtCore.Qt.RightButton:
            self.camera.pan(self.m_mousePos, QtGui.QVector2D(event.localPos()))
            self.m_mousePos = QtGui.QVector2D(event.localPos())
        self.update()

    def wheelEvent(self, event:QtGui.QWheelEvent):
        self.camera.zoom(event.delta())
        self.update()


    # TODO: Draw wireframe as a texture
    @QtCore.Slot(bool)
    def onGeoModeChanged(self, is_wireframe: bool):
        """Action to perform on 'Wireframe' button click.
        Change viewport' s polygon mode fill."""
        self.makeCurrent()
        if is_wireframe:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            self.update()
            return
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.update()
