from PySide2.QtGui import QQuaternion, QVector2D, QVector3D, QMatrix4x4


class PlyViewportCamera:
    def __init__(self):
        self.__projectionMatrix = QMatrix4x4()
        self.__viewMatrix = QMatrix4x4()

        self.__viewZoom = -10.0
        self.__clipRange = (0.1, 1000.0)
        self.__fov = 45

        self.__viewRotation = QQuaternion()
        self.__xRotation = QQuaternion()
        self.__yRotation = QQuaternion()

    def __rotateX(self, rotation: QQuaternion):
        self.__xRotation = rotation * self.__xRotation
        self.__viewRotation = self.__xRotation * self.__yRotation
        self.__viewRotation.normalize()

    def __rotateY(self, rotation: QQuaternion):
        self.__yRotation = rotation * self.__yRotation
        self.__viewRotation = self.__xRotation * self.__yRotation
        self.__viewRotation.normalize()

    def rotate(self, p_start: QVector2D, p_end: QVector2D):
        prev_rotation = self.__viewRotation
        div_factor = 10
        diff = p_end - p_start
        angle_x = diff.y() / div_factor
        angle_y = diff.x() / div_factor
        self.__rotateX(QQuaternion.fromAxisAndAngle(1.0, 0.0, 0.0, angle_x))
        self.__rotateY(QQuaternion.fromAxisAndAngle(0.0, 1.0, 0.0, angle_y))
        self.__viewRotation = QQuaternion.slerp(prev_rotation, self.__viewRotation, 0.6)
        self.__viewRotation.normalize()

    def zoom(self, delta: float):
        if delta > 0 and self.__viewZoom != -1.0:
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
