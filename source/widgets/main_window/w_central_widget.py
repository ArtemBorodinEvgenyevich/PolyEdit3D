from PySide2 import QtWidgets
from source.widgets.viewport.w_viewport import GlViewportWidget
from source.widgets.main_window.w_splitter import WindowSplitter


class CentralWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.splitter = WindowSplitter()
        self._initUI()


    def _initUI(self):
        self.setLayout(QtWidgets.QHBoxLayout())

        self.layout().addWidget(self.splitter)
        self.splitter.addWidget(GlViewportWidget())
        self.splitter.addWidget(QtWidgets.QWidget())
        self.splitter.addWidget(QtWidgets.QWidget())

