import pygame
import sys

pygame.init()

width, height = 800, 600
white = (255, 255, 255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Анимация бега в Pygame")

running_image_1 = pygame.image.load("3.png")
running_image_2 = pygame.image.load("4.png")
running_image_3 = pygame.image.load("5.png")

standing_image_1 = pygame.image.load("1.png")
standing_image_2 = pygame.image.load("2.png")

flipped_running_image_1 = pygame.transform.flip(running_image_1, True, False)
flipped_running_image_2 = pygame.transform.flip(running_image_2, True, False)
flipped_running_image_3 = pygame.transform.flip(running_image_3, True, False)

player_width, player_height = 50, 160
player_x, player_y = width // 2 - player_width // 2, height - player_height

velocity_y = 0
gravity = 1
jump_height = -15

is_jumping = False
is_running = False
is_facing_left = False
running_animation_counter = 0
standing_animation_counter = 0

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
        running_animation_counter += 1
        standing_animation_counter = 0
        if running_animation_counter % 18 < 6:
            if is_facing_left:
                screen.blit(flipped_running_image_1, (player_x, player_y))
            else:
                screen.blit(running_image_1, (player_x, player_y))
        elif 6 <= running_animation_counter % 18 < 12:
            if is_facing_left:
                screen.blit(flipped_running_image_2, (player_x, player_y))
            else:
                screen.blit(running_image_2, (player_x, player_y))
        else:
            if is_facing_left:
                screen.blit(flipped_running_image_3, (player_x, player_y))
            else:
                screen.blit(running_image_3, (player_x, player_y))
    else:
        standing_animation_counter += 0.7
        if standing_animation_counter % 18 < 6:
            screen.blit(standing_image_1, (player_x, player_y))
        elif 6 <= standing_animation_counter % 18 < 12:
            screen.blit(standing_image_2, (player_x, player_y))
        else:
            screen.blit(standing_image_1, (player_x, player_y))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()