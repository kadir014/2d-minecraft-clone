"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

from engine import Engine
import scenes


if __name__ == "__main__":
    engine = Engine()

    engine.add_scene(scenes.game.Scene(engine), "Game")

    engine.run()