import pygame
from pygame.locals import *
from settings import *
from utils import w12,h12

def MakeHud(font, screen, level, towersInfos, health, debug_mode):
    DisplayEnemyHealthBar(screen, level.enemies)
    if(debug_mode):
        DisplayDebugTools(font, screen, level)

    textEnemyCount = f"Enemies: {len(level.enemies)}"
    hud_textEnemyCount = font.render(textEnemyCount, True, WHITE)
    screen.blit(hud_textEnemyCount, (10, 10))
    
    textTowerCount = f"Towers:"
    hud_textTowerCount = font.render(textTowerCount, True, WHITE)
    screen.blit(hud_textTowerCount, (10, 25))

    textTowerCount = f"T1: {towersInfos[0].numberOf}"
    hud_textTowerCount = font.render(textTowerCount, True, WHITE)
    screen.blit(hud_textTowerCount, (10, 40))
    
    textTowerCount = f"T2: {towersInfos[1].numberOf}"
    hud_textTowerCount = font.render(textTowerCount, True, WHITE)
    screen.blit(hud_textTowerCount, (10, 55))
    
    textHealth = f"Health: {health}"
    hud_textHealth = font.render(textHealth, True, WHITE)
    screen.blit(hud_textHealth, (10, 70))


def DisplayEnemyHealthBar(screen, enemies):
    for enemy in enemies:
        rect = enemy.rect.copy()
        rect.w = (enemy.health / enemy.max_health) * 20
        rect.h = 5
        rect.centerx = enemy.rect.centerx
        rect.y =+ enemy.rect.y - 8
        pygame.draw.rect(screen, GREEN, rect)

def DisplayGameOverScreen(screen, level):
    # Create a semi-transparent black surface to overlay the screen
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Set the alpha value to 150 for transparency
    screen.blit(overlay, (0, 0))

    # Display text on the game over screen
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 64)

    gameover_text = big_font.render("Game Over", True, WHITE)
    gameover_rect = gameover_text.get_rect(center=(w12(6), h12(2)))
    screen.blit(gameover_text, gameover_rect)

    # Display enemy remaining count
    remaining_enemy_count_text = font.render(f"Enemies Remaining: {len(level.enemies)}", True, WHITE)
    remaining_enemy_count_rect = remaining_enemy_count_text.get_rect(center=(w12(6), h12(3)))
    screen.blit(remaining_enemy_count_text, remaining_enemy_count_rect)

    # Display enemy killed count
    enemy_killed_count_text = font.render(f"Enemies Killed: {level.enemies_killed}", True, WHITE)
    enemy_killed_count_rect = enemy_killed_count_text.get_rect(center=(w12(6), h12(4)))
    screen.blit(enemy_killed_count_text, enemy_killed_count_rect)

    # Display health
    health_text = font.render(f"Health: ({level.health}/{level.original_health})", True, WHITE)
    health_rect = health_text.get_rect(center=(w12(6), h12(5)))
    screen.blit(health_text, health_rect)

def DisplayDebugTools(font, screen, level):
    for i,enemy in enumerate(level.enemies):
        for y, routeStep in enumerate(enemy.route):
            block = level.area_blocks.sprites()[y]
            image = pygame.Surface((int(block.rect.w/3), int(block.rect.h/3)))
            color = BLACK
            if(routeStep.is_active):
                color = GREEN
            else:
                color = RED
            rect = image.get_rect()
            rect.centerx = block.rect.centerx
            rect.centery = block.rect.centery
            pygame.draw.rect(screen, color, rect)

        textEnemy = f"enemy {i}"
        hud_textEnemy = font.render(textEnemy, True, WHITE)
        screen.blit(hud_textEnemy, (w12(10), 10 + 50 * (i+1)))

        textEnemyHp = f"{enemy.health} hp"
        hud_textEnemyHp = font.render(textEnemyHp, True, WHITE)
        screen.blit(hud_textEnemyHp, (w12(10), 25 + 50 * (i+1)))

        textEnemyHp = f"pos: {enemy.rect.x},{enemy.rect.y}"
        hud_textEnemyHp = font.render(textEnemyHp, True, WHITE)
        screen.blit(hud_textEnemyHp, (w12(10), 40 + 50 * (i+1)))
    