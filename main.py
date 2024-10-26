import pygame, time, random
from player import Player
from missile import Missile
from enemy import Enemy
from missile_enemy import EnemyMissile

# Inicialización pygame
pygame.init()

# Configuración de la pantalla
width, height = 1050, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sky Guardians")

background = pygame.image.load("assets/images/background.png")
background = pygame.transform.scale(background, (width, height))

# Fuentes
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Temporizador para niveles
time_limit = 30
level1_duration = 30 * 1000

# Variables globales
enemy_shoot_interval = 2000
last_enemy_shot_time = pygame.time.get_ticks()

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
    global player, missiles, enemies, start_time, tiempo_misil, missiles_enemy, enemy_shoot_interval, last_enemy_shot_time
    player = Player(width // 2, height)             # Reiniciar posición del jugador
    missiles = pygame.sprite.Group()                # Vaciar el grupo de misiles
    missiles_enemy = pygame.sprite.Group()          # Vaciar el grupo de misiles
    enemies = pygame.sprite.Group()                 # Vaciar el grupo de enemigos
    start_time = pygame.time.get_ticks()            # Reiniciar el temporizador
    tiempo_misil = time.time()                      # Reiniciar el tiempo para los misiles
    enemy_shoot_interval = 2000                     # Reiniciar intervalo de disparo enemigo
    last_enemy_shot_time = pygame.time.get_ticks()  # Reiniciar tiempo del último disparo enemigo

def main_game():
    global start_time, tiempo_misil, last_enemy_shot_time
    reset_game()
    start_time = pygame.time.get_ticks()
    running = True
    game_over = False

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
                tiempo_misil = time.time()

        # Disparo aleatorio de enemigos
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_shot_time > enemy_shoot_interval:
            if len(enemies) > 0:
                random_enemy = random.choice(enemies.sprites())  # Elegir enemigo aleatorio
                enemy_missile = EnemyMissile(random_enemy.rect.centerx, random_enemy.rect.bottom)
                missiles_enemy.add(enemy_missile)
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

        # Dibujar el temporizador
        timer_text = small_font.render(f'Tiempo: {int(remaining_time)}s', True, (255, 255, 255))
        screen.blit(timer_text, (900, 10))

        # Actualización pantalla
        pygame.display.flip()

        # Verificar si el tiempo se ha agotado
        if remaining_time <= 0 or game_over:
            show_game_over_screen()
            running = False

show_start_screen()
while True:
    main_game()