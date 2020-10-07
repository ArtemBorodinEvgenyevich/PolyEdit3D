from PolyEdit3D.Widgets import PlyViewportToolPanel
from PolyEdit3D.Widgets import PlyBtnSetWireView
from PolyEdit3D.GL.Renderer import PlyRenderer, PlyViewportCamera
from PolyEdit3D.GL.Elements import PlySceneAxisDots, PlySceneAxisLines, PlySceneGrid

from PolyEdit3D.GL.Elements.SceneElements.TMPPlane import TMPPlane

from OpenGL import GL as gl
from PySide2 import QtWidgets, QtCore, QtGui


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
        self.m_panStart = False

        self.renderer = PlyRenderer()
        self.camera = PlyViewportCamera()

        self.grid = None
        self.scene_dots = None
        self.scene_lines = None

        self.draw_list = list()

        self.__initUI()

    def __initUI(self):
        """Setup user interface inside the viewport."""
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.layout().addWidget(self.toolPanel)

    def screenToWorld(self, mouse_pos: QtGui.QVector2D):
        tmp = QtGui.QVector4D(
            2.0 * mouse_pos.x() / self.width() - 1.0,
            -2.0 * mouse_pos.y() / self.height() + 1.0,
            -1.0, 1.0
        )
        i_tmp = QtGui.QVector4D(
            (tmp * self.camera.projectionMatrix.inverted()[0]).toVector3D(), 0.0
        )
        direction = QtGui.QVector3D(
            (i_tmp * self.camera.viewMatrix.inverted()[0]).toVector3D().normalized()
        )
        cam_pos = QtGui.QVector3D(
            (QtGui.QVector4D(0.0, 0.0, 0.0, 1.0) * self.camera.viewMatrix.inverted()[0]).toVector3D()
        )

        normal = QtGui.QVector3D(0.0, 1.0, 0.0)
        t = -QtGui.QVector3D.dotProduct(cam_pos, normal) / QtGui.QVector3D.dotProduct(direction, normal)
        result = cam_pos + direction * t

        return result

    def initializeGL(self):
        self.renderer.clear()

        self.grid = PlySceneGrid()
        self.scene_dots = PlySceneAxisDots()
        self.scene_lines = PlySceneAxisLines()

    def paintGL(self):
        self.renderer.init()
        self.renderer.clear()

        self.camera.updateCamera()

        for obj in self.draw_list:
            self.renderer.draw(obj, self.camera)

        self.renderer.draw(self.grid, self.camera)
        self.renderer.draw(self.scene_dots, self.camera, draw_type=gl.GL_POINTS)
        self.renderer.draw(self.scene_lines, self.camera, draw_type=gl.GL_LINES)

    def resizeGL(self, w: int, h: int):
        self.camera.setProjection(w, h)

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            self.setFocus()
        elif event.type() == QtCore.QEvent:
            self.clearFocus()
        return super(PlyViewportWidget, self).eventFilter(watched, event)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Shift:
            self.m_panStart = True

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Shift:
            self.m_panStart = False

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.makeCurrent()
        self.m_mousePos = QtGui.QVector2D(event.localPos())

        if event.buttons() == QtCore.Qt.RightButton and not self.m_panStart:
            vec = self.screenToWorld(self.m_mousePos)
            print(vec)
            geo = TMPPlane()
            geo.translate(vec)
            self.draw_list.append(geo)

            self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.camera.rotate(self.m_mousePos, QtGui.QVector2D(event.localPos()))
            self.m_mousePos = QtGui.QVector2D(event.localPos())

        if event.buttons() == QtCore.Qt.RightButton and self.m_panStart:
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
        Change viewport's polygon mode fill."""
        self.makeCurrent()
        if is_wireframe:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            self.update()
            return
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.update()
