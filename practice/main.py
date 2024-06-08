from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game:
    def __init__(self):
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Super Pirate World")

        tmx_maps = {0:load_pygame(join("data","levels","omni.tmx"))}

        self.current_stage = Level(tmx_maps[0])

    def run(self):
        while True:
            dt = pygame.time.Clock().tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()
            self.current_stage.run(dt)

if __name__ == '__main__':
    game = Game()
    game.run()