"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

from . import base
from ui import Text


class Scene(base.Scene):
    """
    Game scene
    """

    def __init__(self, engine: "Engine"):
        super().__init__(engine)

        self.display_debug = True

        self.text = Text(self.engine, (5, 5), "text ui looool hello")

    def draw(self):
        if self.display_debug:

            self.text.render()

            self.engine.window.blit(
                self.engine.font.render(
                    f"In-development version {self.engine.version}",
                    True,
                    (255, 255, 255)),
                (5, 2))

            self.engine.window.blit(
                self.engine.font.render(
                    f"{int(self.engine.clock.get_fps())} fps (max: {self.engine.max_fps})",
                    True,
                    (255, 255, 255)),
                (5, 22))

            self.engine.window.blit(
                self.engine.font.render(
                    f"Entities: 0/100",
                    False,
                    (255, 255, 255)),
                (5, 42))

            self.engine.window.blit(
                self.engine.font.render(
                    f"Particles: 0/100",
                    False,
                    (255, 255, 255)),
                (5, 62))

            self.engine.window.blit(
                self.engine.font.render(
                    f"XY: 0.00 / 0.00",
                    False,
                    (255, 255, 255)),
                (5, 102))

            self.engine.window.blit(
                self.engine.font.render(
                    f"Block: 0 0",
                    False,
                    (255, 255, 255)),
                (5, 122))

            self.engine.window.blit(
                self.engine.font.render(
                    f"Chunk: 0 0 in 0 0",
                    False,
                    (255, 255, 255)),
                (5, 142))

            self.engine.window.blit(
                self.engine.font.render(
                    f"Light: 0",
                    False,
                    (255, 255, 255)),
                (5, 162))