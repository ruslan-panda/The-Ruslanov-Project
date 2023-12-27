import pygame
import os

pygame.init()
screen=pygame.display.set_mode((1200,800))
def draw_my_screen(my_simple_hero):
    my_simple_hero.draw_on_screen()#рисует уже обновновленного героя


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

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("hero_stop.png", -1)
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)

def run_game():
    pygame.display.set_caption('ХОХО ИТС МАРИО')
    clock=pygame.time.Clock()
    pygame.mouse.set_visible(1)
    game_active=True# Этот флаг нужен для завершения главного цикла игры
    mouse_x=0#если не добавить ошибка
    mouse_y=0#если не добавить ошибка
    my_simple_hero=Hero(screen)#Создание нашего персонажа, которого будем перемещать
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("mar.png")
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)


    while game_active:#Главный цикл игры. Пока флаг - истина, игра работает
        screen.fill((255,255,255))

        for event in pygame.event.get():#получение всех событий
            if event.type==pygame.QUIT:#проверка события "Выход"
                game_active=False

            if event.type == pygame.KEYDOWN:  # Если кнопка клавиатуры нажата, то...
                if event.key == pygame.K_d:  # Если это кнопка вправо, то...
                    my_simple_hero.movie_right = True  # перемещать героя вправо - Да!
                if event.key == pygame.K_a:
                    my_simple_hero.movie_left = True
                if event.key == pygame.K_w:
                    my_simple_hero.movie_forward = True
                if event.key == pygame.K_s:
                    my_simple_hero.movie_backward = True

            if event.type == pygame.KEYUP:  # Если кнопка отжата, то...
                if event.key == pygame.K_d:
                    my_simple_hero.movie_right = False
                if event.key == pygame.K_a:
                    my_simple_hero.movie_left = False
                if event.key == pygame.K_w:
                    my_simple_hero.movie_forward = False
                if event.key == pygame.K_s:
                    my_simple_hero.movie_backward = False
        # запуск функции нашего героя, которая меняет его расположение
        my_simple_hero.moving()

        draw_my_screen(my_simple_hero)#Эта функция рисует все объкты. Принимает в себя героя.

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()#Еслиб не добавить будет висеть окно

class Hero():#Класс нашего героя
    def __init__(self,screen,**kwargs):
        self.screen=screen#При инициализации получает ссылку на окно, в котором рисуются все на экране

        self.pos_x=100
        self.pos_y=100
        self.radius=10
        self.color=(0,0,255)
        #эти флажки нужны для постоянного перемещения героя
        self.movie_left=False
        self.movie_right=False
        self.movie_forward=False
        self.movie_backward=False
        spriterun1 = pygame.sprite.Sprite()
        spriterun1.rect = sprite.image.get_rect()
        all_sprites.add(sprite)

        #границы экрана за которые герой не перемещается
        self.max_y=800-self.radius
        self.max_x=1200-self.radius

    def moving(self):#перемещает героя
        if self.movie_left==True:
            self.pos_x-=10
            if self.pos_x<self.radius:
                self.pos_x=self.radius
        if self.movie_right==True:
            self.pos_x+=10
            if self.pos_x>self.max_x:
                self.pos_x=self.max_x
        if self.movie_forward==True:
            self.pos_y-=10
            if self.pos_y<self.radius:
                self.pos_y=self.radius
        if self.movie_backward==True:
            self.pos_y+=10
            if self.pos_y>self.max_y:
                self.pos_y=self.max_y
        sprite.rect.x = self.pos_x
        sprite.rect.y = self.pos_y

    def draw_on_screen(self):#рисует героя
        all_sprites.draw(screen)



run_game()#запускаем нашу игру