import pygame

import pygame_widgets
from pygame_widgets.button import Button

# Set up Pygame
pygame.init()
win = pygame.display.set_mode((600, 600))
click = False
# Creates the button with optional parameters
button = Button(
    # Mandatory Parameters
    win,  # Surface to place button on
    100,  # X-coordinate of top left corner
    100,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    inactiveColour=(200, 50, 0, 255),  # Colour of button when not being interacted with
    hoverColour=(150, 0, 0, 255),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20, 255),  # Colour of button when being clicked
    image=pygame.image.load("1.png"),
    onClick=lambda: print(234567890),  # Function to call when clicked on
    shadowDistance=255
)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    pygame.display.update()
