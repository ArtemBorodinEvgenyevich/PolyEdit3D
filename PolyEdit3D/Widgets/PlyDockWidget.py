from PySide2 import QtWidgets, QtCore, QtGui


class PlyDockWidget(QtWidgets.QDockWidget):
    """Application docking widget."""
    def __init__(self):
        super(PlyDockWidget, self).__init__()