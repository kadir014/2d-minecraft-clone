class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<Vector2({self.x}, {self.y})>"

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x + other.x, self.y + other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x + other, self.y + other)

        return self

    def __isub__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x - other.x, self.y - other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x - other, self.y - other)

        return self

    def __imul__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x * other.x, self.y * other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x * other, self.y * other)

        return self

    def __itruediv__(self, other):
        if isinstance(other, Vector2):
            self = Vector2(self.x / other.x, self.y / other.y)

        elif isinstance(other, (int, float)):
            self = Vector2(self.x / other, self.y / other)

        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)

        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)

        return self

    def __neg__(self):
        return self * -1

    def set(self, vector):
        self.x = vector.x
        self.y = vector.y

    def to_tuple(self):
        return (self.x, self.y)
