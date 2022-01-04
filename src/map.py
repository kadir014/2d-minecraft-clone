"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

from enum import Enum


class TileType(Enum):
    """
    Tile type enumeration
    """
    AIR = 0,
    GRASS = 1,


class Tile:
    """
    Single block (tile) in the map
    """

    def __init__(self, type_: TileType, position: tuple[int, int]):
        self.type = type_
        self.position = position
        self.light = 15

    @property
    def id(self):
        """
        Get integer ID
        """
        return self.type.value

    @property
    def name(self):
        """
        Get string name
        """
        return self.type.name


class Chunk:
    """
    An area of 16x256 tiles
    """

    def __init__(self, x: int):
        self.x = x
        self.tiles = []

    def get_tile(self, x: int, y: int) -> Tile:
        """
        Get tile at position x, y
        """
        return self.tiles[y * 16 + x]

    def set_tile(self, x: int, y: int, tile: Tile):
        """
        Set tile at given position
        """
        self.tiles[y * 16 + x] = tile


class Map:
    """
    Whole world
    """

    def __init__(self, width: int = 16*5, height: int = 256):
        self.width = width
        self.height = height

        self.chunks = []

    def get_chunk(self, x: int) -> Chunk:
        """
        Get the corresponding chunk that includes given x position
        """
        return self.chunks[x // 16]

    def set_tile(self, x: int, y: int, tile: Tile):
        """
        Set tile at given position
        """
        self.get_chunk(x).set_tile(x, y, tile)

    def set_tile_by_type(self, x: int, y: int, tiletype: TileType):
        """
        Set tile at given position by tile type
        """
        tile = Tile(tiletype, (x, y))
        self.get_chunk(x).set_tile(x, y, tile)

    def generate_chunks(self):
        self.chunks.clear()

        a = self.width // 16

        if a % 2 == 0:
            for nx in range(a // 2):
                self.chunks.append(Chunk(-(self.width//2 - ((nx+1)*16))))

            for px in range(a // 2):
                self.chunks.append(Chunk((px+1)*16))

        else:
            for nx in range(a // 2):
                self.chunks.append(Chunk(-(self.width//2 - ((nx+1)*16))))

            self.chunks.append(Chunk(0))

            for px in range(a // 2):
                self.chunks.append(Chunk((px+1)*16))

    def generate(self):
        self.generate_chunks()

        for c in self.chunks:
            print(c.x)


map = Map()

map.generate()