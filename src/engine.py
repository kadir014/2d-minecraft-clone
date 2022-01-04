"""

    2D Minecraft Clone in Pygame
    MIT © Kadir Aksoy
    https://github.com/kadir014/2d-minecraft-clone

    All Minecraft textures and sound effects used in this game are
    registered trademarks of Mojang Studios

"""

import os; os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import moderngl
from scenes.base import Scene
from utils import AssetLoader, source_path


# A list of commmon display resolutions up to 4K
DISPLAY_RESOLUTIONS = {
    "16:9": (
        (768, 432),
        (1024, 576),
        (1280, 720),
        (1366, 768),
        (1600, 900),
        (1920, 1080),
        (2560, 1440),
        (3840, 2160)
    ),
    "4:3": (
        (768, 576),
        (1024, 768),
        (1280, 960),
        (1366, 1024),
        (1600, 1200),
        (1920, 1440),
        (2560, 1920),
        (3840, 2880)
    ),
}


class Engine:
    """
    Core engine of the project
    """

    def __init__(self):
        self.asset_loader = AssetLoader()

        # Temporary context is used to get the multi-sampling limit
        tempcontext = moderngl.create_standalone_context()
        self.max_samples = tempcontext.max_samples
        tempcontext.release()

        pygame.init()

        self.display_info = pygame.display.Info()
        self.monitor_width = self.display_info.current_w
        self.monitor_height = self.display_info.current_h

        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, self.max_samples)

        pygame.display.set_caption("")
        self.window_width = 1066
        self.window_height = 600
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.OPENGL|pygame.DOUBLEBUF)
        pygame.display.set_icon(pygame.image.load(source_path("assets", "windowicon.png")))
        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.camera = pygame.Vector2(0, 0)

        self.context = moderngl.create_context()
        self.context.enable(moderngl.BLEND)

        self.scenes = dict()
        self._scene_name = ""
        self.events = list()
        self.running = False

        self.font = pygame.font.Font(source_path("assets", "fonts", "Minecraftia-Regular.ttf"), 16)

        # Version information
        self.version = (0, 0, 0)
        self.version_state = "indev"
        self.versionstr = ".".join((str(v) for v in self.version))
        self.pygame_version = pygame.version.ver
        self.sdl_version = ".".join((str(v) for v in pygame.get_sdl_version()))
        self.opengl_version = self.context.version_code
        self.moderngl_version = moderngl.__version__

        self.gpu_vendor = self.context.info["GL_VENDOR"]
        self.gpu_renderer = self.context.info["GL_RENDERER"]
        self.gpu_version = self.context.info["GL_VERSION"]

    def get_usable_resolutions(self) -> dict:
        """ Get usable resolutions relative to monitor resolution """

        r = {"16:9":[], "4:3":[]}

        for res in DISPLAY_RESOLUTIONS["16:9"]:
            if res[0] <= self.monitor_width and res[1] <= self.monitor_height:
                r["16:9"].append(res)

        for res in DISPLAY_RESOLUTIONS["4:3"]:
            if res[0] <= self.monitor_width and res[1] <= self.monitor_height:
                r["4:3"].append(res)

        return r

    @property
    def scene(self):
        """ Get the current scene """
        return self.scenes[self._scene_name]

    def add_scene(self, scene: Scene, name: str):
        """
        Add a scene to engine
        this function also sets the current scene as the last added one
        """
        self._scene_name = name
        self.scenes[self._scene_name] = scene

    def map_coords(self,
        x: float,
        y: float,
        width: float,
        height: float):
        """
        Map 2D window coordinates into vertex coordinates

        OpenGL's Coordinate System

         -1, 1           0, 1           1, 1
               ┌──────────────────────┐
               │                      │
         -1, 0 │         0, 0         │ 1, 0
               │                      │
               └──────────────────────┘
         -1, -1          0, -1          1, -1

        Pygame's Coordinate System

          0, 0          W/2, 0          W, 0
               ┌──────────────────────┐
               │                      │
        0, H/2 │       W/2, H/2       │ W, H/2
               │                      │
               └──────────────────────┘
          0, H          W/2, H          W, H
        """

        y = self.window_height - y

        bottomleft = (x, y - height)
        bottomright = (x + width, y - height)
        topleft = (x, y)
        topright = (x + width, y)

        bottomleft = (bottomleft[0] / (self.window_width / 2) - 1,
                      bottomleft[1] / (self.window_height / 2) - 1)

        bottomright = (bottomright[0] / (self.window_width / 2) - 1,
                       bottomright[1] / (self.window_height / 2) - 1)

        topleft = (topleft[0] / (self.window_width / 2) - 1,
                   topleft[1] / (self.window_height / 2) - 1)

        topright = (topright[0] / (self.window_width / 2) - 1,
                    topright[1] / (self.window_height / 2) - 1)

        return (*bottomleft, *bottomright, *topleft, *topright)

    def handle_events(self):
        """ Handle pygame events """
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT: self.stop()

    def stop(self):
        """ Stop the engine """
        self.running = False

    def run(self):
        """ Run the engine """
        self.running = True

        print("Starting asset loader")
        self.asset_loader.start()

        # Warmup clock
        for _ in range(10): self.clock.tick(self.max_fps)

        while self.running:
            self.deltatime = self.clock.tick(self.max_fps) / 1000
            pygame.display.set_caption(f"2D Minecraft Clone   —   Pygame "
                                       f"{self.pygame_version}  "
                                       f"SDL {self.sdl_version}  "
                                       f"OpenGL {self.opengl_version}  "
                                       f"ModernGL {self.moderngl_version}  "
                                       f"@{self.clock.get_fps():.4} FPS")
            self.handle_events()
            self.mouse = pygame.Vector2(*pygame.mouse.get_pos())

            self.context.clear(0.498, 0.627, 0.968)

            self.scene.update()
            self.scene.draw()

            pygame.display.flip()

            if len(self.asset_loader.assets_to_load) == 0 and self.asset_loader.running:
                print("Asset loader queue is empty, stopping")
                self.asset_loader.stop()

        pygame.quit()
        self.context.release()