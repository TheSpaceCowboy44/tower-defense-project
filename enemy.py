from enum import Enum
import json
import pygame
from pygame.locals import *
from settings import *
from utils import Direction, Position, TypeOfStep, h12, w12

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH*0.05, SCREEN_WIDTH*0.05))
        self.image.fill(RED)
        self.direction = Direction.DOWN
        self.health = 1
        self.route = [EnemyRouteStep(Position(w12(6), SCREEN_HEIGHT + 500 ), Direction.DOWN, True, TypeOfStep.ENTRY)]
        
    def update(self):
        for i, routeStep in enumerate(self.route):
            if(routeStep.is_active):
                if(routeStep.typeOfStep == TypeOfStep.EXIT):
                    self.moveInDirection(routeStep.direction)
                else:
                    if(checkEnemyRouteCollision(self, routeStep) ):
                        self.checkRoute(i, i+6)
                        displayCurrentRouteSteps(self.route)
                        break
                    else:
                        self.moveInDirection(routeStep.direction)
                
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def checkRoute(self, i, nextStepIndex):
        if self.route[i].typeOfStep != TypeOfStep.EXIT:
            self.route[i].is_active = False
            if(nextStepIndex is not None):
                self.route[nextStepIndex].is_active = True
    def moveInDirection(self, direction):
        if(direction == Direction.DOWN):
            self.rect.y = (self.rect.y + self.speed)
        if(direction == Direction.UP):
            self.rect.y = (self.rect.y - self.speed)
        if(direction == Direction.RIGHT):
            self.rect.x = (self.rect.x + self.speed)
        if(direction == Direction.LEFT):
            self.rect.x = (self.rect.x - self.speed)


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


def checkEnemyRouteCollision(enemy, routeStep):
    check_x_axis = enemy.rect.x > (routeStep.position.x + ENEMY_PATH_SPACE_DELIMITER) and enemy.rect.x < (routeStep.position.x + w12(2) - ENEMY_PATH_SPACE_DELIMITER)
    check_y_axis = enemy.rect.y > (routeStep.position.y + ENEMY_PATH_SPACE_DELIMITER) and enemy.rect.y < (routeStep.position.y + h12(2) - ENEMY_PATH_SPACE_DELIMITER)
    if(check_x_axis and check_y_axis):
        return True
    else:
        return False
        
def displayCurrentRouteSteps(steps):
    for step in steps:
        if((steps.index(step)+1) % 6 == 1 and steps.index(step) != 0):
            print("")
        if(step.direction == Direction.RIGHT):
            if(step.is_active):
                print('► ', end='')
            else:
                print("→ ", end='')
        elif(step.direction == Direction.LEFT):
            if(step.is_active):
                print("◄ ", end='')
            else:
                print("🠔", end='')
        elif(step.direction == Direction.UP):
            if(step.is_active):
                print("▲ ", end='')
            else:
                print("🠕", end='')
        elif(step.direction == Direction.DOWN):
            if(step.is_active):
                print("▼ ", end='')
            else:
                print("🠗", end='')
    print("\n")