from enum import Enum
import math

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

def check_collision_circle(sprite, group, radius):
    sprite_rect = sprite.rect
    for other_sprite in group:
        dx = sprite_rect.centerx - other_sprite.rect.centerx
        dy = sprite_rect.centery - other_sprite.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance < radius + sprite_rect.width / 2 + other_sprite.rect.width / 2:
            return True
    return False