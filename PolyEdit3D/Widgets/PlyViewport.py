from PySide2 import QtWidgets, QtCore, QtGui
from OpenGL import GL as gl


class PlyViewportWidget(QtWidgets.QOpenGLWidget):
    instance_list = []

    def __init__(self):
        super().__init__()
        self.bg_color = (0.2, 0.3, 0.3, 1.0)

        self.__initUI()

        #PlyViewportWidget.instance_list.append(self)

    def __initUI(self):
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter)

    def initializeGL(self):
        pass

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(*self.bg_color)

    def resizeGL(self, w:int, h:int):
        gl.glViewport(0, 0, w, h)

    def keyPressEvent(self, event:QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            QtWidgets.QApplication.exit()
        elif event.key() == QtCore.Qt.Key_H and self.toolBox.isVisible():
            self.toolBox.hide()
        elif event.key() == QtCore.Qt.Key_H and not self.toolBox.isVisible():
            self.toolBox.setVisible(True)