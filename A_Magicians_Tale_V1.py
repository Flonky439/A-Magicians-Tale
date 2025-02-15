import pygame
import math
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Magician's Tale")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 223, 0)

player_speed = 5
magica_speed = 6
enemy_speed = 4

player_health = 100
max_health = 100
coin_count = 0  

last_heal_time = 0
healing_cooldown = 30000  # 30 seconds

font = pygame.font.Font(None, 36)

# Load high score from file
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read().strip())
        except ValueError:
            high_score = 0

Player = pygame.Rect(400, 400, 20, 20)
Magica = pygame.Rect(400, 380, 20, 3)

enemy_count = 5
enemies = []
coins = []  

respawn_time = None

def spawn_enemies():
    """Respawn enemies at random positions."""
    global enemies
    enemies = []
    for _ in range(enemy_count):
        x = random.randint(0, WIDTH - 30)
        y = random.randint(0, HEIGHT - 30)
        enemy_rect = pygame.Rect(x, y, 30, 30)
        enemies.append({'rect': enemy_rect, 'health': 100})

spawn_enemies()

running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and Player.left > 0:
        Player.x -= player_speed
    if keys[pygame.K_d] and Player.right < WIDTH:
        Player.x += player_speed
    if keys[pygame.K_w] and Player.top > 0:
        Player.y -= player_speed
    if keys[pygame.K_s] and Player.bottom < HEIGHT:
        Player.y += player_speed

    if keys[pygame.K_LEFT] and Magica.left > 0:
        Magica.x -= magica_speed
    if keys[pygame.K_RIGHT] and Magica.right < WIDTH:
        Magica.x += magica_speed
    if keys[pygame.K_UP] and Magica.top > 0:
        Magica.y -= magica_speed
    if keys[pygame.K_DOWN] and Magica.bottom < HEIGHT:
        Magica.y += magica_speed
    
    if keys[pygame.K_1] and player_health < max_health and coin_count > 1:
        coin_count -= 1
        player_health += 5

        

    for enemy in enemies[:]:  
        dx = Player.x - enemy['rect'].x
        dy = Player.y - enemy['rect'].y
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            enemy['rect'].x += (dx / distance) * enemy_speed
            enemy['rect'].y += (dy / distance) * enemy_speed

        if Player.colliderect(enemy['rect']):
            player_health -= 1
            if player_health < 0:
                player_health = 0

        if Magica.colliderect(enemy['rect']):
            enemy['health'] -= 2
            if enemy['health'] <= 0:
                coins.append(pygame.Rect(enemy['rect'].x + 10, enemy['rect'].y + 10, 10, 10))  
                enemies.remove(enemy)  

    for coin in coins[:]:
        if Player.colliderect(coin):  
            coins.remove(coin)
            coin_count += 1

    if not enemies and respawn_time is None:
        respawn_time = pygame.time.get_ticks() + 5000

    if respawn_time and pygame.time.get_ticks() >= respawn_time:
        spawn_enemies()
        respawn_time = None  

    if player_health == 0:
        running = False

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, Player)
    pygame.draw.rect(screen, GREY, Magica)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy['rect'])
        health_ratio = enemy['health'] / 100
        pygame.draw.rect(screen, RED, (enemy['rect'].x, enemy['rect'].y - 10, 30, 5))
        pygame.draw.rect(screen, GREEN, (enemy['rect'].x, enemy['rect'].y - 10, 30 * health_ratio, 5))

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin.x + 5, coin.y + 5), 5)  

    pygame.draw.rect(screen, RED, (20, 20, 100, 10))
    pygame.draw.rect(screen, GREEN, (20, 20, 100 * (player_health / max_health), 10))


    coin_text = font.render(f"Coins: {coin_count}", True, WHITE)
    screen.blit(coin_text, (WIDTH - 120, 20))  


    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 20))

    if coin_count >= 50:
        Win_text = font.render("YOU WIN", True, GREEN)
        text_rect = Win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(Win_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False 

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

if coin_count > high_score:
    with open("highscore.txt", "w") as f:
        f.write(str(coin_count))
