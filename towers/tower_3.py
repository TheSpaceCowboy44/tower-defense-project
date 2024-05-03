import pygame
from pygame.locals import *
from constants import *
from utils import *

class Tower_3(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TOWER_1_SIZE, TOWER_1_SIZE))
        self.image.fill(GREEN)  # Couleur de la nouvelle tour
        self.rect = self.image.get_rect(center=(x, y))
        self.highlight_detection_circle = False
        self.laser_active = False  # Indique si le laser est actif
        self.laser_timer = pygame.time.get_ticks() + 1000  # Initialisation du timer
        self.laser_duration = 1000  # Durée d'activation du laser en millisecondes
        self.laser_cooldown = 1000  # Temps de recharge du laser en millisecondes

    def update(self, enemies, player):
        now = pygame.time.get_ticks()

        # Vérifie si un ennemi est détecté
        enemy_detected = check_collision_group_circle(self, enemies, TOWER_1_DETECTION_RADIUS)
        if enemy_detected:
            self.highlight_detection_circle = True
            # Active le laser si le timer est écoulé et le laser n'est pas déjà actif
            if now > self.laser_timer and not self.laser_active:
                self.laser_active = True
                self.laser_timer = now + self.laser_cooldown  # Démarre le timer de recharge

        else:
            self.highlight_detection_circle = False

        # Désactive le laser après la durée spécifiée
        if self.laser_active and now < self.laser_timer:
            self.draw_laser()  # Affiche le laser

    def draw_laser(self):
        # Affiche une ligne horizontale jaune en dessous de la tour
        laser_width = 100  # Largeur du laser
        laser_height = 2  # Hauteur du laser
        laser_color = YELLOW  # Couleur du laser
        laser_rect = pygame.Rect(self.rect.centerx - laser_width // 2, self.rect.bottom, laser_width, laser_height)
        pygame.draw.rect(screen, laser_color, laser_rect)

    def draw(self, surface):
        if self.highlight_detection_circle:
            circle_center = (self.rect.centerx, self.rect.centery)
            pygame.draw.circle(surface, GREEN, circle_center, TOWER_1_DETECTION_RADIUS, 2)


