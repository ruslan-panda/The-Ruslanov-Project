import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 50
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Динозаврик")
dino_img_1 = pygame.image.load("dino1.png")
dino_img_2 = pygame.image.load("dino2.png")
dino_img_3 = pygame.image.load("dino3.png")
cactus_img = pygame.image.load("cactus.png")
background_img = pygame.image.load("background.jpg")
ground_img = pygame.image.load("ground.png")


dino_img_1 = pygame.transform.scale(dino_img_1, (70, 70))
dino_img_2 = pygame.transform.scale(dino_img_2, (70, 70))
dino_img_3 = pygame.transform.scale(dino_img_3, (70, 70))
cactus_img = pygame.transform.scale(cactus_img, (50, 70))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [dino_img_1, dino_img_2, dino_img_3]
        self.index = 0
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT - GROUND_HEIGHT - 25)
        self.gravity = 0.8
        self.jump_height = -17
        self.velocity = 0
        self.animation_speed = 5

    def update(self):
        self.index += 1
        if self.index >= len(self.images) * self.animation_speed:
            self.index = 0
        self.image = self.images[self.index // self.animation_speed]

        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.bottom > HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.velocity = 0

    def jump(self):
        if self.rect.bottom == HEIGHT - GROUND_HEIGHT:
            self.velocity += self.jump_height


class Cactus(pygame.sprite.Sprite):
    def __init__(self, last_position):
        super().__init__()
        self.image = cactus_img
        self.rect = self.image.get_rect()
        self.rect.center = (last_position + random.randint(200, 400), HEIGHT - GROUND_HEIGHT - 25)
        self.scored = False

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.centery = HEIGHT - GROUND_HEIGHT - 25
            self.scored = False


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = background_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self):
        pass


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ground_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, HEIGHT - GROUND_HEIGHT)

    def update(self):
        pass


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def update(self):
        self.image = self.font.render(f"Score: {self.score}", True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)


class GameOverScreen(pygame.sprite.Sprite):
    def __init__(self, score):
        super().__init__()
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.font = pygame.font.Font(None, 72)
        self.game_over_text = self.font.render("Game Over", True, BLACK)
        self.game_over_rect = self.game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))

        self.score_text = self.font.render(f"Score: {score}", True, BLACK)
        self.score_rect = self.score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        pass


all_sprites = pygame.sprite.Group()
cacti_group = pygame.sprite.Group()

background = Background()
ground = Ground()
dino = Dino()
score = Score()

all_sprites.add(background, ground, dino, score)

clock = pygame.time.Clock()
running = True
spawn_counter = 0
spawn_frequency = 120
last_cactus_position = WIDTH
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()

    all_sprites.update()
    if pygame.sprite.spritecollide(dino, cacti_group, False):
        game_over_screen = GameOverScreen(score.score)
        all_sprites.add(game_over_screen)
        running = False

    for cactus in cacti_group:
        if cactus.rect.right < dino.rect.left and not cactus.scored:
            cactus.scored = True
            score.score += 1

    spawn_counter += 1
    if spawn_counter >= spawn_frequency:
        new_cactus = Cactus(last_cactus_position)
        cacti_group.add(new_cactus)
        all_sprites.add(new_cactus)
        last_cactus_position = new_cactus.rect.right + random.randint(200, 400)
        spawn_counter = 0

    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

font = pygame.font.Font(None, 72)
game_over_text = font.render("Game Over", True, BLACK)
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
screen.blit(game_over_text, game_over_rect)

score_text = font.render(f"Счёт: {score.score}", True, BLACK)
score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
screen.blit(score_text, score_rect)

pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.key == pygame.K_RETURN:
                waiting = False
                running = False

pygame.quit()
sys.exit()