import pygame

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/player_missile.png").convert_alpha()  # Imagen
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10  # Velocidad del misil
        self.rect.width += 10  # Incrementa la anchura del área de colisión
        self.rect = self.rect.inflate(10, 0)  # Añade 15 píxeles a cada lado

    def update(self):
        self.rect.y -= self.speed  # Movimiento hacia arriba
        if self.rect.bottom < 0:   # Eliminar misil cuando salga de la pantalla
            self.kill()

