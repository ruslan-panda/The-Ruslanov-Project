import pygame
from pygame.locals import *
import sys
import random
import time
import os
import pygame_widgets
from pygame_widgets.button import Button


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


g1 = False
g2 = False
g3 = False


def start_screen():
    global s1, s2
    s1 = True
    pygame.init()

    width, height = 1500, 800
    white = (255, 255, 255)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Анимация бега в Pygame")

    fon = pygame.transform.scale(load_image('bg.jpg'), (width, height))
    but = pygame.image.load("button.png")
    screen.blit(fon, (0, 0))
    button = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on

        410,  # X-coordinate of top left corner
        240,  # Y-coordinate of top left corner
        310,  # Width
        120,  # Height

        # Optional Parameters
        image=but,
        inactiveColour=(118, 174, 99, 255),  # Colour of button when not being interacted with
        hoverColour=(120, 160, 99, 0),  # Colour of button when being hovered over
        pressedColour=(0, 200, 20, 0),  # Colour of button when being clicked

    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button.clicked:
                s1 = False
                s2 = True
                return
            pygame_widgets.update(event)  # Call once every loop to allow widgets to render and listen
            pygame.display.flip()


def game1():
    global g1
    pygame.init()
    vec = pygame.math.Vector2

    HEIGHT = 600
    WIDTH = 550
    ACC = 0.5
    FRIC = -0.12
    FPS = 60

    FramePerSec = pygame.time.Clock()

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    global g1
    background = pygame.image.load("bg.jpg")
    otd = pygame.image.load("mr.png")

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.surf = pygame.image.load("1.png")
            self.rect = self.surf.get_rect()

            self.pos = vec((10, 360))
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.jumping = False
            self.score = 0

        def move(self):
            self.acc = vec(0, 0.5)

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[K_a]:
                self.acc.x = -ACC
            if pressed_keys[K_d]:
                self.acc.x = ACC

            self.acc.x += self.vel.x * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            if self.pos.x > WIDTH:
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = WIDTH

            self.rect.midbottom = self.pos

        def jump(self):
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits and not self.jumping:
                self.jumping = True
                self.vel.y = -15

        def cancel_jump(self):
            if self.jumping:
                if self.vel.y < -3:
                    self.vel.y = -3

        def update(self):
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if self.vel.y > 0:
                if hits:
                    if self.pos.y < hits[0].rect.bottom:
                        if hits[0].point == True:
                            hits[0].point = False
                            self.score += 1
                        self.pos.y = hits[0].rect.top + 1
                        self.vel.y = 0
                        self.jumping = False

    class Coin(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()

            self.image = pygame.image.load("Coin.png")
            self.rect = self.image.get_rect()

            self.rect.topleft = pos

        def update(self):
            if self.rect.colliderect(P1.rect):
                P1.score += 5
                self.kill()

    class platform(pygame.sprite.Sprite):
        def __init__(self, width=0, height=18):
            super().__init__()

            if width == 0:
                width = random.randint(50, 120)

            self.image = pygame.image.load("platform.png")
            self.surf = pygame.transform.scale(self.image, (width, height))
            self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                                   random.randint(0, HEIGHT - 30)))

            self.point = True
            self.moving = True
            self.speed = random.randint(-1, 1)

            if self.speed == 0:
                self.moving == False

        def move(self):
            hits = self.rect.colliderect(P1.rect)
            if self.moving == True:
                self.rect.move_ip(self.speed, 0)
                if hits:
                    P1.pos += (self.speed, 0)
                if self.speed > 0 and self.rect.left > WIDTH:
                    self.rect.right = 0
                if self.speed < 0 and self.rect.right < 0:
                    self.rect.left = WIDTH

        def generateCoin(self):
            if self.speed == 0:
                coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))

    def check(platform, groupies):
        if pygame.sprite.spritecollideany(platform, groupies):
            return True
        else:
            for entity in groupies:
                if entity == platform:
                    continue
                if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                    return True
            C = False

    def plat_gen():
        while len(platforms) < 8:
            width = random.randrange(50, 100)
            p = None
            C = True

            while C:
                p = platform()
                p.rect.center = (random.randrange(0, WIDTH - width),
                                 random.randrange(-50, 0))
                C = check(p, platforms)

            p.generateCoin()
            platforms.add(p)
            all_sprites.add(p)

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    PT1 = platform(1400, 80)
    PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    PT1.moving = False
    PT1.point = False

    P1 = Player()

    all_sprites.add(PT1)
    all_sprites.add(P1)
    platforms.add(PT1)

    for x in range(random.randint(4, 5)):
        C = True
        pl = platform()
        while C:
            pl = platform()
            C = check(pl, platforms)
        pl.generateCoin()
        platforms.add(pl)
        all_sprites.add(pl)

    run = True

    button_zak = Button(
        displaysurface,
        100,
        250,
        400,
        150,


        text='Легкий',
        fontSize=50,
        radius=10,
        textColour=(255, 255, 255, 255),
        inactiveColour=(0, 204, 0, 255),
        hoverColour=(0, 102, 0, 255),
        pressedColour=(0, 102, 0, 255),

    )

    while True:
        P1.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    P1.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    P1.cancel_jump()

        if P1.rect.top <= HEIGHT / 3:
            P1.pos.y += abs(P1.vel.y)
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

            for coin in coins:
                coin.rect.y += abs(P1.vel.y)
                if coin.rect.top >= HEIGHT:
                    coin.kill()

        plat_gen()
        displaysurface.blit(background, (0, 0))
        f = pygame.font.SysFont("Verdana", 20)
        g = f.render(str(P1.score), True, (123, 255, 0))
        displaysurface.blit(g, (WIDTH / 2, 10))

        for entity in all_sprites:
            displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        for coin in coins:
            displaysurface.blit(coin.image, coin.rect)
            coin.update()

        if P1.rect.top > HEIGHT:
            for entity in all_sprites:
                entity.kill()
            time.sleep(1)
            displaysurface.blit(otd, (0, 0))
            g1 = False
            run = False
            g1 = False
            f = pygame.font.SysFont("SONY Fixed", 100)
            g = f.render(str(P1.score), True, (123, 255, 0))
            text_rect = g.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            displaysurface.blit(g, text_rect)
            pygame.display.update()
            time.sleep(5)
            level_selection()
            return

        if button_zak.clicked:
            level_selection()

        pygame.display.update()
        FramePerSec.tick(FPS)


