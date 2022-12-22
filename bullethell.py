import sys
import random
import pygame

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width = 640
screen_height = 480

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the player image
player_image = pygame.image.load("player.png")

# Get the player size and position
player_rect = player_image.get_rect()
player_x = player_rect.centerx
player_y = screen_height - player_rect.height
player_width = 64
player_height = 64
# Set the player speed
player_speed = 5

# Set the player bullet size and speed
player_bullet_width = 10
player_bullet_height = 10
player_bullet_speed = 10

# Load the player bullet image
player_bullet_image = pygame.image.load("bullets/01.png")

# Create a surface for the player's bullet
player_bullet_surface = pygame.Surface((player_bullet_width, player_bullet_height), pygame.SRCALPHA)
player_bullet_surface.blit(player_bullet_image, (0, 0))

# Create a tuple with the player's bullet position and size
player_bullet = (player_x, player_y, player_bullet_width, player_bullet_height)

# Set the enemy size and speed
enemy_width = 50
enemy_height = 50
enemy_speed = 5

# Load the enemy image
enemy_image = pygame.image.load("enemy.png")

# Create a surface for the enemy
enemy_surface = pygame.Surface((enemy_width, enemy_height), pygame.SRCALPHA)
enemy_surface.blit(enemy_image, (0, 0))

# Initialize the enemy position
enemy_x = 0
enemy_y = 0

# Create a tuple with the enemy position and size
# enemy_rect = (random.uniform(0, screen_width - enemy_width), 0, enemy_width, enemy_height)

# Set the enemy bullet size and speed
enemy_bullet_width = 10
enemy_bullet_height = 10
enemy_bullet_speed = 10

# Set the enemy shooting rate
enemy_shooting_rate = 1000  # 1 second

# Initialize the enemy shooting timer
enemy_shooting_timer = pygame.time.get_ticks()

# Set the player and enemy health
player_health = 100
enemy_health = 100

# Set the player and enemy damage
player_damage = 10
enemy_damage = 10

# Set the screen shake duration and intensity
shake_duration = 1000  # Shake for 1 second
shake_intensity = 10  # Shake intensity of 10 pixels

# Create a surface for the screen buffer
screen_buffer = pygame.Surface((screen_width, screen_height))

# Set the font and message
font = pygame.font.Font(None, 36)
message = None
# Initialize the start_shake variable
start_shake = 0
# Initialize the player and enemy rectangles
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

# Game loop
while True:
    # Check if the player has been hit
    if player_health <= 0:
        message = ("Game Over!", (0, 0, 0), (255, 255, 255))
        # Start the screen shake
        start_shake = pygame.time.get_ticks()
        print("Player hit! start_shake =", start_shake)  # Debugging line

    # Check if the enemy has been hit
    if enemy_health <= 0:
        message = ("You Win!", (0, 0, 0), (255, 255, 255))
        start_shake = pygame.time.get_ticks()
        print("Enemy hit! start_shake =", start_shake)  # Debugging line

    # Check if the screen should be shaking
    if pygame.time.get_ticks() - start_shake < shake_duration:
        # Calculate the shake offset
        shake_offset_x = random.uniform(-shake_intensity, shake_intensity)
        shake_offset_y = random.uniform(-shake_intensity, shake_intensity)

        # Scroll the screen buffer with the shake offset
        screen_buffer.scroll(int(shake_offset_x), int(shake_offset_y))

    # Clear the screen buffer
    screen_buffer.fill((255, 255, 255))

    # Update the player position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    player_rect.centerx = player_x

    # Update the player bullet position
    player_bullet = (player_bullet[0], player_bullet[1] - player_bullet_speed)

    # Update the enemy position
    enemy_rect = (enemy_rect[0], enemy_rect[1] + enemy_speed)

    # Update the enemy shooting timer
    if pygame.time.get_ticks() - enemy_shooting_timer > enemy_shooting_rate:
        enemy_shooting_timer = pygame.time.get_ticks()

    # Draw the player on the screen
    screen_buffer.blit(player_image, player_rect)

    # Draw the player's bullet on the screen
    screen_buffer.blit(player_bullet_surface, player_bullet)

    # Draw the enemy on the screen
    screen_buffer.blit(enemy_surface, enemy_rect)

    # Check for collisions
    # if player_rect.colliderect(enemy_rect):
    #     # Decrease the player health
    #     player_health -= enemy_damage
    #     print("Player hit! player_health =", player_health)  # Debugging line
    if player_bullet[1] <= 0:
        # Decrease the enemy health
        enemy_health -= player_damage
        print("Enemy hit! enemy_health =", enemy_health)  # Debugging line

    # Apply the postprocessing effects to the screen buffer
    # screen_buffer = pygfx.apply_gfx(screen_buffer, "CRT")

    # Blit the screen buffer to the screen
    screen.blit(screen_buffer, (0, 0))

    # Update the display
    pygame.display.flip()

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Update the player bullet position
                player_bullet = (player_x, player_y, player_bullet_width, player_bullet_height)

