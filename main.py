# Example file showing a circle moving on screen
import pygame
import os
from generate import *
from globals import screen

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
station_img = pygame.image.load(os.path.join("assets", "station.png"))
first_station_pos = screen.get_width() / 4, screen.get_height() / 3
generate_plates(station_img, first_station_pos, 3, 3)
load_ingredients()
active_ingredient = None

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
          if event.button == 1:
            active_ingredient = None
        if event.type == pygame.MOUSEMOTION:
          if active_ingredient != None: 
            ingredients[active_ingredient]._rect.move_ip(event.rel)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    box = pygame.Rect(30,30,40,30)

    # Display station
    display_kitchen_items()

    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.rect(screen, "white", box,  40) ,

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Get the state of mouse buttons
    leftclick, _, rightclick = pygame.mouse.get_pressed()
    if leftclick:
        player_pos.x, player_pos.y = pygame.mouse.get_pos()
        for num, ingredient in enumerate(ingredients):
          if ingredient._rect.collidepoint(event.pos):
            active_ingredient = num
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