def level_selection():
    pygame.init()

    width, height = 1500, 800
    white = (255, 255, 255)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Анимация бега в Pygame")

    global g1, g2, g3
    fon = pygame.transform.scale(load_image('start_game.png'), (width, height))
    screen.blit(fon, (0, 0))
    button1 = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        100,  # X-coordinate of top left corner
        250,  # Y-coordinate of top left corner
        400,  # Width
        150,  # Height

        # Optional Parameters
        text='Легкий',  # Text to display
        fontSize=50,  # Size of font
        radius=10,
        textColour=(255, 255, 255, 255),
        inactiveColour=(0, 204, 0, 255),  # Colour of button when not being interacted with
        hoverColour=(0, 102, 0, 255),  # Colour of button when being hovered over
        pressedColour=(0, 102, 0, 255),  # Colour of button when being clicked

    )
    button2 = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        550,  # X-coordinate of top left corner
        250,  # Y-coordinate of top left corner
        400,  # Width
        150,  # Height

        # Optional Parameters
        text='Средний',  # Text to display
        fontSize=50,  # Size of font
        radius=10,
        textColour=(255, 255, 255, 255),
        inactiveColour=(204, 204, 0, 255),  # Colour of button when not being interacted with
        hoverColour=(102, 102, 0, 255),  # Colour of button when being hovered over
        pressedColour=(102, 102, 0, 255),  # Colour of button when being clicked

    )
    button3 = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        1000,  # X-coordinate of top left corner
        250,  # Y-coordinate of top left corner
        400,  # Width
        150,  # Height

        # Optional Parameters
        text='Сложный',  # Text to display
        fontSize=50,  # Size of font
        radius=10,
        textColour=(255, 255, 255, 255),
        inactiveColour=(204, 0, 0, 255),  # Colour of button when not being interacted with
        hoverColour=(102, 0, 0, 255),  # Colour of button when being hovered over
        pressedColour=(102, 0, 0, 255),  # Colour of button when being clicked

    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button1.clicked:
                g1 = True
                game1()
                return
            if button2.clicked:
                g2 = True

                return
            if button3.clicked:
                g3 = True

                return
            pygame_widgets.update(event)  # Call once every loop to allow widgets to render and listen
            pygame.display.flip()


start_screen()
level_selection()
