import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        player_width = 99
        self.rect.x = random.randint(player_width // 2, 1050 - (player_width // 2 + self.rect.width))  # Posición aleatoria en X
        self.rect.y = random.randint(-100, -40)  # Aparece fuera de la pantalla
        self.speed = random.randint(1, 5)  # Aumentamos la velocidad mínima

    def update(self):
        self.rect.y += self.speed  # Mover el enemigo hacia abajo

        # Verificar si el enemigo ha llegado a la parte inferior de la pantalla
        if self.rect.bottom >= 875:
            return True  
        return False