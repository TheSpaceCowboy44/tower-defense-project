from enum import Enum
import math
import pygame
from pygame.locals import *

from constants import *

class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def MakeHud(font, screen, enemies, towers_to_build):
    text = f"Enemies: {len(enemies)}"
    hud_text = font.render(text, True, WHITE)
    screen.blit(hud_text, (10, 10))
    text2 = f"Towers: {towers_to_build}"
    hud_text2 = font.render(text2, True, WHITE)
    screen.blit(hud_text2, (10, 30))

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

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect)