import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QSurfaceFormat
from PySide2.QtCore import Qt

from PolyEdit3D.Widgets import PlyMainWindow
from PolyEdit3D.GL.Setup import GLSurfaceFormat


if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
    QSurfaceFormat.setDefaultFormat(GLSurfaceFormat())

    app = QApplication()

    window = PlyMainWindow()
    window.show()

    sys.exit(app.exec_())
