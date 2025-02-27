import pygame

from assets_loader import Asset, load_asset
from settings import BULLET_SPEED, BULLET_SIZE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            load_asset(Asset.BULLET.filename)
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, BULLET_SIZE)
        self.rect = self.image.get_rect(centerx=x, bottom=y)

    def update(self):
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
