import time
import pygame
from player import Player
from map import Map, Tile
from random import randint
from entity import Entity
from mob import HostileMob


class Game:
    def __init__(self, core):
        self.core = core
        pygame.mouse.set_visible(False)

        self.map = Map()
        s = time.time()
        self.map.generate()
        self.map.calculate_light()
        print("Map generated in:", int((time.time()-s)*1000), "ms")

        self.draw_lights = True

        #load tile textures
        self.textures = dict()
        self.textures["void"] = pygame.Surface((16, 16))
        for t in Tile.idnames:
            if t == "air": continue
            self.textures[t] = pygame.image.load(f"assets/tiles/{t}.png")

        self.tile_width = 32
        self.tile_height = 32

        self.cursor = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
        pygame.draw.circle(self.cursor, (255, 255, 255), (self.tile_width/2, self.tile_height/2), self.tile_width/4)
        self.cursor.set_alpha(100)

        self.gravity = 10
        self.max_vertical_vel = 800

        self.player = Player(self, core)
        self.entity = HostileMob(self, core)

        self.font = pygame.font.Font("assets/fonts/Minecraftia-Regular.ttf", 16)
        self.debug_display = True

        for t in self.textures:
            self.textures[t] = pygame.transform.scale(self.textures[t], (self.tile_width, self.tile_height))

    def is_block(self, tile):
        if tile == None: return False
        elif tile.id == 0: return False
        else: return True

    def update(self):
        for e in self.core.events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.draw_lights: self.draw_lights = False
                    else: self.draw_lights = True

                if e.key == pygame.K_F3:
                    if self.debug_display: self.debug_display = False
                    else: self.debug_display = True

        self.player.update()
        self.entity.update()

        self.chunk_updates = round(((self.core.camera.x % self.core.window_width) / 1066) + 3)

    def draw(self):

        self.player.draw()
        pygame.draw.rect(self.core.window, (0, 0, 255), (self.entity.position.x-self.core.camera.x, self.entity.position.y-self.core.camera.y, self.entity.hitbox.width, self.entity.hitbox.height), 2)

        for y in range(int(self.core.window_height // self.tile_height)+2):
            for x in range(int(self.core.window_width // self.tile_width)+2):
                xx = x + int(self.core.camera.x / self.tile_width)
                yy = y + int(self.core.camera.y / self.tile_height)

                tile = self.map.get_tile(xx, yy)
                if tile == None: continue
                if tile.id == 0: continue

                if self.draw_lights:
                    if tile.light == 0:
                        self.core.window.blit(
                                    self.textures["void"],
                                    ((xx * self.tile_width) - self.core.camera.x,
                                     (yy * self.tile_height) - self.core.camera.y))

                    else:
                        self.core.window.blit(
                                    self.textures[self.map.get_tile(xx, yy).name],
                                    ((xx * self.tile_width) - self.core.camera.x,
                                     (yy * self.tile_height) - self.core.camera.y))

                        shadow = pygame.Surface((self.tile_width, self.tile_height))
                        shadow.set_alpha(255 - ((255 / 5) * tile.light))

                        self.core.window.blit(
                                    shadow,
                                    ((xx * self.tile_width) - self.core.camera.x,
                                     (yy * self.tile_height) - self.core.camera.y))
                else:
                    self.core.window.blit(
                                self.textures[self.map.get_tile(xx, yy).name],
                                ((xx * self.tile_width) - self.core.camera.x,
                                 (yy * self.tile_height) - self.core.camera.y))

                # if tile.collide:
                #     tile.collide = False
                #
                #     shadow = pygame.Surface((self.tile_width, self.tile_height))
                #     shadow.fill((255, 50, 0))
                #     shadow.set_alpha(128)
                #
                #     self.core.window.blit(
                #                 shadow,
                #                 ((xx * self.tile_width) - self.core.camera.x,
                #                  (yy * self.tile_height) - self.core.camera.y))
                #
                # elif tile.checking:
                #     tile.checking = False
                #
                #     shadow = pygame.Surface((self.tile_width, self.tile_height))
                #     shadow.fill((0, 255, 100))
                #     shadow.set_alpha(128)
                #
                #     self.core.window.blit(
                #                 shadow,
                #                 ((xx * self.tile_width) - self.core.camera.x,
                #                  (yy * self.tile_height) - self.core.camera.y))

        # for chunk in self.map.chunks:
        #     x = chunk.pos * self.tile_width - self.core.camera.x
        #     pygame.draw.line(self.core.window, (0, 255, 0), (x, 0), (x, self.core.window_height), 2)


        # pygame.draw.circle(self.core.window,
        #                    (255, 128, 0),
        #                    (self.player.position.x - self.core.camera.x + self.player.hitbox.width/2,
        #                    self.player.position.y - self.core.camera.y + self.player.hitbox.height/2),
        #                    self.player.reach_radius, 1)


        cx = round(self.core.camera.x / self.tile_width) * self.tile_width
        cy = round(self.core.camera.y / self.tile_height) * self.tile_height
        dx = self.core.camera.x - cx
        dy = self.core.camera.y - cy
        mx = round((self.core.mouse.x + dx) / self.tile_width) * self.tile_width
        my = round((self.core.mouse.y + dy) / self.tile_height) * self.tile_height
        self.mouse_tile_x = (mx - dx + cx) / self.tile_width
        self.mouse_tile_y = (my - dy + cy) / self.tile_height
        #self.core.window.blit(self.cursor, (mx-cx, my-cy))
        pygame.draw.rect(self.core.window, (210, 210, 210), (mx-dx, my-dy, self.tile_width, self.tile_height), 1)
        #pygame.draw.rect(self.core.window, (60, 60, 60), (mx-cx, my-cy, self.tile_width, self.tile_height), 1)
        self.core.window.blit(self.cursor, (self.core.mouse.x, self.core.mouse.y))

        # debug info
        if self.debug_display:
            self.core.window.blit(self.font.render(f"2D Minecraft Clone {self.core.version}{self.core.state}", True, (255, 255, 255)), (5, 5))
            self.core.window.blit(self.font.render(f"{int(self.core.clock.get_fps())} fps", True, (255, 255, 255)), (5, 25))
            self.core.window.blit(self.font.render(f"Entities: 0", True, (255, 255, 255)), (5, 45))
            self.core.window.blit(self.font.render(f"Lighting: {('Off', 'On')[self.draw_lights]}", True, (255, 255, 255)), (5, 65))
            self.core.window.blit(self.font.render(f"Chunk Updates: {self.chunk_updates}", True, (255, 255, 255)), (5, 85))
            self.core.window.blit(self.font.render(f"Position: {float(self.player.position.x/self.tile_width):.4} / {float(self.player.position.y/self.tile_height):.4}", True, (255, 255, 255)), (5, 115))
            self.core.window.blit(self.font.render(f"Velocity: {float(self.player.velocity.x):.4} / {float(self.player.velocity.y):.4}", True, (255, 255, 255)), (5, 135))
            #self.core.window.blit(self.font.render(f"", True, (255, 255, 255)), (5, 5))
