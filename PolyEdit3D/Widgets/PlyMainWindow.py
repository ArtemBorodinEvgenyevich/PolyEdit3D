from PySide2 import QtWidgets, QtCore, QtGui

from PolyEdit3D.Widgets import PlyDockWidget, PlyViewportWidget, PlySceneTreeWidget


class PlyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PlyMainWindow, self).__init__()
        self.w_sceneTree = PlyDockWidget()
        self.w_sceneSettings = None
        self.w_sceneViewport = PlyViewportWidget()

        self.setContentsMargins(5, 5, 5, 5)

        self.__initUI()

    def __initUI(self):
        self.setCentralWidget(self.w_sceneViewport)

        self.w_sceneTree.setWidget(PlySceneTreeWidget())
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.w_sceneTree)

    def showEvent(self, event:QtGui.QShowEvent):
        QtWidgets.QMainWindow.showMaximized(self)