import pygame

class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/images/enemy_missile.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.rect.width += 10
        self.rect = self.rect.inflate(10, 0)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.kill()  # Si el misil sale de la pantalla, se elimina