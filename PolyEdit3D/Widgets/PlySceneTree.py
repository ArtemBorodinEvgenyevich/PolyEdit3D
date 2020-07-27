from PySide2 import QtWidgets, QtCore, QtGui


class PlySceneTreeWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(PlySceneTreeWidget, self).__init__()
        self.addItem("Item 1")
        self.addItem("Item 2")
        self.addItem("Item 3")
        self.addItem("Item 4")
        self.addItem("Item 5")