from PySide2 import QtGui, QtWidgets, QtCore


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
        if self.isChecked():
            self.qPen.setColor(self.colorQPenNormal)
        super(PlyViewportToolButton, self).mouseReleaseEvent(event)