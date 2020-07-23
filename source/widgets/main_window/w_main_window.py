from PySide2 import QtWidgets, QtGui
from source.widgets.viewport.w_viewport import GlViewportWidget
from source.widgets.main_window.w_central_widget import CentralWidget


# TODO:
class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.addToolBar(QtWidgets.QToolBar())
        self.setCentralWidget(CentralWidget())

    def showEvent(self, event: QtGui.QShowEvent):
        QtWidgets.QMainWindow.showMaximized(self)
