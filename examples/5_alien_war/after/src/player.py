import pygame

from assets_loader import Asset, load_asset
from bullet import Bullet
from settings import (
    PLAYER_SPEED,
    WIDTH,
    HEIGHT,
    SOUND_VOLUME,
    PLAYER_SIZE,
    INITIAL_LIVES,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load(
            load_asset(Asset.PLAYER.filename)
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.lives = INITIAL_LIVES

        self.shoot_sound = pygame.mixer.Sound(load_asset(Asset.SHOOT_SOUND.filename))
        self.shoot_sound.set_volume(SOUND_VOLUME)
        self.screen = screen

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(self.screen.get_rect())

    def shoot(self, bullets, all_sprites):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)
        self.shoot_sound.play()
