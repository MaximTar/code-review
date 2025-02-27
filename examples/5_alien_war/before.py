#!!!!!!!!!!!!!!!!!звук может быть громкий!!!!!!!!!!!!!!!!!!!!!!
import os
import pygame
import random
import urllib.request
from concurrent.futures import ThreadPoolExecutor

files = [
    ("https://drive.usercontent.google.com/u/0/uc?id=1YeQGIUjfLgv1H5w2Zh5sEInAI8dO1g_s&export=download",
     "background.jpg"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1V2hlAR1hI0gpBC64qsoyol4Q4ejaTCI4&export=download", "alien.png"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1fdGfMGHCZ0Pi8jxFCLCQw_Fic_enUISS&export=download", "player.png"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1YYcBOUPqerpeZ2TxZG4otqr8gBGRgrKc&export=download", "bullet.png"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1detZdbBHrkDLdDdrVm5JzGlC4C8rJKUa&export=download", "shoot.wav"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1NxFduvac5PSGSM2mj4d4Q2o5Sijkm34_&export=download", "hit.wav"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1VKCV2xWT32-glKj0WT8FQ38otniSsjab&export=download",
     "explosion.wav"),
    ("https://drive.usercontent.google.com/u/0/uc?id=1sKO-Xs7nIkTSr-3npNueRjyMD2b_QTQ0&export=download",
     "background.wav"),
]

def check_files():
    for file in files:
        if not file[1] in os.listdir():
            return False
    return True

def download_file(url, filename):
    try:
        print(f"Начинаю загрузку: {filename}")
        urllib.request.urlretrieve(url, filename)
        print(f"Загрузка завершена: {filename}")
    except Exception as e:
        print(f"Ошибка при загрузке {filename}: {e}")
        exit()

if not check_files():
    with ThreadPoolExecutor(max_workers=4) as executor:
        [executor.submit(download_file, url, filename) for url, filename in files]

pygame.init()
WIDTH, HEIGHT = 1200, 800
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабирование под размер экрана
background_y1 = 0
background_y2 = -HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = -15
MOB_SPEED_RANGE = (2, 4)
TOTAL_MOBS = 30

shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)  # Фоновая музыка

class Player(pygame.sprite.Sprite):  #Класс игрока
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.lives = 3

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speedx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speedx = PLAYER_SPEED
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Alien(pygame.sprite.Sprite):  #Класс пришельцев
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("alien.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speedy = random.randint(*MOB_SPEED_RANGE)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(*MOB_SPEED_RANGE)

# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Война с инопланетянами")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mobs = pygame.sprite.Group()

for _ in range(TOTAL_MOBS):
    mob = Alien()
    all_sprites.add(mob)
    mobs.add(mob)

bullets = pygame.sprite.Group()

score = 0
running = True

def show_game_over_screen():  #Экран смерти
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    font = pygame.font.SysFont("Arial", 48)
    text = font.render("Игра окончена", True, WHITE)
    score_text = font.render(f"Ваш счет: {score}", True, ORANGE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)

def update_background():
    global background_y1, background_y2
    background_speed = 2  #Скорость движения фона
    #Перемещение фона вниз
    background_y1 += background_speed
    background_y2 += background_speed

    #Если изображение уходит за пределы экрана, переместить наверх
    if background_y1 >= HEIGHT:
        background_y1 = -HEIGHT
    if background_y2 >= HEIGHT:
        background_y2 = -HEIGHT

def draw_background():  #Отрисовка двух копий фона
    screen.blit(background, (0, background_y1))
    screen.blit(background, (0, background_y2))

while running:  #Игровой цикл
    clock.tick(FPS)

    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot()

    update_background()  #Обновление фона
    all_sprites.update()  #Обновление спрайтов
    #Проверка попаданий
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        explosion_sound.play()
        mob = Alien()
        all_sprites.add(mob)
        mobs.add(mob)
    #Проверка столкновений мобов с игроком
    hits = pygame.sprite.spritecollide(player, mobs, True)  #Проверка столкновений мобов с игроком
    if hits:
        player.lives -= 1
        hit_sound.play()
        if player.lives <= 0:
            show_game_over_screen()
            running = False

    screen.fill(BLACK)  #Заливка экрана
    draw_background()  #Отрисовка фона
    all_sprites.draw(screen)
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Счет: {score} Жизни: {player.lives}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
