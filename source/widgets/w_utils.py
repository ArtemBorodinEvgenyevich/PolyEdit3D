import sys
from PySide2 import QtGui, QtConcurrent
from source.widgets.viewport.w_viewport import GlSurfaceFormat


def setWindowSurface(args):
    surface = GlSurfaceFormat()
    surface.printSurfaceInfo()
    QtGui.QSurfaceFormat.setDefaultFormat(surface)

