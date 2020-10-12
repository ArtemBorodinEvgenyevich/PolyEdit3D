from PySide2.QtGui import QQuaternion, QVector2D, QVector3D, QVector4D, QMatrix4x4


class PlyViewportCamera:
    def __init__(self):
        self.__viewportSize = QVector2D()

        self.__projectionMatrix = QMatrix4x4()
        self.__viewMatrix = QMatrix4x4()

        self.__viewZoom = 1
        self.__clipRange = (0.1, 1000.0)
        self.__fov = 45

        self.__camPos = QVector3D()
        self.__camEye = QVector3D(0.0, 5.0, -10.0)
        self.__camTarget = QVector3D(0.0, 0.0, 0.0)
        self.__camUp = QVector3D(0.0, 1.0, 0.0)

        self.__mousePos = QVector2D()
        self.__isPanEnabled = False

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

    def createRayDir(self, mouse_pos: QVector2D):
        # Normalized Coordinate Space
        x = 2.0 * mouse_pos.x() / self.__viewportSize.x() - 1
        y = 2.0 * mouse_pos.y() / self.__viewportSize.y() - 1

        clip = QVector4D(x, -y, -1.0, 1.0)
        proj = QVector4D((clip * self.__projectionMatrix.inverted()[0]).toVector2D(), -1.0, 0.0)

        return (proj * self.__viewMatrix).toVector3D().normalized()

    def getRayGridIntersecton(self, mouse_pos: QVector2D):
        ray_dir = self.createRayDir(mouse_pos)

        n = QVector3D(0.0, 1.0, 0.0)
        t = -QVector3D.dotProduct(self.__camPos, n) / QVector3D.dotProduct(ray_dir, n)

        return self.__camPos + ray_dir * t

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

    def pan(self, start: QVector2D, end: QVector2D):
        delta = end - start
        transform = QVector3D(delta.x() / 100, delta.y() / 100, 0.0)
        self.__camEye += transform
        self.__camTarget += transform
        self.__mousePos = end

    def zoom(self, delta: float):
        if delta < 0 and self.__viewZoom > 0.2:
            self.__viewZoom -= 0.1
        elif delta > 0 and self.__viewZoom < 9.9:
            self.__viewZoom += 0.1

    def updateCamera(self):
        self.__viewMatrix.setToIdentity()
        self.__viewMatrix.lookAt(self.__camEye,
                                 self.__camTarget,
                                 self.__camUp)
        self.__viewMatrix.rotate(self.__viewRotation)
        self.__viewMatrix.scale(self.__viewZoom)
        self.__camPos = self.__viewMatrix.inverted()[0].column(3).toVector3D()

    def setProjection(self, w: int, h: int):
        aspect_ratio = w / h
        self.__projectionMatrix.setToIdentity()
        self.__projectionMatrix.perspective(self.__fov, aspect_ratio, *self.__clipRange)
        self.__viewportSize = QVector2D(w, h)

    @property
    def camPos(self):
        return self.__camPos

    @property
    def projectionMatrix(self):
        return self.__projectionMatrix

    @property
    def viewMatrix(self):
        return self.__viewMatrix

    @property
    def viewportSize(self):
        return self.__viewportSize

    @property
    def mousePos(self):
        return self.__mousePos

    @mousePos.setter
    def mousePos(self, coords: QVector2D):
        self.__mousePos = coords

    @property
    def isPanEnabled(self):
        return self.__isPanEnabled

    @isPanEnabled.setter
    def isPanEnabled(self, is_enabled: bool):
        self.__isPanEnabled = is_enabled
