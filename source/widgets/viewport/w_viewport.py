from PySide2 import QtWidgets, QtCore, QtGui
from OpenGL import GL


class GlSurfaceFormat(QtGui.QSurfaceFormat):
    def __init__(self):
        super().__init__()

        self.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        self.setMinorVersion(3)
        self.setMajorVersion(4)
        self.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        self.setColorSpace(QtGui.QSurfaceFormat.sRGBColorSpace)
        self.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)

    def printSurfaceInfo(self):
        print(f"QT_SURFACE_FORMAT::{self.__class__.__name__}")
        print("------------------------------>")
        print(f"INFO::GL_MAJOR_VERSION::{self.majorVersion()}")
        print(f"INFO::GL_MINOR_VERSION::{self.minorVersion()}")
        print(f"INFO::GL_PROFILE::{str(self.profile()).split('.')[4]}")
        print(f"INFO::GL_SWAP_BEAHAVIOR::{str(self.swapBehavior()).split('.')[4]}")
        print(f"INFO::QT_RENDERABLE_TYPE::{str(self.renderableType()).split('.')[4]}")
        print(f"INFO::QT_COLOR_SPACE::{str(self.colorSpace()).split('.')[4]}")
        print("------------------------------>\n")


class GlViewportWidget(QtWidgets.QOpenGLWidget):
    instance_list = []

    def __init__(self):
        super().__init__()
        self.bg_color = (0.2, 0.3, 0.3, 1.0)

        GlViewportWidget.instance_list.append(self)

    def initializeGL(self):
        pass

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClearColor(*self.bg_color)

    def resizeGL(self, w:int, h:int):
        GL.glViewport(0, 0, w, h)

    def keyPressEvent(self, event:QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            QtWidgets.QApplication.exit()