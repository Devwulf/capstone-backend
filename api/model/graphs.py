class TwoDPoint():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class TwoDGraph():
    def __init__(self, points) -> None:
        self.points = points

class LabeledPoint():
    def __init__(self, label, value) -> None:
        self.label = label
        self.value = value

class LabeledGraph():
    def __init__(self, points) -> None:
        self.points = points