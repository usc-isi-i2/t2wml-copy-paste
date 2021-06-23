from src.selection import Selection


class Anchor:
    def __init__(self, content, x_source, y_source, x_target, y_target):
        self.content = content
        self.x_target = x_target
        self.y_target = y_target
        self.selection = Selection(x_source, x_source, y_source, y_source)

    def get_bounds(self):
        return self.x_target, self.x_target, self.y_target, self.y_target

    def var_name(self, index):
        return f'{self.content}_{index}'
