from pygame import *
import pygame
from globals import screen
import os
from pathlib import Path

plates = []
ingredients = []
actions = []
cooking_chain = []
buttons = []

class GameItem():
    _bounds_x = (0, 0)
    _bounds_y = (0, 0)
    _x = 0
    _y = 0
    _rect = None
    _item = None
    _stacked_item = None
    _draggable = False
    _clickable = False
    _stacked = False
    _image_path = None

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

    def is_clicked(self):
        pass

    def display(self):
        screen.blit(self._item, self._rect)

    def select(self):
        pygame.draw.rect(screen, pygame.Color(0, 0, 255), self._rect, 4)
    
    def is_draggable(self): 
        return self._draggable 

    def is_empty(self):
        return self._stacked_item is None

    def stack_item(self, items_list, index):
        if self.is_empty():
            items_list[index] = Ingredient(pygame.transform.scale(items_list[index]._item, self._item.get_size()), self._x, self._y)
            items_list[index]._stacked = True

    def scale_with(self, item_to_scale_with):
        self._item = pygame.transform.scale(self._item, item_to_scale_with.get_size())
        self._rect = self._item.get_rect(center=(self._x, self._y))


class Plate(GameItem):
    def __init__(self, item: Surface, x: int, y: int):
        super().__init__(item, x, y)


class Ingredient(GameItem):
    def __init__(self, item: Surface, x: int, y: int):
        self._draggable = True
        super().__init__(item, x, y)

    def display(self):
        if self._stacked:
            super().display()

class Action(GameItem):
    def __init__(self, item: Surface, x: int, y: int):
        self._draggable = True
        super().__init__(item, x, y)

    def display(self):
        if self._stacked:
            super().display()

class Button(GameItem):
    def __init__(self, x: int, y: int):
        self._item = pygame.image.load(os.path.join("assets", "buttons", "go.png"))
        self._clickable = True
        super().__init__(self._item, x, y)

    def is_clicked(self):
        if self.is_hovered():
            leftclick, _, _ = pygame.mouse.get_pressed()
            return leftclick

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

def generate_stoves(object: Surface, origin: tuple[int, int], rows: int, cols: int):
    positions = _generate_stack_positions(object, origin, rows + 1, cols)
    for pos in positions[:-1:]:
        cooking_chain.append(Stove(object, pos[0], pos[1]))

    pos = positions[-1]
    button = Button(pos[0], pos[1])
    buttons.append(button)
    buttons[-1].scale_with(object)

def load_ingredients(ingredient_sprites_list):
    for ingredient_file in ingredient_sprites_list:
        try:
            ingredient = pygame.image.load(ingredient_file)
            ingredients.append(Ingredient(ingredient, 0, 0))
        except TypeError:        
            print("Warning  not a file object: {}".format(ingredient_file))

    index = 0
    for plate in plates:
        if plate.is_empty():
            if index < len(ingredients) - 1:
                plate.stack_item(ingredients, index)
                index += 1

def load_actions(action_sprites_list):
    for action_file in action_sprites_list:
        try:
            action = pygame.image.load(action_file)
            actions.append(Action(action, 0, 0))
        except TypeError:
            print("Warning  not a file object: {}".format(action_file))

    index = 0
    for plate in plates:
        if plate.is_empty():
            if index < len(actions) - 1:
                plate.stack_item(actions, index)
                index += 1


def display_kitchen_items():
    for plate in plates:
        plate.display()

    for ingredient in ingredients:
        ingredient.display()
    
    # @todo fixme
    for action in actions:
        action.display()
        
    for element in cooking_chain:
        element.display()
        element.is_clicked()

    for button in buttons:
        button.display()

stocksoup_ad_path = os.path.join("assets", "drawings", "stocksoup.png")
stocksoup_ad = pygame.image.load(stocksoup_ad_path)
ad_size = stocksoup_ad.get_size()
stocksoup_ad_pos = (screen.get_width() - ad_size[0] / 2, ad_size[1] / 2)
print(screen.get_size(), stocksoup_ad_pos)
stocksoup_ad_obj = Stove(stocksoup_ad, stocksoup_ad_pos[0], stocksoup_ad_pos[1])

def last_minute_faff():
    if buttons[-1].is_clicked():
        stocksoup_ad_obj.display()


# Some utils functions

def generate_a_sprite_list_from_yaml_config(list):
    '''
    Quick helping function to build a list of sprites from a YAML file
    It expects the folling format with key="image_file" for file containing the sprite:

    Ingredients:
      Aubergine:
        image_file: assets/ingredients/Aubergine.png

      Carrot:
        image_file: assets\ingredients\Carrot.png
    '''
    sprites_list = []
    for key in list:
        if list[key] is not None:
            try:
                
                try:
                    file=Path(list[key]["image_file"])
                    print ("Key:{} Image:{}".format(key, list[key]["image_file"]))
                    sprites_list.append(file)
                except TypeError:
                   pass
            except KeyError:
               pass
    return sprites_list
