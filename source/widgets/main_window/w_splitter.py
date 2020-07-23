from PySide2 import QtWidgets

# TODO: Customize
class WindowSplitter(QtWidgets.QSplitter):
    def __init__(self):
        super().__init__()
        self.setChildrenCollapsible(True)
        self.setHandleWidth(10)