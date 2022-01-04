"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

from threading import Thread
from pathlib import Path
import pygame


# TODO
def pyinstaller_path():
    pass

# TODO
def cxfreeze_path():
    pass

# TODO
def source_path(*children) -> Path:
    """
    Get resolved path of a source file (code, asset, etc..) regardless of
    OS and used freezer (pyinstaller & cxfreeze)
    """
    return Path(*children).resolve()


class AssetLoader(Thread):
    """
    Threaded asset loader class

    Loads assets from disk in a seperate thread, gets stopped by the engine
    when everything is loaded
    """
    def __init__(self):
        super().__init__()

        self.assets_to_load = {}
        self.loaded_assets = {}
        self.hook_callbacks = []
        self.running = False

    def __getitem__(self, name):
        """ Get a loaded asset """
        return self.loaded_assets[name]

    def add_asset(self, name, path):
        """ Add an asset to the loading queue """
        self.assets_to_load[name] = path

    def hook(self, func):
        """
        Hook a callback function which will be called when certain
        events happen
        """
        self.hook_callbacks.append(func)

    def stop(self):
        """
        Stop the asset loader

        Any unloaded assets won't get loaded thus this method shouldn't
        be called manually
        """
        self.running = False

    def start(self):
        """ Start the asset loader """
        self.running = True
        super().start()

    def run(self):
        while self.running:
            if len(self.assets_to_load) > 0:
                for asset in self.assets_to_load:
                    path = self.assets_to_load[asset]

                    if path.endswith(".png"):
                        img = pygame.image.load(path)
                        self.loaded_assets[asset] = img
                        for hook in self.hook_callbacks:
                            hook(asset)

                self.assets_to_load.clear()