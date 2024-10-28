import pygame, time, random
from player import Player
from missile import Missile
from enemy import Enemy
from missile_enemy import EnemyMissile

# Inicialización pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
width, height = 1050, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sky Guardians")

# Imagenes
background = pygame.image.load("assets/images/background.png")
background = pygame.transform.scale(background, (width, height))
heart = pygame.image.load("assets/images/heart.png")
heart= pygame.transform.scale(heart, (50, 50))
heart.set_colorkey((255, 255, 255))

# Sonidos
sonido_jugador = pygame.mixer.Sound("assets/tirPlayer.wav")
sonido_enemigo = pygame.mixer.Sound("assets/tirEnemy.wav")
sonido_golpe = pygame.mixer.Sound("assets/uuhhh.mp3")

# Fuentes
font = pygame.font.Font("assets/EuropeanTeletext.ttf", 74)
small_font = pygame.font.Font(None, 36)

# Temporizador para niveles
time_limit = 30
level1_duration = 30 * 1000

# Variables globales
enemy_shoot_interval = 2000
last_enemy_shot_time = pygame.time.get_ticks()
player_lives = 3

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Pantallas
def show_start_screen():
    screen.blit(background, (0, 0))
    draw_text('Sky Guardians', font, (255, 255, 255), screen, width // 2, height // 2 - 50)
    draw_text('Pulsa ENTER para iniciar', small_font, (255, 255, 255), screen, width // 2, height // 2 + 50)
    pygame.display.flip()

    pygame.mixer.music.load("assets/menu.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False



def show_game_over_screen():
    screen.blit(background, (0, 0))
    draw_text('¡Game Over!', font, (255, 0, 0), screen, width // 2, height // 2 - 50)
    draw_text('Pulsa ENTER para reiniciar', small_font, (255, 255, 255), screen, width // 2, height // 2 + 50)
    pygame.display.flip()
    pygame.mixer.music.load("assets/gameOver.mp3")
    pygame.mixer.music.play(0)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def show_level_completed_screen():
    screen.blit(background, (0, 0))
    draw_text('¡Nivel Conseguido!', font, (0, 255, 0), screen, width // 2, height // 2 - 50)  # Texto en verde
    draw_text('Pulsa ENTER para continuar', small_font, (255, 255, 255), screen, width // 2, height // 2 + 50)
    pygame.display.flip()

    pygame.mixer.music.load("assets/levelCompleted.mp3")
    pygame.mixer.music.play(0)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def reset_game():
    # Crear y configurar los objetos del juego de nuevo
    global player, missiles, enemies, start_time, tiempo_misil, missiles_enemy, enemy_shoot_interval, last_enemy_shot_time, player_lives
    player = Player(width // 2, height)
    missiles = pygame.sprite.Group()
    missiles_enemy = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    start_time = pygame.time.get_ticks()
    tiempo_misil = time.time()
    enemy_shoot_interval = 2000
    last_enemy_shot_time = pygame.time.get_ticks()
    player_lives = 3

def draw_lives(screen, lives, image):
    for i in range(lives):
        screen.blit(image, (10 + i * 40, 10))

def main_game():
    global start_time, tiempo_misil, last_enemy_shot_time, player_lives, heart
    reset_game()
    start_time = pygame.time.get_ticks()
    running = True
    game_over = False

    pygame.mixer.music.load("assets/battle.wav")
    pygame.mixer.music.play(-1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Actualización jugador
        player.update()

        # Disparo de misiles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if time.time() - tiempo_misil > 0.3:
                missile = Missile(player.rect.centerx, player.rect.top)
                missiles.add(missile)
                sonido_jugador.play()
                tiempo_misil = time.time()

        # Disparo aleatorio de enemigos
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_shot_time > enemy_shoot_interval:
            if len(enemies) > 0:
                random_enemy = random.choice(enemies.sprites())  # Elegir enemigo aleatorio
                enemy_missile = EnemyMissile(random_enemy.rect.centerx, random_enemy.rect.bottom)
                missiles_enemy.add(enemy_missile)
                sonido_enemigo.play()
                last_enemy_shot_time = current_time

        # Actualización misiles
        missiles.update()
        missiles_enemy.update()

        # Generar enemigos durante el primer nivel
        if pygame.time.get_ticks() - start_time < level1_duration:
            if random.randint(1, 50) == 1:
                new_enemy = Enemy()
                enemies.add(new_enemy)

        # Actualización enemigos
        enemies.update()

        # Verificar si algún enemigo ha alcanzado el borde inferior
        for enemy in enemies:
            if enemy.rect.bottom >= height:
                game_over = True

        # Detección de colisiones entre misiles y enemigos
        for missile in missiles:
            hits = pygame.sprite.spritecollide(missile, enemies, True)
            if hits:
                missile.kill()

        # Colisiones entre misiles enemigos y el jugador
        if pygame.sprite.spritecollide(player, missiles_enemy, True):
            player.hit()
            player_lives -= 1
            sonido_golpe.play()
            if player_lives <= 0:
                game_over = True

        # Calcular el tiempo transcurrido
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, time_limit - elapsed_time)

        # Dibujo de pantalla
        screen.blit(background, (0, 0))
        screen.blit(player.image, player.rect)
        missiles.draw(screen)
        enemies.draw(screen)
        missiles_enemy.draw(screen)

        # Dibujar el temporizador y vidas
        timer_text = small_font.render(f'Tiempo: {int(remaining_time)}s', True, (255, 255, 255))
        screen.blit(timer_text, (900, 10))
        draw_lives(screen, player_lives, heart)

        # Actualización pantalla
        pygame.display.flip()

        # Verificar si el tiempo se ha agotado
        if remaining_time <= 0:
            show_level_completed_screen()
            running = False
        if game_over:
            show_game_over_screen()
            running = False

show_start_screen()
while True:
    main_game()