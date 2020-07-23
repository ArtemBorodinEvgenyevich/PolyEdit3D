import sys
from source.widgets.w_utils import setWindowSurface
from source.widgets.main_window.w_main_window import AppMainWindow
from PySide2 import QtWidgets, QtGui


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    setWindowSurface(sys.argv)

    window = AppMainWindow()
    window.show()

    sys.exit(app.exec_())
