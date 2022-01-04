"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""


class Scene:
    """
    Base scene class
    """

    def __init__(self, engine: "Engine"):
        self.engine = engine

    def update(self):
        """
        Scene updating
        """
        pass

    def draw(self):
        """
        Scene rendering
        """
        pass