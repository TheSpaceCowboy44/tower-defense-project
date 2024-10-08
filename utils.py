from enum import Enum
import math
import pygame
from pygame.locals import *

from settings import *

def check_collision_group_circle(sprite, group, radius):
    sprite_rect = sprite.rect
    for other_sprite in group:
        dx = sprite_rect.centerx - other_sprite.rect.centerx
        dy = sprite_rect.centery - other_sprite.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance < radius + sprite_rect.width / 2 + other_sprite.rect.width / 2:
            return other_sprite
    return False

def check_collision_circle(sprite1, sprite2, radius):
    sprite_rect = sprite1.rect
    dx = sprite_rect.centerx - sprite2.rect.centerx
    dy = sprite_rect.centery - sprite2.rect.centery
    distance = math.sqrt(dx**2 + dy**2)
    if distance < radius + sprite_rect.width / 2 + sprite2.rect.width / 2:
        return True
    return False

def calculer_angle(x1, y1, x2, y2):
    # Calculer les différences entre les coordonnées
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Calculer l'angle en radians
    angle_radians = math.atan2(delta_y, delta_x)

    # Convertir l'angle en degrés
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees

def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect.topleft)

def h12(multiplier):
    return int(SCREEN_HEIGHT * (multiplier/12))
def w12(multiplier):
    return int(SCREEN_WIDTH * (multiplier/12))

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

class TypeOfStep(Enum):
    NORMAL = 0
    ENTRY = 1
    EXIT = 2

class TowerType(Enum):
    TOWER_1 = 1
    TOWER_2 = 2
    TOWER_3 = 3

class Level(Enum):
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 2

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_dict(self):
        return {"x": self.x, "y": self.y}