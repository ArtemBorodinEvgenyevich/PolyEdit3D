from source.graphics.object_entity import ObjectEntity


class ObjPlain(ObjectEntity):
    def __init__(self):
        super().__init__()

        self.vertices = [ 0.5,  0.5, 0.0,   # top right
                          0.5, -0.5, 0.0,   # bottom right
                          0.0,  0.5, 0.0]   # top left

        self.indices = [0, 1, 3,
                        1, 2, 3]
