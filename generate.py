from pygame import *
import pygame

def display_item(screen: Surface, object: Surface, pos: tuple[int, int]):
    station_rect = object.get_rect(center=pos)
    screen.blit(object, station_rect)

def generate_stack_positions(object: Surface, origin: tuple[int, int], rows: int, cols: int):
    w0, h0 = int(origin[0]), int(origin[1])
    w, h = int(object.get_width()), int(object.get_height())
    x_positions = range(w0, w0 + w * rows, w)
    y_positions = range(h0, h0 + h * cols, h)
    positions = [(x, y) for x in x_positions for y in y_positions]
    return positions

def display_stack_of(screen: Surface, object: Surface, origin: tuple[int, int], rows: int, cols: int):
    positions = generate_stack_positions(object, origin, rows, cols)
    for pos in positions:
        display_item(screen, object, pos)

