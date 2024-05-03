import random
import pygame
from pygame.locals import *
from enemy import *
import json

class MainLevel(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (pygame.display.Info().current_w - width) // 2
        self.rect.y = (pygame.display.Info().current_h - height) // 2
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.configFile = ''
        self.enemyInfos = []
        self.towerInfos = []
        self.gameover = {'state': 'lost', 'hasEnded': False }
        self.timer = pygame .time.get_ticks()

    def update(self,player):
        player_towers_collisions = pygame.sprite.spritecollide(player, self.towers, False)
        
        if(len(player_towers_collisions) == 0) and self.isInTowerArea(player) and not self.isInEnemyArea(player):
            player.can_place_tower = True
        else:
            player.can_place_tower = False
        self.towers.update(self.enemies, player)
        
        for enemy in self.enemies:
            if(enemy.rect.y > SCREEN_HEIGHT + 20):
                self.health = self.health - enemy.damage
                enemy.kill()
        for tower in self.towers:
            self.checkBulletCollision(tower.bullets, self.enemies)
        self.enemies.update()
        player.update(self)
        self.gameover = self.checkGameOver()

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
        for enemyData in self.enemyInfos:
            addEnemy(self, enemyData)
    def checkGameOver(self):
        if(self.health <= 0):
            now = pygame.time.get_ticks()
            if(now - self.timer > 15000):
                return {'state': 'lost', 'hasEnded': True }
        elif(len(self.enemies) == 0 and self.health > 0):
            now = pygame.time.get_ticks()
            if(now - self.timer > 15000):
                return {'state': 'won', 'hasEnded': True }
    def reset(self, width, height):
        self.__init__(width, height)


def addEnemy(self, enemy):
    x_start_boundary = SCREEN_WIDTH/2-SMALL_CORRIDOR_GAP + SCREEN_WIDTH*0.02
    x_end_boundary = SCREEN_WIDTH/2+SMALL_CORRIDOR_GAP - SCREEN_WIDTH*0.04
    spawn_x = random.randint(x_start_boundary, x_end_boundary)
    enemy = makeEnemy(enemy.enemyType, spawn_x, enemy.spawn_y)
    self.enemies.add(enemy)

def getEnemyInfosFromJson(json_file):
    enemySpawnDataList = []
    with open(json_file, 'r') as file:
        data = json.load(file)

    enemySpawnDataJson = data['enemySpawnData']

    for enemy in enemySpawnDataJson:
        enemy_type = int(enemy['enemyType'])
        spawn_y = int(enemy['spawn_y'])
        enemySpawnData = EnemySpawnData(enemy_type, spawn_y)
        enemySpawnDataList.append(enemySpawnData)
    return enemySpawnDataList

def getTowerInfosFromJson(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    towersData = data['towersData']
    for towerData in towersData:
        if towerData.get('tower_1') is not None:
            tower_1 = TowerAvailabilityData(1, int(towerData['tower_1']))
        if towerData.get('tower_2') is not None:
            tower_2 = TowerAvailabilityData(2, int(towerData['tower_2']))
        if towerData.get('tower_3') is not None:
            tower_3 = TowerAvailabilityData(3, int(towerData['tower_3']))
    towerDataList = [tower_1, tower_2, tower_3]
    return towerDataList

def makeEnemy(enemy_type, spawn_x, spawn_y):
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
    def __init__(self,enemyType, spawn_y):
        self.enemyType = enemyType
        self.spawn_y = spawn_y

class TowerAvailabilityData:
    def __init__(self,towerType, numberOfTower):
        self.towerType = towerType
        self.numberOf = numberOfTower