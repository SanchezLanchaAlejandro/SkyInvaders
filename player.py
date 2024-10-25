import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.image = pygame.image.load("assets/images/player.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 9

    def update(self): # Funcion para mover el personaje
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed     # Teclas de movimiento
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1050:  # Limites de la pantalla
            self.rect.right = 1050

        self.rect.y = 800 - self.rect.height - 10 # Posición en la pantalla

