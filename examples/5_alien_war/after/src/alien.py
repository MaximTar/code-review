import random

import pygame

from assets_loader import Asset, load_asset
from settings import WIDTH, HEIGHT, ALIEN_SPEED_RANGE, ALIEN_SIZE


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(load_asset(Asset.ALIEN.filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, ALIEN_SIZE)
        self.rect = self.image.get_rect(
            x=random.randint(0, WIDTH - ALIEN_SIZE[0]), y=random.randint(-100, -40)
        )
        self.speedy = random.randint(*ALIEN_SPEED_RANGE)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(*ALIEN_SPEED_RANGE)
