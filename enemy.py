from enum import Enum
import json
import pygame
from pygame.locals import *
from settings import *
from utils import Direction, Position, TypeOfStep, w12

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.05, SCREEN_WIDTH*0.05))
        self.image.fill(RED)
        self.direction = Direction.DOWN
        self.health = 1
        self.route = [EnemyRouteStep(Position(w12(6), SCREEN_HEIGHT + 500, ), Direction.DOWN, True, TypeOfStep.ENTRY)]
        
    def update(self):
        for i, routeStep in enumerate(self.route):
            if(routeStep.is_active):

                if(routeStep.direction == Direction.DOWN):
                    if(routeStep.typeOfStep == TypeOfStep.EXIT):
                        self.rect.y = (self.rect.y + self.speed)
                    else:
                        if(self.rect.y <= routeStep.position.y):
                            self.rect.y = (self.rect.y + self.speed)
                        elif(self.rect.y > routeStep.position.y):
                            self.checkRoute(i)
                            break
                if(routeStep.direction == Direction.UP):
                    if(routeStep.typeOfStep == TypeOfStep.EXIT):
                        self.rect.y = (self.rect.y - self.speed)
                    else:
                        if (self.rect.y >= routeStep.position.y):
                            self.rect.y = (self.rect.y - self.speed)
                        elif (self.rect.y < routeStep.position.y):
                            self.checkRoute(i)
                            break
                if(routeStep.direction == Direction.RIGHT):
                    json_data = json.dumps([step.to_dict() for step in self.route], indent=4)
                    print("###########################################################################################################")
                    print("###########################################################################################################")
                    print("###########################################################################################################")
                    print("###########################################################################################################")
                    print(json_data)
                    if(routeStep.typeOfStep == TypeOfStep.EXIT):
                        self.rect.x = (self.rect.x + self.speed)
                    else:
                        if (self.rect.x <= routeStep.position.x):
                            self.rect.x = (self.rect.x + self.speed)
                        elif (self.rect.x > routeStep.position.x):
                            self.checkRoute(i)
                            break
                if(routeStep.direction == Direction.LEFT):
                    if(routeStep.typeOfStep == TypeOfStep.EXIT):
                        self.rect.x = (self.rect.x - self.speed)
                    else:
                        if(self.rect.x >= routeStep.position.x):
                            self.rect.x = (self.rect.x - self.speed)
                        elif (self.rect.x < routeStep.position.x):
                            self.checkRoute(i)
                            break
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def checkRoute(self, i):
        self.route[i].is_active = False
        if i + 1 < len(self.route) and self.route[i+1] is not None:
            self.route[i+1].is_active = True

class Enemy_Type_1(Enemy):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.02, SCREEN_WIDTH*0.02))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.health = ENEMY_TYPE_1_HEALTH
        self.max_health = ENEMY_TYPE_1_HEALTH
        self.damage = ENEMY_TYPE_1_DAMAGE
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Enemy_Type_2(Enemy):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.03, SCREEN_WIDTH*0.03))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 8
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.health = ENEMY_TYPE_2_HEALTH
        self.max_health = ENEMY_TYPE_2_HEALTH
        self.damage = ENEMY_TYPE_2_DAMAGE
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Enemy_Type_3(Enemy):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.04, SCREEN_WIDTH*0.04))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 10
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.health = ENEMY_TYPE_3_HEALTH
        self.max_health = ENEMY_TYPE_3_HEALTH
        self.damage = ENEMY_TYPE_3_DAMAGE
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class EnemyRouteStep():
    def __init__(self, position, direction, is_active, typeOfStep):
        self.position = position
        self.direction = direction
        self.is_active = is_active
        self.typeOfStep = typeOfStep
    def to_dict(self):
        return {
            "pos": f"{self.position.x},{self.position.y}",
            "dir": self.direction.name,
            "is_active": self.is_active,
            "typeOfStep": self.typeOfStep.name
        }


