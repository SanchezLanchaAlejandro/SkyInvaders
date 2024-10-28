import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.image = pygame.image.load("assets/images/player.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 9

        # Variables para la sacudida
        self.is_shaking = False
        self.shake_duration = 300  # Duración de la sacudida en milisegundos
        self.shake_time = 0
        self.original_position = (x, y)  # Posición original del jugador

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

        if self.is_shaking:
            current_time = pygame.time.get_ticks()
            if current_time - self.shake_time < self.shake_duration:
                # Sacudir el jugador hacia la izquierda y derecha
                shake_offset = 10 * ((current_time // 50) % 2)  # Cambia entre 0 y 10
                self.rect.x = self.original_position[0] - shake_offset
            else:
                # Finalizar la sacudida y restablecer la posición
                self.is_shaking = False
                self.rect.x = self.original_position[0]

    def hit(self):
        self.is_shaking = True
        self.shake_time = pygame.time.get_ticks()  # Reiniciar el tiempo de sacudida
        self.original_position = (self.rect.x, self.rect.y)

