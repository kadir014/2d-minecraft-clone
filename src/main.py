import pygame
from libs.vector import Vector2


class Core:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.display_info = pygame.display.Info()
        self.monitor_width = self.display_info.current_w
        self.monitor_height = self.display_info.current_h

        pygame.display.set_caption("")
        self.window_width = 1066
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_icon(pygame.image.load("assets/windowicon.png"))
        self.clock = pygame.time.Clock()
        self.max_fps = 60

        # misc
        self.camera = Vector2(0, 0)
        self.scenes = dict()
        self.current_scene = "Game"
        self.events = list()
        self.running = False

        # version info
        self.version = "0.0.1"
        self.state = "indev"
        self.version_tuple = (0, 0, 0)
        self.pyg_ver = pygame.version.ver
        sdl_ver = pygame.get_sdl_version()
        self.sdl_ver = f"{sdl_ver[0]}.{sdl_ver[1]}.{sdl_ver[2]}"

    def get_current_scene(self):
        return self.scenes[self.current_scene]

    def handle_events(self):
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT: self.running = False

    def run(self):
        self.running = True

        #warmup clock
        for i in range(10): self.clock.tick(self.max_fps)

        while self.running:
            self.deltatime = self.clock.tick(self.max_fps) / 1000
            pygame.display.set_caption(f"2D Minecraft Clone   |   Pygame {self.pyg_ver}  SDL {self.sdl_ver}  FPS {self.clock.get_fps():.4}")
            self.handle_events()
            self.mouse = Vector2(*pygame.mouse.get_pos())

            self.window.fill((127, 160, 247))

            self.get_current_scene().update()
            self.get_current_scene().draw()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    core = Core()
    from scenes.game import Game
    core.scenes["Game"] = Game(core)
    core.run()
