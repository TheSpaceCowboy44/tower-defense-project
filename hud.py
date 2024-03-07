import pygame
from pygame.locals import *
from constants import *

def MakeHud(font, screen, enemies, towers_to_build, health):
    textEnemyCount = f"Enemies: {len(enemies)}"
    hud_textEnemyCount = font.render(textEnemyCount, True, WHITE)
    screen.blit(hud_textEnemyCount, (10, 10))
    
    textTowerCount = f"Towers: {towers_to_build}"
    hud_textTowerCount = font.render(textTowerCount, True, WHITE)
    screen.blit(hud_textTowerCount, (10, 30))
    
    textHealth = f"Health: {health}"
    hud_textHealth = font.render(textHealth, True, WHITE)
    screen.blit(hud_textHealth, (10, 50))

    DisplayEnemyHealthBar(screen, enemies)

def DisplayEnemyHealthBar(screen, enemies):
    for enemy in enemies:
        rect = enemy.rect.copy()
        rect.w = (enemy.health / enemy.max_health) * 20
        rect.h = 5
        rect.centerx = enemy.rect.centerx
        rect.y =+ enemy.rect.y - 8
        pygame.draw.rect(screen, GREEN, rect)
        