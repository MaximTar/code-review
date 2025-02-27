import pygame

from alien import Alien
from assets_loader import Asset, load_asset
from player import Player
from settings import (
    BLACK,
    WHITE,
    ORANGE,
    TOTAL_ALIENS,
    FPS,
    WIDTH,
    HEIGHT,
    BACKGROUND_SPEED,
    SOUND_VOLUME,
)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self.screen)
        self.all_sprites.add(self.player)

        self.explosion_sound = pygame.mixer.Sound(
            load_asset(Asset.EXPLOSION_SOUND.filename)
        )
        self.explosion_sound.set_volume(SOUND_VOLUME)
        self.hit_sound = pygame.mixer.Sound(load_asset(Asset.HIT_SOUND.filename))
        self.hit_sound.set_volume(SOUND_VOLUME)

        pygame.mixer.music.load(load_asset(Asset.MUSIC.filename))
        pygame.mixer.music.set_volume(SOUND_VOLUME)
        pygame.mixer.music.play(-1)

        for _ in range(TOTAL_ALIENS):
            alien = Alien()
            self.all_sprites.add(alien)
            self.aliens.add(alien)

        self.score = 0

        self.background = pygame.image.load(load_asset(Asset.BACKGROUND.filename))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_y1 = 0
        self.background_y2 = -HEIGHT

    def run(self):
        while True:
            self.clock.tick(FPS)
            if not self.handle_events():
                break
            self.move_background()
            self.all_sprites.update()
            self.check_hit()
            if not self.check_collision():
                break

            pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
            self.draw()
        pygame.quit()

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                self.player.shoot(self.bullets, self.all_sprites)
        return True

    def move_background(self):
        self.background_y1 += BACKGROUND_SPEED
        self.background_y2 += BACKGROUND_SPEED
        if self.background_y1 >= HEIGHT:
            self.background_y1 = -HEIGHT
        if self.background_y2 >= HEIGHT:
            self.background_y2 = -HEIGHT

    def check_hit(self):
        hits = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)
        for _ in hits:
            self.score += 1
            self.explosion_sound.play()
            alien = Alien()
            self.all_sprites.add(alien)
            self.aliens.add(alien)

    def check_collision(self) -> bool:
        hits = pygame.sprite.spritecollide(
            self.player, self.aliens, True
        )
        if hits:
            self.player.lives -= 1
            self.hit_sound.play()
            if self.player.lives <= 0:
                self.show_game_over_screen()
                return False
        return True

    def show_game_over_screen(self) -> None:
        pygame.mixer.music.stop()
        self.screen.fill(BLACK)
        game_over_font = pygame.font.SysFont("Arial", 48)
        game_over_text = game_over_font.render("Игра окончена", True, WHITE)
        score_text = game_over_font.render(f"Ваш счет: {self.score}", True, ORANGE)
        self.screen.blit(
            game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3)
        )
        self.screen.blit(
            score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2)
        )
        pygame.display.flip()
        pygame.time.wait(3000)

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, self.background_y1))
        self.screen.blit(self.background, (0, self.background_y2))
        self.all_sprites.draw(self.screen)
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(
            f"Счет: {self.score} Жизни: {self.player.lives}", True, WHITE
        )
        self.screen.blit(text, (10, 10))
        pygame.display.flip()
