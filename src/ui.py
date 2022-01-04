"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

from typing import Union
from utils import source_path
from render import Drawable
import pygame


class UIBase(Drawable):
    """
    Base UI class
    """

    def __init__(self,
            engine: "Engine",
            position: Union[tuple[float, float], pygame.Vector2],
            size: tuple[float, float]):

        super().__init__(engine, position, size, "ui")


FONTS = {}
def get_font(fontname: str, font_size: int, sys: bool = False) -> pygame.font.Font:
    if fontname in FONTS:
        return FONTS[fontname]

    else:
        if sys:
            font = pygame.font.SysFont(fontname, font_size)
        else:
            font = pygame.font.Font(fontname, font_size)

        FONTS[fontname] = font

        return font



class Text(UIBase):
    """
    Multi-line text UI
    """

    def __init__(self,
            engine: "Engine",
            position: Union[tuple[float, float], pygame.Vector2],
            text: str,
            font: str = "Arial",
            font_size: int = 20,
            antialias: bool = True,
            color: tuple[int, int, int] = (0, 0, 0)):
        
        self.text = text
        self.font = font
        self.font_size = font_size
        self.antialias = antialias
        self.color = color

        self.surface = self._render_text()

        super().__init__(engine, position, self.surface.get_size())

        self.build_texture()

    def _render_text(self) -> pygame.Surface:
        surf = get_font(self.font, self.font_size, sys=True).render(
            self.text,
            self.antialias,
            self.color
        )

        return surf