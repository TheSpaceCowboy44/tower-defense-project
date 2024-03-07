import random
import pygame
from pygame.locals import *
from enemy import *
import json

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
        self.enemyInfos = getEnemyInfos()
        self.enemy_spawn_executed = False

    def update(self,player):
        player_towers_collisions = pygame.sprite.spritecollide(player, self.towers, False)
        if(self.towers_to_build > 0):
            if(len(player_towers_collisions) == 0) and self.isInTowerArea(player) and not self.isInEnemyArea(player):
                player.can_place_tower = True
            else:
                player.can_place_tower = False
        self.towers.update(self.enemies, player)
        if not self.enemy_spawn_executed:
            self.spawnEnemies()
        for tower in self.towers:
            self.checkBulletCollision(tower.bullets, self.enemies)
        self.enemies.update()
        player.update(self)

    def draw(self, surface):
        for area_block in self.area_blocks:
            pygame.draw.rect(surface, area_block.color, area_block.rect)
        for tower in self.towers:
            tower.draw(surface)
        self.enemies.draw(surface)
        self.towers.draw(surface)
    
    def getEnemyAreaBlocks(self):
        enemy_area_blocks = pygame.sprite.Group()
        for area_block in self.area_blocks:
            if(area_block.type == "enemy_area"):
                enemy_area_blocks.add(area_block)
        return enemy_area_blocks
    
    def getTowerAreaBlocks(self):
        tower_area_blocks = pygame.sprite.Group()
        for area_block in self.area_blocks:
            if(area_block.type == "tower_area"):
                tower_area_blocks.add(area_block)
        return tower_area_blocks

    def isInTowerArea(self, sprite):
        tower_area_blocks = self.getTowerAreaBlocks()
        sprite_blocks_collisions = pygame.sprite.spritecollide(sprite, tower_area_blocks, False)
        return len(sprite_blocks_collisions) > 0
    
    def isInEnemyArea(self, sprite):
        enemy_area_blocks = self.getEnemyAreaBlocks()
        sprite_blocks_collisions = pygame.sprite.spritecollide(sprite, enemy_area_blocks, False)
        return len(sprite_blocks_collisions) > 0
    
    def checkBulletCollision(self, bullets, enemies):
        stick = pygame.sprite.groupcollide(bullets, enemies, False, False, pygame.sprite.collide_mask)
        for bullet, enemyList in stick.items():
            enemyList[0].health = enemyList[0].health - bullet.bullet_damage
            bullet.kill()
            if(enemyList[0].health <= 0):
                enemyList[0].kill()
    def spawnEnemies(self):
        now = pygame.time.get_ticks()
        for enemyData in self.enemyInfos:
            now = pygame.time.get_ticks()
            if now - self.enemy_spawn_timer > enemyData.spawnWaitTime:
                addEnemy(self, enemyData.enemyType)
                self.enemy_spawn_timer = now
        if(len(self.enemies) == len(self.enemyInfos)):
            self.enemy_spawn_executed = True

def addEnemy(self, enemyType):
    x_start_boundary = SCREEN_WIDTH/2-SMALL_CORRIDOR_GAP + SCREEN_WIDTH*0.02
    x_end_boundary = SCREEN_WIDTH/2+SMALL_CORRIDOR_GAP - SCREEN_WIDTH*0.04
    spawn_x = random.randint(x_start_boundary, x_end_boundary)
    enemy_sprite = create_enemy_sprite(enemyType, spawn_x, -200)
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

def getEnemyInfos():
    enemySpawnDataList = []
    with open('levels/level_0.json', 'r') as file:
        data = json.load(file)

    enemySpawnDataJson = data['enemySpawnData']

    for enemy in enemySpawnDataJson:
        enemy_type = enemy['enemyType']
        spawn_wait_time = enemy['spawnWaitTime']
        enemySpawnData = EnemySpawnData(int(enemy_type), int(spawn_wait_time))
        enemySpawnDataList.append(enemySpawnData)
    return enemySpawnDataList

def create_enemy_sprite(enemy_type, spawn_x, spawn_y):
    if enemy_type == 1:
        return Enemy_Type_1(spawn_x, spawn_y)
    elif enemy_type == 2:
        return Enemy_Type_2(spawn_x, spawn_y)
    elif enemy_type == 3:
        return Enemy_Type_3(spawn_x, spawn_y)
    else:
        raise ValueError(f"Unsupported enemyType: {enemy_type}")

class AreaBlock(pygame.sprite.Sprite):
    def __init__(self, rect, type, color):
        super().__init__()
        self.rect = rect
        self.type = type
        self.color = color
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
class EnemySpawnData:
    def __init__(self,enemyType, spawnWaitTime):
        self.enemyType = enemyType
        self.spawnWaitTime = spawnWaitTime