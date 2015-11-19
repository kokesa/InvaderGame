import Vector2D
from Vector2D import Vector2D

class PatternMovement(object):
    pattern = []
    def __init__(self, init_x, init_y, surface, pattern_movement_type):
        self.init_x = init_x
        self.init_y = init_y
        self.init_pos = Vector2D(init_x, init_y)
        self.set_pattern_movement(surface, pattern_movement_type)
            
    def set_pattern_movement(self, surface, type):
        if type == "right_to_left":
            self.set_right_to_left_pattern(surface)
        elif type == "rect":
            pass
        self.pattern_movement_id = 0
        self.pattern_length = len(self.pattern)
            
    def set_right_to_left_pattern(self, surface):
        pattern = self.pattern
        surface_width = surface.get_width()
        if self.init_x <= surface_width / 2:
            pattern.append({"right":140})
            pattern.append({"wait":50})
            pattern.append({"left":140})
            pattern.append({"wait":50})
        else:
            pattern.append({"left":280})
            pattern.append({"wait":50})
            pattern.append({"right":280})
            pattern.append({"wait":50})
        self.pattern_length = len(self.pattern)
   
    def set_rect_movement_pattern(self, surface, width, height):
        pattern = self.pattern
        pattern.clear()
        pattern.append({"right":+width})
        pattern.append({"wait":50})
        pattern.append({"down":+height})
        pattern.append({"wait":50})
        pattern.append({"left":-width})
        pattern.append({"wait":50})
        pattern.append({"up":-height})
        pattern.append({"wait":50})
        