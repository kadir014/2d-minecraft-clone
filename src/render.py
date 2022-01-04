"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

from typing import Union
from utils import source_path
import struct
import moderngl
import pygame


PROGRAMS = {}
def _compile_programs(context: moderngl.Context, force: bool = False):
    """
    This function caches shader programs for future use.
    force keyword recompiles all shaders
    """
    if len(PROGRAMS) == 0 or force:
        PROGRAMS.clear()

        PROGRAMS["tile"] = context.program(
            vertex_shader = open(source_path("shaders", "tile.vsh")).read(),
            fragment_shader = open(source_path("shaders", "tile.fsh")).read()
        )

        PROGRAMS["ui"] = context.program(
            vertex_shader = open(source_path("shaders", "ui.vsh")).read(),
            fragment_shader = open(source_path("shaders", "ui.fsh")).read()
        )


class Drawable:
    """
    A quad base class for all things drawable on display
    """

    def __init__(self,
            engine: "Engine",
            position: Union[tuple[float, float], pygame.Vector2],
            size: tuple[float, float],
            shaderprogram: str):
        
        self.engine = engine
        self.context = self.engine.context
        self.position = pygame.Vector2(position)
        self.size = size

        _compile_programs(self.context)
        self.program = PROGRAMS[shaderprogram]
        
        self.vertices = self.engine.map_coords(
            self.position.x,
            self.position.y,
            *self.size
        )

        self.uvmap = [0, 1,  1, 1,
                      0, 0,  1, 0]

        self.indices = [0, 1, 2,
                        1, 2, 3]

        self.vbo, self.uvbo, self.ibo = b"", b"", b""
        self.update_buffers()

        self.vao = self.engine.context.vertex_array(
            self.program,
            [
                (self.vbo, "2f", "inpos"),
                (self.uvbo, "2f", "inUV")
            ],
            self.ibo
        )

        self.texture = None

    def update_buffers(self):
        """ Update VBO, UVBO and IBO """
        self.vbo = self.context.buffer(struct.pack("8f", *self.vertices))
        self.uvbo = self.context.buffer(struct.pack("8f", *self.uvmap))
        self.ibo = self.context.buffer(struct.pack("6I", *self.indices))

    def change_program(self, shaderprogram: str):
        """ Change current vertex array object's shader program """
        self.program = PROGRAMS[shaderprogram]

        self.vao = self.engine.context.vertex_array(
            self.program,
            [
                (self.vbo, "2f", "inpos"),
                (self.uvbo, "2f", "inUV")
            ],
            self.ibo
        )

    def build_texture(self):
        """ Build texture from Pygame surface """  
        self.texture = self.context.texture(
            self.surface.get_size(),
            4,
            pygame.image.tostring(self.surface, "RGBA")
        )

    def render(self):
        """ Bind the texture (if there is one) and render VAO """
        if self.texture is not None:
            self.texture.use()

        self.vao.render()

    

