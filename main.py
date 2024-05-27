import os
import pygame
from pygame.locals import *
import sys

from button import Button
from fake_block import FakeBlock
from levels.level_0.level_0 import Level_0
from settings import *
from levels.level_1.level_1 import Level_1
from player import Player
from hud.hud import DisplayGameOverScreen, MakeHud


def chooseCurrentLevel(level_name):
    if(level_name == "level_0"):
        return Level_0(SCREEN_WIDTH, SCREEN_HEIGHT)
    if(level_name == "level_1"):
        return Level_1(SCREEN_WIDTH, SCREEN_HEIGHT)


# Initialize Pygame
pygame.init()

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense Game")
clock = pygame.time.Clock()

levels = []
levels_directory = os.listdir("levels")
for level in levels_directory:
    if("level_" in level):
        levels.append(level)

current_level_name = levels[0]
current_level = chooseCurrentLevel(current_level_name)

font = pygame.font.Font(None, 20)

player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

button1 = Button("Start", (SCREEN_WIDTH/4, SCREEN_HEIGHT*(1/5)), (SCREEN_WIDTH/2, SCREEN_HEIGHT/10), 36, "start_start")
button2 = Button("Quit", (SCREEN_WIDTH/4, SCREEN_HEIGHT*(2/5)), (SCREEN_WIDTH/2, SCREEN_HEIGHT/10), 36, "start_quit")
start_menu_buttons = [button1, button2]

for i, level in enumerate(levels):
    button_select_level = Button(f"{i}", (i*(SCREEN_WIDTH/10) + (SCREEN_WIDTH/20), SCREEN_HEIGHT - 100), (SCREEN_WIDTH/20, SCREEN_HEIGHT/20), 28, f"start_level_{i}")
    start_menu_buttons.append(button_select_level)

button_Ok = Button("Ok", (SCREEN_WIDTH // 2 - 50 -120, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/8), (120, 40), 36, "gameover_ok")
button_Retry = Button("Retry", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT/2 + SCREEN_HEIGHT/8), (120, 40), 36, "gameover_retry")
gameover_buttons = [button_Ok, button_Retry]

all_buttons = start_menu_buttons + gameover_buttons

level_started = False
game_state = "startmenu"

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                for button in all_buttons:
                    if button.is_clicked(pos):
                        if button.id == "start_start" and game_state == "startmenu":
                            print("Start button clicked")
                            level_started = True
                            game_state = "in_game"
                        elif button.id == "start_quit" and game_state == "startmenu":
                            running = False  # Quit the game
                        for i, level in enumerate(levels):
                            if button.id == f"start_level_{i}" and game_state == "startmenu":
                                for start_menu_button in start_menu_buttons:
                                    start_menu_button.background_color = GRAY
                                button.background_color = GREEN
                                current_level = chooseCurrentLevel(f"level_{i}")
                        if button.id == "gameover_ok" and game_state == "gameover":
                            level_started = False
                            game_state = "startmenu"
                        elif button.id == "gameover_retry" and game_state == "gameover":
                            level_started = True
                            game_state = "in_game"
                        

    now = pygame.time.get_ticks()

    if(game_state == "in_game"):
        if(level_started):
            current_level.reset(SCREEN_WIDTH, SCREEN_HEIGHT)
            level_started = False
        # Update
        current_level.update(player)

        # Draw
        current_level.draw(screen)
        player.draw(screen)
        screen.blit(current_level.image, current_level.rect.topleft)
        MakeHud(font, screen, current_level.enemies, current_level.towerInfos, current_level.health)
        if current_level.gameover is not None and current_level.gameover.get('hasEnded', False) == True :
            DisplayGameOverScreen(screen, current_level.enemies)
            game_state = "gameover"

    if(game_state == "startmenu"):
        screen.fill(BLACK)
        for button in start_menu_buttons:
            button.draw(screen)
    if(game_state == "gameover"):
        for button in gameover_buttons:
            button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

