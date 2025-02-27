import pygame

from assets_loader import ensure_assets
from game import Game
from settings import HEIGHT, WIDTH

if __name__ == "__main__":
    ensure_assets()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Война с инопланетянами")

    game = Game(screen)
    game.run()
