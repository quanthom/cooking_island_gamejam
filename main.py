# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

active_box = None
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
boxes = []
for i in range(5):
    x = 100
    y = 100
    w = 200
    h = 40
    box = pygame.Rect(x, y*i, w, h)
    boxes.append(box)

while running:

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    
    for box in boxes:
       pygame.draw.rect(screen, "white", box)
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for num, box in enumerate(boxes):
          print("click"+ " " + str(num))
          if box.collidepoint(event.pos):
            active_box = num
      if event.type == pygame.MOUSEMOTION: 
        if active_box != None:
          boxes[active_box].move_ip(event.rel)
          print(active_box) 
       
      if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        active_box = None

      if event.type == pygame.QUIT:
        running = False
 

    pygame.draw.circle(screen, "red", player_pos, 40)

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
    #leftclick, _, rightclick = pygame.mouse.get_pressed()
    #if leftclick:
     #   player_pos.x, player_pos.y = pygame.mouse.get_pos()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
