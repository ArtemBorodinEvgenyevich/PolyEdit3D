from PySide2 import QtGui, QtCore

from .PlyViewportToolButton import PlyViewportToolButton
from PolyEdit3D.Utilities import AppPaths
from PolyEdit3D.GL.GeometryEngine import PlyEditEnum

class PlyBtnSetWireView(PlyViewportToolButton):
    """Tool button for polygon mode change."""
    def __init__(self, parent=None):
        super(PlyBtnSetWireView, self).__init__(parent)
        self.setCheckable(True)
        self.setIcon(QtGui.QPixmap(AppPaths.BTN_WIREFRAME_ICON.value))


class PlyBtnDrawPlaneByVector(PlyViewportToolButton):
    """Tool button for polygon mode change."""
    def __init__(self, parent=None):
        super(PlyBtnDrawPlaneByVector, self).__init__(parent)
        self.setCheckable(True)
        self.setIcon(QtGui.QPixmap(AppPaths.BTN_PLN_VEC_ICON.value))
