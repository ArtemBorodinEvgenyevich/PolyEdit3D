import numpy as np
from OpenGL import GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
from PySide2.QtGui import QQuaternion, QVector2D, QVector3D, QMatrix4x4


class PlyViewportCamera:
    def __init__(self):
        self.__projectionMatrix = QMatrix4x4()
        self.__viewMatrix = QMatrix4x4()

        self.__viewZoom = 1
        self.__clipRange = (0.1, 1000.0)
        self.__fov = 45

        self.__camEye = QVector3D(0.0, 5.0, -10.0)
        self.__camTarget = QVector3D(0.0, 0.0, 0.0)
        self.__camUp = QVector3D(0.0, 1.0, 0.0)

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

    def pan(self, start: QVector2D, end:QVector2D):
        delta = end - start
        transform = QVector3D(delta.x() / 50, delta.y() / 50, 0.0)
        self.__camEye += transform
        self.__camTarget += transform

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

    def setProjection(self, w: int, h: int):
        aspect_ratio = w / h
        self.__projectionMatrix.setToIdentity()
        self.__projectionMatrix.perspective(self.__fov, aspect_ratio, *self.__clipRange)

    @property
    def projectionMatrix(self):
        return self.__projectionMatrix

    @property
    def viewMatrix(self):
        return self.__viewMatrix
