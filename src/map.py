from libs.vector import Vector2
from libs.aabb import AABB
from random import randint


class Tile:
    ids = {
        0x000 : "air",
        0x001 : "grass",
        0x002 : "dirt",
        0x003 : "stone",
        0x004 : "bedrock"
    }
    idnames = {
        "air"     : 0x000,
        "grass"   : 0x001,
        "dirt"    : 0x002,
        "stone"   : 0x003,
        "bedrock" : 0x004
    }

    def __init__(self, id, position):
        self.id = id
        self.name = Tile.ids[self.id]
        self.position = position
        self.light = 5

        self.checking = False
        self.collide = False

    def __repr__(self):
        return f"<Tile({self.name}, llight={self.light})>"

    def get_aabb(self, w):
        return AABB(self.position * w,
                    Vector2(self.position.x * w + w, self.position.y * w),
                    Vector2(self.position.x * w, self.position.y * w + w),
                    Vector2(self.position.x * w + w, self.position.y * w + w))


class Chunk:
    def __init__(self, map, pos):
        self.pos = pos

        self.map = map
        self.tiles = list()
        self.entities = list()

    def get_tile(self, x, y):
        return self.tiles[y * 16 + x]

    def calculate_light(self):
        for y in range(self.map.height):
            for x in range(16):
                tile = self.get_tile(x, y)
                if tile.id == 0: continue
                uptile = self.get_tile(x, y+1)
                if uptile == None: continue

                if uptile.id == 0:
                    tile.light = 5

                elif uptile.light == 0:
                    tile.light = 0

                else:
                    tile.light = uptile.light - 1


class Map:
    def __init__(self):
        self.width = 256 * 3
        self.height = 256

        self.tiles = []

        self.chunk_width = 16
        self.chunks = [Chunk(self, i*self.chunk_width) for i in range(self.width//self.chunk_width)]

    def clear(self):
        self.tiles.clear()
        for y in range(self.height):
            self.tiles.append(list())
            for x in range(self.width):
                self.tiles[y].append(Tile(0, Vector2(x, y)))

    def set_tile(self, x, y, name=None, id=None):
        x = round(x)
        y = round(y)
        try:
            if name:
                self.tiles[y][x].id = Tile.idnames[name]
                self.tiles[y][x].name = name
            elif id: self.tiles[y][x].id = id
        except IndexError:
            pass

    def get_tile(self, x, y):
        if y > len(self.tiles) - 1 or y < 0: return None
        if x > len(self.tiles[0]) - 1 or x < 0: return None
        return self.tiles[y][x]

    def get_chunk(self, x, tile_width=1):
        for c in self.chunks:
            if c.pos == int((x/tile_width) / 16) * 16:
                return c

    def generate(self):
        self.clear()

        for y in range(self.height):
            for x in range(self.width):

                if y <= 2:
                    self.set_tile(x, y, "bedrock")

                elif y == 3:
                    if randint(0, 1):
                        self.set_tile(x, y, "bedrock")
                    else:
                        self.set_tile(x, y, "stone")

                elif y == 4:
                    if randint(0, randint(0, randint(0, 1))):
                        self.set_tile(x, y, "bedrock")
                    else:
                        self.set_tile(x, y, "stone")

                elif y > 4 and y <= 30:
                    self.set_tile(x, y, "stone")

                elif y == 31:
                    if randint(0, 1):
                        self.set_tile(x, y, "stone")
                    else:
                        self.set_tile(x, y, "dirt")

                elif y > 31 and y <= 35:
                    self.set_tile(x, y, "dirt")

                elif y == 36:
                    if randint(0, 1):
                        self.set_tile(x, y, "grass")
                    else:
                        self.set_tile(x, y, "air")

                tile = self.get_tile(x, y)

                self.get_chunk(x).tiles.append(tile)

        self.tiles = self.tiles[::-1]

        for col in self.tiles:
            for tile in col:
                tile.position.y = len(self.tiles) - tile.position.y

    def calculate_light(self):
        for y in range(self.height):
            for x in range(self.width):

                tile = self.get_tile(x, y)
                if tile.id == 0: continue
                uptile = self.get_tile(x, y-1)
                if uptile == None: continue

                if uptile.id == 0:
                    tile.light = 5

                elif uptile.light == 0:
                    tile.light = 0

                else:
                    tile.light = uptile.light - 1
