from PolyEdit3D.Widgets.PlyToolPanel import PlyViewportToolPanel, PlyBtnSetWireView, PlyBtnDrawPlaneByVector
from PolyEdit3D.GL.Renderer import PlyRenderer, PlyViewportCamera
from PolyEdit3D.GL.Elements import PlySceneAxisDots, PlySceneAxisLines, PlySceneGrid
from PolyEdit3D.GL.GeometryEngine import GeometryEngine, PlyEditEnum

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
        self.btnWire.clicked.connect(self.onGeoModeChanged)

        self.btnPlnVec = PlyBtnDrawPlaneByVector(parent=self)
        self.btnPlnVec.clicked.connect(self.onPlaneVecDrawStateChanged)

        self.editState = PlyEditEnum.IDLE

        self.geoEngine = GeometryEngine()
        self.renderer = PlyRenderer()
        self.camera = PlyViewportCamera()

        self.grid = None
        self.scene_dots = None
        self.scene_lines = None

        self.draw_list = list()

        self.first_point = QtGui.QVector3D()
        self.move_point = QtGui.QVector3D()

        self.__initUI()

    def __initUI(self):
        """Setup user interface inside the viewport."""
        self.toolPanel.addButton(self.btnPlnVec, hasSpacer=True)
        self.toolPanel.addButton(self.btnWire, hasSpacer=True)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.layout().addWidget(self.toolPanel)

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
            self.camera.isPanEnabled = True
            print(self.geoEngine.currentObject)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Shift:
            self.camera.isPanEnabled = False

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.makeCurrent()
        self.camera.mousePos = QtGui.QVector2D(event.localPos())

        if event.buttons() == QtCore.Qt.RightButton and self.editState == PlyEditEnum.DRAW_PLANE:
            click_pos = self.camera.getRayGridIntersecton(self.camera.mousePos)
            self.geoEngine.startPoint = click_pos
            self.geoEngine.movePoint = click_pos
            self.geoEngine.setObject(TMPPlane())
            self.geoEngine.setScaleByScalar(0.0)
            self.geoEngine.setTranslationByVector(click_pos)
            self.draw_list.append(self.geoEngine.currentObject)

        self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.RightButton and self.editState == PlyEditEnum.DRAW_PLANE:
            self.geoEngine.releaseObject()
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.buttons() == QtCore.Qt.RightButton and self.editState == PlyEditEnum.DRAW_PLANE:
            self.geoEngine.planeFromVector(self.camera.getRayGridIntersecton(QtGui.QVector2D(event.localPos())))

        if event.buttons() == QtCore.Qt.LeftButton:
            self.camera.rotate(self.camera.mousePos, QtGui.QVector2D(event.localPos()))
            self.camera.mousePos = QtGui.QVector2D(event.localPos())

        if event.buttons() == QtCore.Qt.RightButton and self.camera.isPanEnabled:
            self.camera.pan(self.camera.mousePos, QtGui.QVector2D(event.localPos()))
        self.update()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        self.camera.zoom(event.delta())
        self.update()

    # TODO: Draw wireframe as a texture
    def onGeoModeChanged(self, ):
        """Action to perform on 'Wireframe' button click.
        Change viewport's polygon mode fill."""
        self.makeCurrent()
        if not self.btnWire.isChecked():
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
            self.update()
            return
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        self.update()

    def onPlaneVecDrawStateChanged(self):
        if self.btnPlnVec.isChecked() and self.editState == PlyEditEnum.IDLE:
            self.editState = PlyEditEnum.DRAW_PLANE
        if not self.btnPlnVec.isChecked() and self.editState == PlyEditEnum.DRAW_PLANE:
            self.editState = PlyEditEnum.IDLE
        self.update()
