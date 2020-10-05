from abc import ABCMeta, abstractmethod, abstractproperty
from PySide2.QtGui import QMatrix4x4


class PlyIObj(metaclass=ABCMeta):
    @abstractmethod
    def initObject(self):
        """Should be called only in a constructor of a derived class."""
        raise NotImplementedError

    @abstractmethod
    def passUniforms(self, projection_matrix: QMatrix4x4, view_matrix: QMatrix4x4, model_matrix: QMatrix4x4):
        raise NotImplementedError

    @abstractmethod
    def setShaders(self, *paths: str):
        raise NotImplementedError

    @property
    @abstractmethod
    def modelMatrix(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def vertexArray(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def vertices(self):
        """Stored to be modified later"""
        raise NotImplementedError


class PlyIObjIndexed(PlyIObj):
    @property
    @abstractmethod
    def indexBuffer(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def indices(self):
        """Stored to be modified later"""
        raise NotImplementedError


class PlyIObjArray(PlyIObj):
    @property
    @abstractmethod
    def vertexAmount(self):
        raise NotImplementedError
