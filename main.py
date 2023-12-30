import pygame
import sys
import os

pygame.init()


width, height = 1500, 800
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра")

running_1 = pygame.image.load("data/3.png")
running_2 = pygame.image.load("data/4.png")
running_3 = pygame.image.load("data/5.png")

standing_1 = pygame.image.load("data/1.png")
standing_2 = pygame.image.load("data/2.png")

flipped_running_1 = pygame.transform.flip(running_1, True, False)
flipped_running_2 = pygame.transform.flip(running_2, True, False)
flipped_running_3 = pygame.transform.flip(running_3, True, False)

player_width, player_height = 50, 160
player_x, player_y = width // 2 - player_width // 2, height - player_height

velocity_y = 0
gravity = 1
jump_height = -15

is_jumping = False
is_running = False
is_facing_left = False
running_k = 0
standing_k = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                velocity_y = jump_height
                is_jumping = True
                is_running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 5
        is_running = True
        is_facing_left = True
    elif keys[pygame.K_RIGHT] and player_x < width - player_width:
        player_x += 5
        is_running = True
        is_facing_left = False
    else:
        is_running = False

    velocity_y += gravity
    player_y += velocity_y

    if player_y > height - player_height:
        player_y = height - player_height
        velocity_y = 0
        is_jumping = False

    screen.fill(white)
    if is_running:
        running_k += 1
        standing_k = 0
        if running_k % 18 < 6:
            if is_facing_left:
                screen.blit(flipped_running_1, (player_x, player_y))
            else:
                screen.blit(running_1, (player_x, player_y))
        elif 6 <= running_k % 18 < 12:
            if is_facing_left:
                screen.blit(flipped_running_2, (player_x, player_y))
            else:
                screen.blit(running_2, (player_x, player_y))
        else:
            if is_facing_left:
                screen.blit(flipped_running_3, (player_x, player_y))
            else:
                screen.blit(running_3, (player_x, player_y))
    else:
        standing_k += 0.7
        if standing_k % 18 < 6:
            screen.blit(standing_1, (player_x, player_y))
        elif 6 <= standing_k % 18 < 12:
            screen.blit(standing_2, (player_x, player_y))
        else:
            screen.blit(standing_1, (player_x, player_y))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
