from enum import Enum

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