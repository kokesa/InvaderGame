import math

class Vector2D(object):
    
    @staticmethod
    def from_points(p1, p2):
        return Vector2D(p2[0] - p1[0], p2[1] - p1[1])
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __get__(self, instance, owner):
        return (self.x, self.y)
    
    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)
    
    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y + rhs.y)
    
    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y - rhs.y)
    
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __div__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def get_magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def inner_product(self, vector):
        return self.x * vector.x + self.y * vector.y
    
    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude

def get_angle_from_vector(vector):
    inner_product = vector.inner_product(Vector2D(1, 0))
    magnitude = vector.get_magnitude()
    return math.acos(inner_product / magnitude)

def rotate_vector(vector, angle):
    if isinstance(angle, Vector2D):
        angle = get_angle_from_vector(angle)
    x = vector.x * math.cos(angle) - vector.y * math.sin(angle)
    y = vector.x * math.sin(angle) + vector.y * math.cos(angle)
    return Vector2D(x, y)
