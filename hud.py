import pygame
from pygame.locals import *
from constants import *

def MakeHud(font, screen, enemies, towers_to_build):
    text = f"Enemies: {len(enemies)}"
    hud_text = font.render(text, True, WHITE)
    screen.blit(hud_text, (10, 10))
    text2 = f"Towers: {towers_to_build}"
    hud_text2 = font.render(text2, True, WHITE)
    screen.blit(hud_text2, (10, 30))
    DisplayEnemyHealthBar(screen, enemies)

def DisplayEnemyHealthBar(screen, enemies):
    for enemy in enemies:
        rect = enemy.rect.copy()
        rect.w = (enemy.health / enemy.max_health) * 20
        rect.h = 5
        rect.centerx = enemy.rect.centerx
        rect.y =+ enemy.rect.y - 8
        pygame.draw.rect(screen, GREEN, rect)
        