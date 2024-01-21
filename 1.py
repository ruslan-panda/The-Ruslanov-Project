import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

background_img = pygame.image.load("background.jpg")
bird_img = pygame.image.load("bird.png")
pipe_img = pygame.image.load("pipe.png")
spike_img = pygame.image.load("pipe.png")

bird_img = pygame.transform.scale(bird_img, (80, 60))
bird_img = pygame.transform.flip(bird_img, True, False)
pipe_img = pygame.transform.scale(pipe_img, (100, 500))
pipe_img = pygame.transform.flip(pipe_img, True, False)
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
spike_img = pygame.transform.scale(spike_img, (20, 20))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)
        self.gravity = 0.6
        self.velocity = 0
        self.jump_height = -10

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0
        elif self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

    def jump(self):
        self.velocity = self.jump_height


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, random.randint(200, 400))
        self.scored = False

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = WIDTH + random.randint(200, 400)
            self.rect.top = random.randint(200, 400)
            self.scored = False


class CeilingObstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = spike_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, 0)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.left = WIDTH + random.randint(200, 400)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = background_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self):
        pass


class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.score_timer = 0

    def update(self):
        self.score_timer += 1
        if self.score_timer % FPS == 0:
            self.score += 1

        self.image = self.font.render(f"Score: {self.score}", True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (10, 10)


all_sprites = pygame.sprite.Group()
pipes_group = pygame.sprite.Group()
ceiling_group = pygame.sprite.Group()

background = Background()
bird = Bird()
score = Score()

all_sprites.add(background, bird, score)

clock = pygame.time.Clock()
running = True
spawn_counter = 0
spawn_frequency = 60
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    spawn_counter += 1
    if spawn_counter >= spawn_frequency:
        new_pipe = Pipe(WIDTH)
        pipes_group.add(new_pipe)
        all_sprites.add(new_pipe)

        new_ceiling_obstacle = CeilingObstacle(WIDTH)
        ceiling_group.add(new_ceiling_obstacle)
        all_sprites.add(new_ceiling_obstacle)

        spawn_counter = 0

    all_sprites.update()

    if pygame.sprite.spritecollide(bird, pipes_group, False) or pygame.sprite.spritecollide(bird, ceiling_group, False):
        running = False

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