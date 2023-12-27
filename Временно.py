import pygame
import sys

pygame.init()

width, height = 800, 600
white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Гравитация и Прыжок в Pygame")

player_width, player_height = 50, 50
player_x, player_y = width // 2 - player_width // 2, height - player_height

velocity_y = 0
gravity = 1
jump_height = -15  # Высота прыжка

is_jumping = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                velocity_y = jump_height
                is_jumping = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += 5

    velocity_y += gravity
    player_y += velocity_y

    if player_y > height - player_height:
        player_y = height - player_height
        velocity_y = 0
        is_jumping = False

    screen.fill(white)
    pygame.draw.rect(screen, black, (player_x, player_y, player_width, player_height))
    pygame.display.flip()

    pygame.time.Clock().tick(60)