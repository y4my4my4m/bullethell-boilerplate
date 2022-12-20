import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 768, 1024
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bullet Hell")

# Load the player and background images
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (64, 64))
background_image = pygame.image.load("space2.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (64, 64))

# Set up the player
player_rect = player_image.get_rect()
player_rect.centerx = screen_width // 2
player_rect.centery = screen_height - 50

# Set up the enemy
enemy_rect = enemy_image.get_rect()
enemy_rect.centerx = screen_width // 2
enemy_rect.centery = 50

# Set up the bullets
bullet_image = pygame.Surface((10, 10))
bullet_image.fill((255, 55, 255))
bullets = []

# Set up the enemy bullets
enemy_bullet_image = pygame.Surface((5, 5))
enemy_bullet_image.fill((255, 0, 0))
enemy_bullets = []

# Set up the enemy bullet colors
enemy_bullet_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
enemy_bullet_color_index = 0

# Set up the enemy bullet sizes
enemy_bullet_sizes = [5, 10, 15]
enemy_bullet_size_index = 0

# Set up the enemy bullet trail
enemy_bullet_trail_image = pygame.Surface((5, 5))
enemy_bullet_trail_image.fill((255, 255, 255))
enemy_bullet_trails = []
# Set up the enemy bullet trail alpha values
enemy_bullet_trail_alphas = [255, 200, 150, 100, 50, 0]
enemy_bullet_trail_alpha_index = 0
# Initialize the enemy bullet trail data list
enemy_bullet_trail_data = []

# Set up the enemy shooting timer
enemy_shoot_timer = 0
enemy_shoot_delay = 1000 # Shoot every 1000 milliseconds

# Set up the clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire a bullet
                bullet = bullet_image.get_rect()
                bullet.centerx = player_rect.centerx
                bullet.centery = player_rect.centery + 10
                bullets.append(bullet)

    # Update the player position
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        player_rect.move_ip(-5, 0)
    if pressed_keys[pygame.K_RIGHT]:
        player_rect.move_ip(5, 0)
    if pressed_keys[pygame.K_UP]:
        player_rect.move_ip(0, -3)
    if pressed_keys[pygame.K_DOWN]:
        player_rect.move_ip(0, 3)

    # Update the bullet positions
    for bullet in bullets:
        bullet.move_ip(0, -10)

    # Remove bullets that have left the screen
    bullets = [b for b in bullets if b.colliderect(screen.get_rect())]

    # Update the enemy position
    enemy_rect.move_ip(random.uniform(-1, 1), 0)

    # Update the enemy shooting timer
    enemy_shoot_timer += clock.get_time()
    if enemy_shoot_timer > enemy_shoot_delay:
        # Reset the timer
        enemy_shoot_timer = 0

        # Fire a spread of bullets
        spread = 10 # Degrees
        for i in range(-spread // 2, spread // 2 + 1):
            angle = i * (360 / spread)
            dx, dy = pygame.math.Vector2(1, 0).rotate(angle)
            enemy_bullet = enemy_bullet_image.get_rect()
            enemy_bullet.centerx = enemy_rect.centerx + dx * 25
            enemy_bullet.centery = enemy_rect.centery + dy * 25
            enemy_bullets.append(enemy_bullet)
            # Initialize the enemy bullet trail alpha values and alpha index
            enemy_bullet_trail_alpha_values = enemy_bullet_trail_alphas
            enemy_bullet_trail_alpha_index = 0
            enemy_bullet_trail_alpha = enemy_bullet_trail_alpha_values[enemy_bullet_trail_alpha_index]
            enemy_bullet_trail_info = (enemy_bullet_trail_alpha_values, enemy_bullet_trail_alpha_index, enemy_bullet_trail_alpha)
            enemy_bullet_trail_data.append(enemy_bullet_trail_info)

    for enemy_bullet in enemy_bullets:
        enemy_bullet.move_ip(0, 5)
        # Change the direction of the bullet every 500 milliseconds
        if clock.get_time() > 15:
            # Calculate the angle from the center of the spread to the bullet
            angle = math.atan2(enemy_bullet.centery - enemy_rect.centery, enemy_bullet.centerx - enemy_rect.centerx)
            # Expand the bullet outward
            # enemy_bullet.move_ip(math.cos(angle) * 10, math.sin(angle) * 10)
            enemy_bullet.move_ip(math.cos(angle) * random.uniform(5, 15), math.sin(angle) * random.uniform(5, 15))
            # Add a trail to the bullet
            trail = enemy_bullet_trail_image.get_rect()
            trail.centerx = enemy_bullet.centerx
            trail.centery = enemy_bullet.centery
            enemy_bullet_trails.append(trail)

    # Update the enemy bullet trail positions, alpha values, and alpha indices
    for i, enemy_bullet_trail in enumerate(enemy_bullet_trails):
        enemy_bullet_trail.move_ip(0, 10)
        # Check if the index is within the bounds of the enemy_bullet_trail_data list
        if i < len(enemy_bullet_trail_data):
            enemy_bullet_trail_info = enemy_bullet_trail_data[i]
            enemy_bullet_trail_alpha_values = enemy_bullet_trail_info[0]
            enemy_bullet_trail_alpha_index = enemy_bullet_trail_info[1]
            enemy_bullet_trail_alpha = enemy_bullet_trail_info[2]
            # Fade the bullet trail alpha value
            enemy_bullet_trail_alpha_index += 1
            if enemy_bullet_trail_alpha_index >= len(enemy_bullet_trail_alpha_values):
                enemy_bullet_trail_alpha_index = 0
            enemy_bullet_trail_alpha = enemy_bullet_trail_alpha_values[enemy_bullet_trail_alpha_index]
            # Remove the bullet trail if its alpha value is zero
            if enemy_bullet_trail_alpha <= 0:
                enemy_bullet_trails.pop(i)
                enemy_bullet_trail_data.pop(i)
                continue
            enemy_bullet_trail_info = (enemy_bullet_trail_alpha_values, enemy_bullet_trail_alpha_index, enemy_bullet_trail_alpha)
            enemy_bullet_trail_data[i] = enemy_bullet_trail_info
        else:
            # Skip this enemy bullet trail
            continue

        # Create the enemy bullet trail image with the new alpha value
        enemy_bullet_trail_image = pygame.Surface((5, 5))
        enemy_bullet_trail_image.set_colorkey((0, 0, 0))
        enemy_bullet_trail_image.set_alpha(enemy_bullet_trail_alpha)
        enemy_bullet_trail_image.fill((255, 255, 255))

    # Remove enemy bullets that have left the screen
    enemy_bullets = [b for b in enemy_bullets if b.colliderect(screen.get_rect())]

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the player
    screen.blit(player_image, player_rect)

    # Draw the enemy
    screen.blit(enemy_image, enemy_rect)

    # Draw the bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)
    for enemy_bullet in enemy_bullets:
        # Flash the bullet color
        enemy_bullet_color_index += 1
        if enemy_bullet_color_index >= len(enemy_bullet_colors):
            enemy_bullet_color_index = 0
        enemy_bullet_color = enemy_bullet_colors[enemy_bullet_color_index]
        pygame.draw.circle(screen, enemy_bullet_color, enemy_bullet.center, 5)
    for enemy_bullet_trail in enemy_bullet_trails:
        # Draw the bullet trail
        screen.blit(enemy_bullet_trail_image, enemy_bullet_trail)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
