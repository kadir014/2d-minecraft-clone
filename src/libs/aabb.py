from libs.vector import Vector2
import pygame


class AABB:

    #      AABB corners:
    #
    #      A  --------  B
    #
    #      |            |
    #      |            |
    #      |            |
    #
    #      C  --------  D

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.width = abs(self.a.x - self.b.x)
        self.height = abs(self.a.y - self.c.y)

    def __repr__(self):
        return f"AABB({self.a}, {self.b}, {self.c}, {self.d})"

    def set_pos(self, vector):
        self.a = vector
        self.b = vector + Vector2(self.width, 0)
        self.c = vector + Vector2(0, self.height)
        self.d = vector + Vector2(self.width, self.height)

    def move(self, vector):
        self.set_pos(vector - self.a)

    def get_pygame_rect(self, offset=Vector2(0, 0)):
        return (float(self.a.x + offset.x), float(self.a.y + offset.y), float(self.width), float(self.height))

    def collide(self, other):
        if pygame.Rect(self.get_pygame_rect()).colliderect(pygame.Rect(other.get_pygame_rect())):
            return True
