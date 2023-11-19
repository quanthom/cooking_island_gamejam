from pygame import *
import pygame
from globals import screen

plates = []
cooking_chain = []

class GameItem():
    _bounds_x = (0, 0)
    _bounds_y = (0, 0)
    _x = 0
    _y = 0
    _rect = None
    _item = None
    _stacked_item = None

    def __init__(self, item: Surface, x: int, y: int):
        width = item.get_width()
        height = item.get_height()
        self._x = x
        self._y = y
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
        screen.blit(self._item, self._rect)
        if not self.is_empty():
            self._item.blit(self._stacked_item, self._stacked_item.get_rect(center=(self._x, self._y)))

    def select(self):
        pygame.draw.rect(screen, pygame.Color(0, 0, 255), self._rect, 4)

    def is_empty(self):
        return self._stacked_item is None

    def store_item(self, item: Surface):
        if self.is_empty():
            self._stacked_item = item


class Plate(GameItem):
    def __init__(self, item: Surface, x: int, y: int):
        super().__init__(item, x, y)


class Ingredient(GameItem):
    def __init__(self, item: Surface, x: int, y: int):
        super().__init__(item, x, y)


class Stove(GameItem):
    def __init__(self, item: Surface, x: int, y: int):
        super().__init__(item, x, y)


def _generate_stack_positions(object: Surface, origin: tuple[int, int], rows: int, cols: int):
    w0, h0 = int(origin[0]), int(origin[1])
    w, h = int(object.get_width()), int(object.get_height())
    x_positions = range(w0, w0 + w * rows, w)
    y_positions = range(h0, h0 + h * cols, h)
    positions = [(x, y) for x in x_positions for y in y_positions]
    return positions

def generate_plates(object: Surface, origin: tuple[int, int], rows: int, cols: int):
    positions = _generate_stack_positions(object, origin, rows, cols)
    for pos in positions:
        plates.append(Plate(object, pos[0], pos[1]))

def display_kitchen_items():
    for plate in plates:
        plate.display()

    for element in cooking_chain:
        element.display()
