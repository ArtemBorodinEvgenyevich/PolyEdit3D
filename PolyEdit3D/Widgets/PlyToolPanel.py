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

        # TODO: Temporary buttons
        btn1 = PlyViewportToolButton()
        btn2 = PlyViewportToolButton()
        btn3 = PlyViewportToolButton()
        btn4 = PlyViewportToolButton()
        btn5 = PlyViewportToolButton()

        self.addButtons(btn1, btn2, btn4, btn5)
        self.addButton(btn3, hasSpacer=True)

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


class PlyViewportToolButton(QtWidgets.QPushButton):
    """`PlyViewportToolPanel`'s button."""
    def __init__(self, icon_path: str = None, parent=None):
        super(PlyViewportToolButton, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_Hover)
        self.installEventFilter(self)
        self.setFixedSize(55, 55)

        self.colorNormal = QtGui.QColor(166, 166, 166)
        self.colorHover = QtGui.QColor(179, 179, 179)
        self.colorQPenNormal = QtGui.QColor(140, 140, 140)
        self.colorQPenClicked = [QtGui.QColor(153, 214, 255), QtGui.QColor(0, 0, 204)]

        self.qBrush = QtGui.QBrush(self.colorNormal)
        self.qPen = QtGui.QPen(self.colorQPenNormal, 3)

        self.ico = icon_path

    def setPenGradient(self, colors: list):
        gradient = QtGui.QRadialGradient(self.rect().center(), self.width() * 2.5)
        gradient.setColorAt(0, colors[0])
        stop_point = 1 / len(colors)

        for i in colors[1:]:
            gradient.setColorAt(stop_point, i)
            stop_point += stop_point

        return QtGui.QBrush(gradient)

    def setIcon(self, icon_path: str):
        """`QPushButton::setIcon` function re-define.
        Set path to button's icon, then redraws the button.
        """
        self.ico = icon_path
        self.update()

    def paintEvent(self, event:QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        widget_rect = self.rect().adjusted(2, 2, -2, -2)
        painter.setPen(self.qPen)
        painter.setBrush(self.qBrush)
        painter.drawRoundedRect(widget_rect, 10., 10., QtCore.Qt.RelativeSize)

        if self.ico is not None:
            self.ico = QtGui.QPixmap(self.ico)
            self.ico_rect = self.ico.rect()
            self.ico_rect.setSize(widget_rect.size())
            painter.drawPixmap(widget_rect, self.ico)

    def eventFilter(self, watched:QtCore.QObject, event:QtCore.QEvent) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            self.qBrush.setColor(self.colorHover)
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.qBrush.setColor(self.colorNormal)

        return super(PlyViewportToolButton, self).eventFilter(watched, event)

    def mousePressEvent(self, event:QtGui.QMouseEvent):
        self.qPen.setBrush(self.setPenGradient(self.colorQPenClicked))
        super(PlyViewportToolButton, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event:QtGui.QMouseEvent):
        if not self.isChecked():
            self.qPen.setColor(self.colorQPenNormal)
        super(PlyViewportToolButton, self).mouseReleaseEvent(event)


class PlyBtnSetWireView(PlyViewportToolButton):
    """Tool button for polygon mode change."""
    geoModeStateChanged = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(PlyBtnSetWireView, self).__init__(parent)
        self.setCheckable(True)
        self.setIcon(QtGui.QPixmap(AppPaths.BTN_WIREFRAME_ICON.value))

        self.clicked.connect(self.geoModeStateChanged)
        self.clicked.connect(self.setWireframe)

    def setWireframe(self):
        """Boolean to pass to `PlyViewportWidget` on button click."""
        if not self.isChecked():
            return False
        return True