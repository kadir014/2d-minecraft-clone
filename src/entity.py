from libs.vector import Vector2
from libs.aabb import AABB


class Entity:
    def __init__(self, scene, core):
        self.scene = scene
        self.core = core
        self.id = "entity"

        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.hitbox = AABB(Vector2(0, 0),
                           Vector2(self.scene.tile_width, 0),
                           Vector2(0, self.scene.tile_height),
                           Vector2(self.scene.tile_width, self.scene.tile_height))

        self.speed = 50
        self.jump_height = 215

        self.on_ground = False
        self.on_air = True
        self.on_wall = False

        # potion effects
        self.speed_factor = 1
        self.jump_factor = 1

    def apply_physics(self):
        self.on_air = True
        self.on_ground = False
        self.velocity.y += self.scene.gravity
        if self.velocity.y > self.scene.max_vertical_vel: self.velocity.y = self.scene.max_vertical_vel

        vx = (self.velocity.x * self.core.deltatime)
        vy = (self.velocity.y * self.core.deltatime)

        # moving left
        if self.velocity.x < 0:

            tile = self.scene.map.get_tile(int(self.position.x//self.scene.tile_width)-1,
                                           int((self.position.y+self.scene.tile_height/2)//self.scene.tile_height))

            if self.scene.is_block(tile):
                tbox = tile.get_aabb(self.scene.tile_width)
                tile.checking = True

                if self.position.x + vx < tbox.b.x:
                    self.velocity.x = 0
                    self.on_wall = True
                    tile.collide = True

        # moving right
        if self.velocity.x > 0:

            tile = self.scene.map.get_tile(int((self.position.x+self.hitbox.width)//self.scene.tile_width),
                                           int((self.position.y+self.scene.tile_height/2)//self.scene.tile_height))

            if self.scene.is_block(tile):
                tbox = tile.get_aabb(self.scene.tile_width)
                tile.checking = True

                if self.position.x + vx + self.hitbox.width + 0.9 > tbox.a.x:
                    self.velocity.x = 0
                    self.on_wall = True
                    tile.collide = True

        # moving down
        if self.velocity.y > 0:

            tile = self.scene.map.get_tile(int((self.position.x + 0.9)//self.scene.tile_width),
                                           int((self.position.y + 0.9)//self.scene.tile_height)+1)

            tile2 = self.scene.map.get_tile(int((self.position.x - 0.9)//self.scene.tile_width)+1,
                                           int((self.position.y + 0.9)//self.scene.tile_height)+1)

            if self.scene.is_block(tile):
                tbox = tile.get_aabb(self.scene.tile_width)
                tile.checking = True

                if self.hitbox.c.y + vy + self.scene.tile_width > tbox.a.y:
                    self.velocity.y = 0
                    self.on_ground = True
                    self.on_air = False
                    tile.collide = True

            if self.scene.is_block(tile2) and not self.on_wall:
                tbox2 = tile2.get_aabb(self.scene.tile_width)
                tile2.checking = True

                if self.hitbox.c.y + vy + self.scene.tile_width > tbox2.a.y:
                    self.velocity.y = 0
                    self.on_air = False
                    tile2.collide = True

        self.position += self.velocity * self.core.deltatime
        self.velocity.x *= 0.75
        if 0 < self.velocity.x < 0.001: self.velocity.x = 0
        if -0.001 < self.velocity.x < 0: self.velocity.x = 0

        self.hitbox.set_pos(self.position)

    def update(self):
        self.apply_physics()

    def draw(self):
        pass
