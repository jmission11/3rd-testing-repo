import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

def init_game():
    # Player
    player = pygame.Rect(WIDTH // 2, HEIGHT - 50, 40, 40)
    
    # Coins
    coins = []
    for _ in range(5):
        coin = pygame.Rect(random.randint(0, WIDTH-20), random.randint(0, HEIGHT-20), 20, 20)
        coins.append(coin)

    # Obstacles
    obstacles = []
    for _ in range(3):
        obstacle = pygame.Rect(random.randint(0, WIDTH-30), random.randint(0, HEIGHT-30), 30, 30)
        obstacles.append(obstacle)

    return player, coins, obstacles, 0, False  # Returns player, coins, obstacles, score, game_over

# Initialize game objects
player, coins, obstacles, score, game_over = init_game()
player_speed = 5

# Create restart button
restart_button = pygame.Rect(WIDTH//2 - 60, HEIGHT//2 + 50, 120, 40)

# Game variables
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if game_over and restart_button.collidepoint(mouse_pos):
                # Reset the game
                player, coins, obstacles, score, game_over = init_game()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += player_speed

        # Coin collection
        for coin in coins[:]:
            if player.colliderect(coin):
                coins.remove(coin)
                score += 1
                new_coin = pygame.Rect(random.randint(0, WIDTH-20), 
                                     random.randint(0, HEIGHT-20), 20, 20)
                coins.append(new_coin)

        # Obstacle collision
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                game_over = True

    # Drawing
    screen.fill(WHITE)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, player)
    
    # Draw coins
    for coin in coins:
        pygame.draw.rect(screen, YELLOW, coin)
    
    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Game over message and restart button
    if game_over:
        game_over_text = font.render('Game Over!', True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))

        pygame.draw.rect(screen, GREEN, restart_button)
        restart_text = font.render('Restart', True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - 40, HEIGHT//2 + 60))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
