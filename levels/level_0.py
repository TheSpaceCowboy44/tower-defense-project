import random
import pygame
from pygame.locals import *
from enemy import *

class Level_0(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (pygame.display.Info().current_w - width) // 2
        self.rect.y = (pygame.display.Info().current_h - height) // 2
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.area_blocks = getAreaBlocks()
        self.towers_to_build = 3
        self.health = 100
        self.enemy_spawn_timer = pygame.time.get_ticks()

    def update(self,player):
        player_towers_collisions = pygame.sprite.spritecollide(player, self.towers, False)
        if(self.towers_to_build > 0):
            if(len(player_towers_collisions) == 0) and self.isInTowerArea(player) and not self.isInEnemyArea(player):
                player.can_place_tower = True
            else:
                player.can_place_tower = False
        self.towers.update(self.enemies, player)
        if(len(self.enemies) < 3):
            now = pygame.time.get_ticks()
            if now - self.enemy_spawn_timer > 2000:
                addEnemy(self)
                self.enemy_spawn_timer = now
        self.enemies.update()

    def draw(self, surface):
        for area_block in self.area_blocks:
            pygame.draw.rect(surface, area_block.color, area_block.rect)
        for tower in self.towers:
            tower.draw(surface)
        self.enemies.draw(surface)
    
    def isInTowerArea(self, player):
        tower_area_blocks = pygame.sprite.Group()
        for area_block in self.area_blocks:
            if(area_block.type == "tower_area"):
                tower_area_blocks.add(area_block)
        player_blocks_collisions = pygame.sprite.spritecollide(player, tower_area_blocks, False)
        return len(player_blocks_collisions) > 0
    
    def isInEnemyArea(self, player):
        enemy_area_blocks = pygame.sprite.Group()
        for area_block in self.area_blocks:
            if(area_block.type == "enemy_area"):
                enemy_area_blocks.add(area_block)
        player_blocks_collisions = pygame.sprite.spritecollide(player, enemy_area_blocks, False)
        return len(player_blocks_collisions) > 0

def addEnemy(self):
    x_start_boundary = SCREEN_WIDTH/2-SMALL_CORRIDOR_GAP + SCREEN_WIDTH*0.02
    x_end_boundary = SCREEN_WIDTH/2+SMALL_CORRIDOR_GAP - SCREEN_WIDTH*0.04
    spawn_x = random.randint(x_start_boundary, x_end_boundary)
    enemy_sprite = Enemy_Type_1(spawn_x, -200)
    self.enemies.add(enemy_sprite)

def getAreaBlocks():
    area_blocks = pygame.sprite.Group()
    center_rect = pygame.Rect(SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP, 0, SCREEN_WIDTH - (SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP) * 2, SCREEN_HEIGHT)
    left_rect = pygame.Rect(0, 0, SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP, SCREEN_HEIGHT)
    right_rect = pygame.Rect(SCREEN_WIDTH/2 + SMALL_CORRIDOR_GAP, 0, SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP, SCREEN_HEIGHT)
    center_block = AreaBlock(center_rect, "enemy_area", NOTVERYBLACK1)
    left_block = AreaBlock(left_rect, "tower_area", NOTVERYBLACK2)
    right_block = AreaBlock(right_rect, "tower_area", NOTVERYBLACK2)
    # center_block = AreaBlock(center_rect, "enemy_area", GREEN_GRASS_DARK)
    # left_block = AreaBlock(left_rect, "tower_area", GREEN_GRASS_LIGHT)
    # right_block = AreaBlock(right_rect, "tower_area", GREEN_GRASS_LIGHT)
    area_blocks.add(left_block,right_block, center_block)
    return area_blocks

class AreaBlock(pygame.sprite.Sprite):
    def __init__(self, rect, type, color):
        super().__init__()
        self.rect = rect
        self.type = type
        self.color = color
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
