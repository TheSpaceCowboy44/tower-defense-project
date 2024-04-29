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

def DisplayGameOverScreen(screen, enemies):
    # Create a semi-transparent black surface to overlay the screen
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Set the alpha value to 150 for transparency
    screen.blit(overlay, (0, 0))

    # Display text on the game over screen
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, WHITE)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    screen.blit(text, text_rect)

    # Display enemy count
    enemy_count_text = font.render(f"Enemies Remaining: {len(enemies)}", True, WHITE)
    enemy_count_rect = enemy_count_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(enemy_count_text, enemy_count_rect)