from PolyEdit3D.Utilities import AppPaths
from PySide2 import QtWidgets, QtGui, QtCore


class PlyViewportToolPanel(QtWidgets.QWidget):
    """Viewport tool widget with the most useful actions."""
    def __init__(self, parent=None):
        super(PlyViewportToolPanel, self).__init__(parent)

        self.colorBackground = QtGui.QColor(89, 89, 89)
        self.qBrush = QtGui.QBrush(self.colorBackground)

        self.setFixedWidth(82)
        self.setContentsMargins(0, 4, 0, 4)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.__initUI()

    def __initUI(self):
        """Set widget layout."""
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setSpacing(1)
        self.layout().setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

    def paintEvent(self, event:QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        widgetRect = self.rect().adjusted(5, 5, -5, -5)
        painter.setBrush(self.qBrush)
        painter.drawRoundedRect(widgetRect, 10, 5, QtCore.Qt.AbsoluteSize)

    def addButton(self, button, hasSpacer: bool = False):
        if hasSpacer:
            self.layout().addSpacing(10)
        self.layout().addWidget(button)

    def addButtons(self, *buttons: QtWidgets.QPushButton):
        for button in buttons:
            self.layout().addWidget(button)
