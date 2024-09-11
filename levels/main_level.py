from enum import Enum
import random
import pygame
from pygame.locals import *
from enemy import *
import json

from utils import TypeOfStep, h12, w12

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
        self.enemies_killed = 0
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.configFile = ''
        self.enemyInfos = []
        self.towerInfos = []
        self.route_steps = []
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
            if(enemy.rect.x > SCREEN_WIDTH + 100 or enemy.rect.x < -100):
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
            if(area_block.type == AreaBlockType.ENEMY):
                enemy_area_blocks.add(area_block)
        return enemy_area_blocks
    
    def getTowerAreaBlocks(self):
        tower_area_blocks = pygame.sprite.Group()
        for area_block in self.area_blocks:
            if(area_block.type == AreaBlockType.TOWER):
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
                self.enemies_killed += 1

    def spawnEnemies(self):
        for enemyData in self.enemyInfos:
            self.addEnemy(enemyData)
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
    
    def getRouteSteps(self, routeStepsMap):
        routeSteps = []
        for y, row in enumerate(routeStepsMap):
            for x, tile in enumerate(row):
                waypoint = tile["wp"]
                if(int(waypoint[0]) == 1):
                    isActive = True
                else:
                    isActive = False
                position = Position(x*w12(2), y*h12(2))
                routeStep = EnemyRouteStep(position, Direction(waypoint[1]), isActive, TypeOfStep(waypoint[2]))
                routeSteps.append(routeStep)
        return routeSteps
    
    def addEnemy(self, enemyData):
        route = self.getRouteSteps(self.route_steps)
        pos = getFirstEnemyPathPosition(route)
        spawn_x = random.randint(pos.x, pos.x + w12(2))
        enemy = makeEnemy(enemyData.enemyType, spawn_x, enemyData.spawn_y)
        enemy.route = route
        if(spawn_x > spawn_x + enemy.rect.width):
            enemy.rect.x = spawn_x
        self.enemies.add(enemy)

def getFirstEnemyPathPosition(route):
    for step in route:
        if step.typeOfStep == TypeOfStep.ENTRY:
            return step.position


def getEnemyInfosFromJson(json_file):
    enemySpawnDataList = []
    enemySpawnDataJson = getItemFromJsonConfig(json_file,'enemySpawnData')
    for enemy in enemySpawnDataJson:
        enemy_type = int(enemy['enemyType'])
        spawn_y = int(enemy['spawn_y'])
        enemySpawnData = EnemySpawnData(enemy_type, spawn_y)
        enemySpawnDataList.append(enemySpawnData)
    return enemySpawnDataList

def getTowerInfosFromJson(json_file):
    towersData = getItemFromJsonConfig(json_file, 'towersData')
    for towerData in towersData:
        if towerData.get('tower_1') is not None:
            tower_1 = TowerAvailabilityData(1, int(towerData['tower_1']))
        if towerData.get('tower_2') is not None:
            tower_2 = TowerAvailabilityData(2, int(towerData['tower_2']))
        if towerData.get('tower_3') is not None:
            tower_3 = TowerAvailabilityData(3, int(towerData['tower_3']))
    towerDataList = [tower_1, tower_2, tower_3]
    return towerDataList

def getHealthFromJson(json_file):
    healthDataJson = getItemFromJsonConfig(json_file, 'health')
    return int(healthDataJson)

def getEnemyRouteFromJson(json_file):
    enemyPath = getItemFromJsonConfig(json_file, 'enemyPath')
    return enemyPath

def getTileMapFromJson(json_file):
    tileMap = getItemFromJsonConfig(json_file, 'tileMap')
    return tileMap

def getItemFromJsonConfig(json_file, data_string):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data[data_string]

def getAreaBlocks(tileMap):
    area_blocks = pygame.sprite.Group()
    for y, row in enumerate(tileMap):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x*w12(2), y*h12(2), w12(2), h12(2))
            block = AreaBlock(rect, AreaBlockType(tile), getBlockColor(tile))
            area_blocks.add(block)
    return area_blocks


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

class AreaBlockType(Enum):
    TOWER = 0
    ENEMY = 1

def getBlockColor(areaBlockType):
    #replace by GREEN_GRASS_DARK and GREEN_GRASS_LIGHT
    if(AreaBlockType(areaBlockType) == AreaBlockType.ENEMY):
        return NOTVERYBLACK1
    if(AreaBlockType(areaBlockType) == AreaBlockType.TOWER):
        return NOTVERYBLACK2
    
class EnemySpawnData:
    def __init__(self,enemyType, spawn_y):
        self.enemyType = enemyType
        self.spawn_y = spawn_y

class TowerAvailabilityData:
    def __init__(self,towerType, numberOfTower):
        self.towerType = towerType
        self.numberOf = numberOfTower

