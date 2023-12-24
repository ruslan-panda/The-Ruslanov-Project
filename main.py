import pygame
import sys
import os

FPS = 60
WIDTH, HEIGHT = 550, 550
name_lvl = "map.txt"


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    try:
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))
    except FileNotFoundError:
        print("ТЫ ЧЁ МНЕ ПОДСУНУЛ")
        exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(100, 100)
        self.pos = pos_x, pos_y

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("ХОХО ИТС МАРИО")
tile_images = {
    'wall': load_image('floar.png'),
    'empty': load_image('back.png')
}
player_image = load_image('mar.png', -1)
level = load_level(name_lvl)
tile_width = tile_height = 50
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
pl_x = 0
pl_y = 0
main_pl = Player(pl_x, pl_y)
player_group.add(main_pl)


def generate_level(level):
    x = None
    y = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)

    # вернем игрока, а также размер поля в клетках



generate_level(load_level(name_lvl))

start_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            pl_x -= 5
        if keys[pygame.K_w]:
            pl_y -= 5
        if keys[pygame.K_d]:
            pl_x += 5
    main_pl.move(pl_x, pl_y)
    screen.fill("black")
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.update()
    clock.tick(FPS)
