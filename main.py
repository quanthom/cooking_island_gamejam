# Example file showing a circle moving on screen
import pygame
import os
from generate import *
from globals import screen
from music import *
from pathlib import Path

try:
    import yaml
    from yaml.loader import SafeLoader
except ModuleNotFoundError:
    exit("Error: No module named yaml. Try\n pip install pyyaml")

# Open the YAML configuration file and load into a dictionary
# Ref: pyyaml documentation, available at https://pynative.com/python-yaml
#   accessed 23/11/2023
action_sprites_list = []
ingredient_sprites_list = []
with open('game_config.yaml') as f:
    game_config = yaml.load(f, Loader=SafeLoader)
    #print (yaml.dump(game_config))
    play_list = game_config['Music']['PlayList']

    actions_list = game_config['Actions']
    action_sprites_list = generate_a_sprite_list_from_yaml_config(actions_list)

    ingredients_list = game_config['Ingredients']
    ingredient_sprites_list = generate_a_sprite_list_from_yaml_config(ingredients_list)

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
station_img = pygame.image.load(os.path.join("assets", "station.png"))

first_station_pos = screen.get_width() / 4, screen.get_height() / 4
generate_plates(station_img, first_station_pos, 3, 3)

second_station_pos = screen.get_width() / 2 , screen.get_height() / 4
generate_plates(station_img, second_station_pos, 2, 2)

first_stove_pos = screen.get_width() / 6, 3 * screen.get_height() / 4
generate_stoves(station_img, first_stove_pos, 7, 1)


load_ingredients(ingredient_sprites_list)
load_actions(action_sprites_list)

# Trying to display a yellow part1 @todo
#pygame.mouse.set_visible(False)
#cursor_img = pygame.image.load(os.path.join("assets", "hand-yellow.svg.hi.png"))
#cursor_img_rect = cursor_img.get_rect()

active_ingredient = None
m = Music(play_list[0])
m.play(loop=True)

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

    # Trying to display a yellow part1=2 @todo
    #cursor_img_rect.center = pygame.mouse.get_pos()  # update position 
    #screen.blit(cursor_img, cursor_img_rect) # draw the cursor
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    box = pygame.Rect(30,30,40,30)

    # Display station
    display_kitchen_items()
    last_minute_faff()

    #We don't needs this anymore
    #pygame.draw.circle(screen, "red", player_pos, 40)

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
