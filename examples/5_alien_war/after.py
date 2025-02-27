import os
from enum import Enum

import pygame
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# константы перетащили в одно место
WIDTH, HEIGHT = 1200, 800
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = -15
ALIEN_SPEED_RANGE = (2, 4)
TOTAL_ALIENS = 30
ASSETS_DIR = "assets"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)


# ассеты (файлы и урлы) вынесли и поменяли на словарь
# потом стало ясно, что лучше их поменять на енум
class Asset(Enum):
    BACKGROUND = ("background.jpg", "https://drive.usercontent.google.com/u/0/uc?id=1YeQGIUjfLgv1H5w2Zh5sEInAI8dO1g_s&export=download")
    ALIEN = ("alien.png", "https://drive.usercontent.google.com/u/0/uc?id=1V2hlAR1hI0gpBC64qsoyol4Q4ejaTCI4&export=download")
    PLAYER = ("player.png", "https://drive.usercontent.google.com/u/0/uc?id=1fdGfMGHCZ0Pi8jxFCLCQw_Fic_enUISS&export=download")
    BULLET = ("bullet.png", "https://drive.usercontent.google.com/u/0/uc?id=1YYcBOUPqerpeZ2TxZG4otqr8gBGRgrKc&export=download")
    SHOOT_SOUND = ("shoot.wav", "https://drive.usercontent.google.com/u/0/uc?id=1detZdbBHrkDLdDdrVm5JzGlC4C8rJKUa&export=download")
    HIT_SOUND = ("hit.wav", "https://drive.usercontent.google.com/u/0/uc?id=1NxFduvac5PSGSM2mj4d4Q2o5Sijkm34_&export=download")
    EXPLOSION_SOUND = ("explosion.wav", "https://drive.usercontent.google.com/u/0/uc?id=1VKCV2xWT32-glKj0WT8FQ38otniSsjab&export=download")
    MUSIC = ("background.wav", "https://drive.usercontent.google.com/u/0/uc?id=1sKO-Xs7nIkTSr-3npNueRjyMD2b_QTQ0&export=download")

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url


# поправили скачивание - теперь скачиваются только недостающие файлы, а не все
# и скачиваются в отдельную папку с ассетами, а не захламляют каталог с кодом
def ensure_assets():
    os.makedirs(ASSETS_DIR, exist_ok=True)

    def download_file(asset: Asset):
        path = os.path.join(ASSETS_DIR, asset.filename)
        if not os.path.exists(path):
            print(f"Downloading {asset.filename}...")
            urllib.request.urlretrieve(asset.url, path)

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_file, Asset)


ensure_assets()


def load_asset(filename):
    return os.path.join(ASSETS_DIR, filename)


# инициализацию почти не меняли
pygame.init()

background = pygame.image.load(load_asset(Asset.BACKGROUND.filename))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_y1, background_y2 = 0, -HEIGHT

shoot_sound = pygame.mixer.Sound(load_asset(Asset.SHOOT_SOUND.filename))
explosion_sound = pygame.mixer.Sound(load_asset(Asset.EXPLOSION_SOUND.filename))
hit_sound = pygame.mixer.Sound(load_asset(Asset.HIT_SOUND.filename))
pygame.mixer.music.load(load_asset(Asset.MUSIC.filename))
pygame.mixer.music.play(-1)

# переместили в блок инициализации
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Война с инопланетянами")

all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

clock = pygame.time.Clock()


# в классах изменения незначительные
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(load_asset(Asset.PLAYER.filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.lives = 3
        # убрали лишний атрибут speedx

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(load_asset(Asset.ALIEN.filename)).convert_alpha()
        # по-хорошему, все эти магические числа нужно выносить в конфиг
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(x=random.randint(0, WIDTH - 60), y=random.randint(-100, -40))
        self.speedy = random.randint(*ALIEN_SPEED_RANGE)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - 60)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(*ALIEN_SPEED_RANGE)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(load_asset(Asset.BULLET.filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect(centerx=x, bottom=y)

    def update(self):
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


def game_loop():
    global background_y1, background_y2

    def show_game_over_screen() -> None:
        pygame.mixer.music.stop()
        screen.fill(BLACK)
        game_over_font = pygame.font.SysFont("Arial", 48)
        game_over_text = game_over_font.render("Игра окончена", True, WHITE)
        score_text = game_over_font.render(f"Ваш счет: {score}", True, ORANGE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    def event_handling() -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # объединили условия
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                player.shoot()
        return True

    def update_background() -> None:
        global background_y1, background_y2
        # background_speed = 2 - тоже в настройки
        background_y1 += 2
        background_y2 += 2
        if background_y1 >= HEIGHT:
            background_y1 = -HEIGHT
        if background_y2 >= HEIGHT:
            background_y2 = -HEIGHT

    def check_hit(score: int) -> int:
        hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for _ in hits:
            score += 1
            explosion_sound.play()
            alien = Alien()
            all_sprites.add(alien)
            aliens.add(alien)
        return score

    def check_collision() -> bool:
        hits = pygame.sprite.spritecollide(player, aliens, True)  # Проверка столкновений мобов с игроком
        if hits:
            player.lives -= 1
            hit_sound.play()
            if player.lives <= 0:
                show_game_over_screen()
                return False
        return True

    player = Player()
    all_sprites.add(player)

    for _ in range(TOTAL_ALIENS):
        alien = Alien()
        all_sprites.add(alien)
        aliens.add(alien)

    score = 0

    while True:
        clock.tick(FPS)

        if not event_handling():
            break

        update_background()
        all_sprites.update()
        score = check_hit(score)

        if not check_collision():
            break

        screen.fill(BLACK)

        screen.blit(background, (0, background_y1))
        screen.blit(background, (0, background_y2))
        all_sprites.draw(screen)

        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Счет: {score} Жизни: {player.lives}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    game_loop()
