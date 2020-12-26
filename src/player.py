import pygame
from libs.vector import Vector2
from libs.aabb import AABB
from entity import Entity
from random import choice


class Player(Entity):
    def __init__(self, scene, core):
        super().__init__(scene, core)
        self.position = Vector2(1000, 6000)
        self.hitbox = AABB(Vector2(0, 0),
                           Vector2(self.scene.tile_width, 0),
                           Vector2(0, self.scene.tile_height*2),
                           Vector2(self.scene.tile_width, self.scene.tile_height*2))

        self.walking_speed = 30
        self.running_speed = 60
        self.crouching_speed = 15
        self.running = False
        self.crouching = False
        self.reach_radius = 100
        self.auto_jump = False
        self.flying = False

    def update(self):
        m = pygame.mouse.get_pressed()

        if m[0]:
            self.scene.map.set_tile(self.scene.mouse_tile_x, self.scene.mouse_tile_y, "air")
            chunk = self.scene.map.get_chunk(self.scene.mouse_tile_x)
            chunk.calculate_light()

        if m[2]:
            self.scene.map.set_tile(self.scene.mouse_tile_x, self.scene.mouse_tile_y, choice(("grass", "dirt", "bedrock", "stone")))
            chunk = self.scene.map.get_chunk(self.scene.mouse_tile_x)
            chunk.calculate_light()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if self.running: speed = self.running_speed
            elif self.crouching: speed = self.crouching_speed
            else: speed = self.walking_speed
            self.velocity.x -= speed * self.speed_factor
            self.on_wall = False

            if self.auto_jump and self.on_ground:
                tile = self.scene.map.get_tile(int((self.position.x - (self.scene.tile_width/2))//self.scene.tile_width),
                                               int((self.position.y-self.scene.tile_height/2)//self.scene.tile_height)+2)

                if self.scene.is_block(tile):
                    self.velocity.y = -self.jump_height * self.jump_factor
                    self.on_ground = False

        if keys[pygame.K_d]:
            if self.running: speed = self.running_speed
            elif self.crouching: speed = self.crouching_speed
            else: speed = self.walking_speed
            self.velocity.x += speed * self.speed_factor
            self.on_wall = False

            if self.auto_jump  and self.on_ground:
                tile = self.scene.map.get_tile(int((self.position.x+self.hitbox.width+(self.scene.tile_width/2))//self.scene.tile_width),
                                               int((self.position.y-self.scene.tile_height/2)//self.scene.tile_height)+2)

                if self.scene.is_block(tile):
                    self.velocity.y = -self.jump_height * self.jump_factor
                    self.on_ground = False

        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.on_ground:
                self.velocity.y = -self.jump_height * self.jump_factor
                self.on_ground = False

        if keys[pygame.K_LCTRL]:
            self.running = True
        else:
            self.running = False

        if keys[pygame.K_LSHIFT]:
            self.crouching = True
        else:
            self.crouching = False

        if keys[pygame.K_r]:
            self.position = Vector2(0, 0)
            self.velocity = Vector2(0, 0)

        self.on_air = True
        self.on_ground = False
        self.velocity.y += self.scene.gravity
        if self.velocity.y > self.scene.max_vertical_vel: self.velocity.y = self.scene.max_vertical_vel

        vx = (self.velocity.x * self.core.deltatime)
        vy = (self.velocity.y * self.core.deltatime)

        # moving left
        if self.velocity.x < 0:

            tile = self.scene.map.get_tile(int(self.position.x//self.scene.tile_width)-1,
                                           int(self.position.y//self.scene.tile_height)+1)

            tile2 = self.scene.map.get_tile(int(self.position.x//self.scene.tile_width)-1,
                                            int((self.position.y-0.1)//self.scene.tile_height)+2)

            if self.scene.is_block(tile):
                tbox = tile.get_aabb(self.scene.tile_width)
                tile.checking = True

                if self.position.x + vx < tbox.b.x:
                    self.velocity.x = 0
                    self.on_wall = True
                    tile.collide = True

            if self.scene.is_block(tile2):
                tbox2 = tile2.get_aabb(self.scene.tile_width)
                tile2.checking = True

                if self.position.x + vx < tbox2.b.x:
                    self.velocity.x = 0
                    self.on_wall = True
                    tile2.collide = True

        # moving right
        if self.velocity.x > 0:

            tile = self.scene.map.get_tile(int((self.position.x+self.hitbox.width)//self.scene.tile_width),
                                           int(self.position.y//self.scene.tile_height)+1)

            tile2 = self.scene.map.get_tile(int((self.position.x+self.hitbox.width)//self.scene.tile_width),
                                           int((self.position.y-0.1)//self.scene.tile_height)+2)

            if self.scene.is_block(tile):
                tbox = tile.get_aabb(self.scene.tile_width)
                tile.checking = True

                if self.position.x + vx + self.hitbox.width > tbox.a.x:
                    self.velocity.x = 0
                    self.on_wall = True
                    tile.collide = True

            if self.scene.is_block(tile2):
                tbox2 = tile2.get_aabb(self.scene.tile_width)
                tile2.checking = True

                if self.position.x + vx + self.hitbox.width > tbox2.a.x:
                    self.velocity.x = 0
                    self.on_wall = True
                    tile2.collide = True

        # moving down
        if self.velocity.y > 0:

            tile = self.scene.map.get_tile(int((self.position.x+0.9)//self.scene.tile_width),
                                           int((self.position.y + self.hitbox.height + self.scene.tile_width / 2 + 0.9)//self.scene.tile_height))

            tile2 = self.scene.map.get_tile(int((self.position.x-0.9)//self.scene.tile_width)+1,
                                           int((self.position.y + self.hitbox.height + self.scene.tile_height / 2 + 0.9)//self.scene.tile_height))

            if self.scene.is_block(tile):
                tbox = tile.get_aabb(self.scene.tile_width)
                tile.checking = True

                if self.position.y + vy + self.hitbox.height + self.scene.tile_height> tbox.a.y:
                    self.velocity.y = 0
                    self.on_ground = True
                    self.on_air = False
                    tile.collide = True

            if self.scene.is_block(tile2) and not self.on_wall:
                tbox2 = tile2.get_aabb(self.scene.tile_width)
                tile2.checking = True

                if self.position.y + vy + self.hitbox.height + self.scene.tile_height> tbox2.a.y:
                    self.velocity.y = 0
                    self.on_air = False
                    tile2.collide = True

        self.position += self.velocity * self.core.deltatime
        self.velocity.x *= 0.75
        if 0 < self.velocity.x < 0.001: self.velocity.x = 0
        if -0.001 < self.velocity.x < 0: self.velocity.x = 0

        self.hitbox.set_pos(self.position)
        self.core.camera.set(self.position + Vector2(-self.core.window_width/2 + self.hitbox.width/2, -self.core.window_height/2 + self.hitbox.height/2))

    def draw(self):
        pygame.draw.rect(self.core.window,
                         (0, 0, 255),
                         self.hitbox.get_pygame_rect(-self.core.camera),
                         2)
