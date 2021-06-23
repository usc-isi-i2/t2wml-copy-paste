X1 = 'x1'
X2 = 'x2'
Y1 = 'y1'
Y2 = 'y2'


class Selection:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    @staticmethod
    def from_dict(selection_dict):
        return Selection(selection_dict[X1], selection_dict[X2], selection_dict[Y1], selection_dict[Y2])

    def contains(self, x, y):
        return (self.x1 <= x <= self.x2) and (self.y1 <= y <= self.y2)
