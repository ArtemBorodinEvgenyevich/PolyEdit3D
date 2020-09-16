from PySide2.QtGui import QQuaternion, QVector2D, QVector3D, QMatrix4x4


class PlyViewportCamera:
    def __init__(self):

        self.__projectionMatrix = QMatrix4x4()
        self.__viewMatrix = QMatrix4x4()
        self.__viewRotation = QQuaternion()

        self.__viewZoom = -10.0
        self.__clipRange = (0.1, 1000.0)
        self.__fov = 45

    def rotate(self, p_start: QVector2D, p_end: QVector2D):
        diff = p_end - p_start
        angle = diff.length() / 20
        axis = QVector3D(diff.y(), diff.x(), 0.0)
        self.__viewRotation = QQuaternion.fromAxisAndAngle(axis, angle) * self.__viewRotation

    def zoom(self, delta: float):
        if delta > 0:
            self.__viewZoom += 0.5
        elif delta < 0:
            self.__viewZoom -= 0.5

    def updateCamera(self):
        self.__viewMatrix.setToIdentity()
        self.__viewMatrix.translate(0.0, 0.0, self.__viewZoom)
        self.__viewMatrix.rotate(15, QVector3D(1.0, 0.0, 0.0))
        self.__viewMatrix.rotate(self.__viewRotation)

    def setProjection(self, w: int = 1280, h: int = 720):
        aspect_ratio = w / h
        self.__projectionMatrix.setToIdentity()
        self.__projectionMatrix.perspective(self.__fov, aspect_ratio, *self.__clipRange)

    @property
    def projectionMatrix(self):
        return self.__projectionMatrix

    @property
    def viewMatrix(self):
        return self.__viewMatrix
