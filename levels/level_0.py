import pygame
from pygame.locals import *
from enemy import *

class Level_0(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = (pygame.display.Info().current_w - width) // 2
        self.rect.y = (pygame.display.Info().current_h - height) // 2
        self.enemies = getEnemylist()
        self.area_blocks = getAreaBlocks()
        self.towers_to_build = 3

    def draw(self, surface):
        # Fill the entire surface with a transparent color
        self.image.fill((0, 0, 0, 0))

        for area_block in self.area_blocks:
            pygame.draw.rect(surface, area_block.color, area_block.rect)
    
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

def getEnemylist():
    enemies = pygame.sprite.Group()
    for i in range(3):
        spawn_x = random.randint(SCREEN_WIDTH/2-SMALL_CORRIDOR_GAP, SCREEN_WIDTH/2+SMALL_CORRIDOR_GAP)
        enemy_sprite = Enemy_Type_1(spawn_x, 0)
        enemies.add(enemy_sprite)
    return enemies

def getAreaBlocks():
    area_blocks = pygame.sprite.Group()
    center_rect = pygame.Rect(SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP, 0, SCREEN_WIDTH - (SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP) * 2, SCREEN_HEIGHT)
    left_rect = pygame.Rect(0, 0, SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP, SCREEN_HEIGHT)
    right_rect = pygame.Rect(SCREEN_WIDTH/2 + SMALL_CORRIDOR_GAP, 0, SCREEN_WIDTH/2 - SMALL_CORRIDOR_GAP, SCREEN_HEIGHT)
    center_block = AreaBlock(center_rect, "enemy_area", NOTVERYBLACK1)
    left_block = AreaBlock(left_rect, "tower_area", NOTVERYBLACK2)
    right_block = AreaBlock(right_rect, "tower_area", NOTVERYBLACK2)
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
