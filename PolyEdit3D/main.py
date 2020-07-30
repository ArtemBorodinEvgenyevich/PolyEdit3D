import sys
from PySide2 import QtWidgets, QtGui

from PolyEdit3D.Widgets import PlyMainWindow
from PolyEdit3D.GL import GLSurfaceFormat


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    QtGui.QSurfaceFormat.setDefaultFormat(GLSurfaceFormat())

    window = PlyMainWindow()
    window.show()

    sys.exit(app.exec_())
