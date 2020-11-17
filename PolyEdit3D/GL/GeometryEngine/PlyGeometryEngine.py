from PySide2.QtGui import QVector2D, QVector3D, QMatrix4x4
from PolyEdit3D.GL.Elements.PlyIMesh import PlyIObjIndexed


class GeometryEngine:
    def __init__(self, parent=None):
        self.__parent = parent
        self.__currentObject = None
        self.__startPoint = QVector2D()
        self.__movePoint = QVector3D()

    def setObject(self, obj: PlyIObjIndexed):
        self.__currentObject = obj

    def releaseObject(self):
        self.__currentObject = None

    def setScaleByVector(self, scale_vector: QVector3D):
        self.__currentObject.scaleVector = scale_vector

    def setScaleByScalar(self, scalar: float):
        self.__currentObject.scaleVector = QVector3D(scalar, scalar, scalar)

    def setTranslationByVector(self, translate_vector: QVector3D):
        self.__currentObject.translateVector = translate_vector

    def translateByVector(self, translate_vector: QVector3D):
        self.__currentObject.translateVector += translate_vector

    def planeFromVector(self, dir_vector: QVector2D):
        if self.__currentObject is not None:
            diff = dir_vector - self.__startPoint
            self.setScaleByVector(QVector3D(diff.x(), 0.0, diff.z()))
            self.translateByVector((dir_vector - self.__movePoint) / 2.0)
            self.__movePoint = dir_vector

    @property
    def currentObject(self):
        return self.__currentObject

    @property
    def startPoint(self):
        return self.__startPoint

    @startPoint.setter
    def startPoint(self, vector: QVector2D):
        self.__startPoint = vector

    @property
    def movePoint(self):
        return self.__movePoint

    @movePoint.setter
    def movePoint(self, vector: QVector3D):
        self.__movePoint = vector
