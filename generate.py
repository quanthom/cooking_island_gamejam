from pygame import *
import pygame

stations = []

class GameItem():
    _bounds_x = (0, 0)
    _bounds_y = (0, 0)
    _rect = None
    _screen = None
    _item = None

    def __init__(self, screen: Surface, item: Surface, x: int, y: int):
        self._screen = screen
        width = item.get_width()
        height = item.get_height()
        self._bounds_x = (x - width / 2, x + width / 2)
        self._bounds_y = (y - width / 2, y + height / 2)
        self._item = item
        self._rect = item.get_rect(center=(x, y))

    def is_hovered(self):
        mx, my = pygame.mouse.get_pos()
        if (
            mx >= self._bounds_x[0] and mx < self._bounds_x[1] and
            my >= self._bounds_y[0] and my < self._bounds_y[1]
        ):
            return True
        else:
            return False

    def display(self):
        self._screen.blit(self._item, self._rect)

    def select(self):
        pygame.draw.rect(self._screen, pygame.Color(0, 0, 255), self._rect, 4)

def generate_stack_positions(object: Surface, origin: tuple[int, int], rows: int, cols: int):
    w0, h0 = int(origin[0]), int(origin[1])
    w, h = int(object.get_width()), int(object.get_height())
    x_positions = range(w0, w0 + w * rows, w)
    y_positions = range(h0, h0 + h * cols, h)
    positions = [(x, y) for x in x_positions for y in y_positions]
    return positions

def generate_stations(screen: Surface, object: Surface, origin: tuple[int, int], rows: int, cols: int):
    positions = generate_stack_positions(object, origin, rows, cols)
    for pos in positions:
        stations.append(GameItem(screen, object, pos[0], pos[1]))

def display_stations():
    for station in stations:
        station.display()