from enum import Enum, unique

@unique
class PlyEditEnum(Enum):
    IDLE = 0
    DRAW_PLANE = 1
    DRAW_CUBE = 2
