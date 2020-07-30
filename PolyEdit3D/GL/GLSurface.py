from PySide2 import QtWidgets, QtCore, QtGui


class GLSurfaceFormat(QtGui.QSurfaceFormat):
    def __init__(self):
        super(GLSurfaceFormat, self).__init__()
        self.__initSurface()

    def __initSurface(self):
        try:
            self.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
            self.setMinorVersion(3)
            self.setMajorVersion(4)
            self.setProfile(QtGui.QSurfaceFormat.CoreProfile)
            self.setColorSpace(QtGui.QSurfaceFormat.sRGBColorSpace)
            self.setSwapBehavior(QtGui.QSurfaceFormat.DoubleBuffer)
        except Exception as gl_error:
            print(gl_error)
            exit(0)

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
