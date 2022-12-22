import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 720, 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bullet Hell")

# Load the player and background images
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (64, 64))
background_image = pygame.image.load("space_4x.png")
# background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (64, 64))

# Set the scroll speed
bg_scroll_speed = 10

# Initialize the background position
bg_pos_y = 0

# Set up the player
player_rect = player_image.get_rect()
# player_rect.centerx = screen_width // 2
# player_rect.centery = screen_height - 50

# Set the player speed and hitbox size
player_speed = 5
player_hitbox_size = 32

# # Initialize the player position and hitbox
player_x = screen_width / 2
player_y = screen_height - player_hitbox_size
player_hitbox = pygame.Rect(player_x, player_y, player_hitbox_size, player_hitbox_size)


player_health = 100

# Set up the enemy
enemy_rect = enemy_image.get_rect()
enemy_rect.centerx = screen_width // 2
enemy_rect.centery = 50
enemy_health = 100
enemy_speed = 2

# Set up the bullets# Load the player bullet image
player_bullet_image = pygame.image.load("bullets/01.png")
player_bullet_image = pygame.transform.scale(player_bullet_image, (64, 64))
# bullet_image = pygame.Surface((10, 10))
bullet_image = pygame.Surface((64, 64), pygame.SRCALPHA)
bullet_image.blit(player_bullet_image, (0, 0))
# bullet_image.fill((255, 55, 255))
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

# Create the health bar rectangles
player_health_bar_rect = pygame.Rect(50, 50, player_health, 20)
enemy_health_bar_rect = pygame.Rect(screen_width - 50 - enemy_health, 50, enemy_health, 20)

# Set the health bar positions
player_health_bar_rect.midtop = (70, 50)
enemy_health_bar_rect.midtop = (screen_width - 70, 50)

# Set up the clock
clock = pygame.time.Clock()

# Game Message & effects
message = ("", (0, 0, 0), (255, 255, 255))

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
                bullet.centerx = player_x
                bullet.centery = player_y + 10
                bullets.append(bullet)

    # Check for player and enemy collisions
    if player_hitbox.colliderect(enemy_rect):
        player_health -= 10
        enemy_health -= 10

    for bullet in bullets:
        if enemy_rect.colliderect(bullet):
            bullets.remove(bullet)
            enemy_health -= 10

    for enemy_bullet in enemy_bullets:
        if player_hitbox.colliderect(enemy_bullet):
            enemy_bullets.remove(enemy_bullet)
            player_health -= 10

    # Update the health bar rectangles
    player_health_bar_rect.width = player_health
    enemy_health_bar_rect.width = enemy_health

    # Check if the player or enemy has died
    if player_health <= 0:
        message = ("Game Over!", (0, 0, 0), (255, 255, 255))
        # break
    # Check if the enemy has died
    if enemy_health <= 0:
        # Create the explosion animation
        message = ("You Win!", (0, 0, 0), (255, 255, 255))
        explosion_animation = []
        for i in range(44):
            filename = "explode{}.png".format(i)
            image = pygame.image.load(filename).convert_alpha()
            explosion_animation.append(image)

        # Play the explosion animation
        for image in explosion_animation:
            screen.blit(image, enemy_rect)
            pygame.display.flip()
            pygame.time.delay(100)

        # Remove the enemy from the game
        # enemies.remove(enemy)


    # Update the player position
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_hitbox.x -= player_speed
    if pressed_keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_hitbox.x += player_speed
    if pressed_keys[pygame.K_UP]:
        player_y -= player_speed
        player_hitbox.y -= player_speed
    if pressed_keys[pygame.K_DOWN]:
        player_y += player_speed
        player_hitbox.y += player_speed
    if pressed_keys[pygame.K_LCTRL]:
        player_speed = 3
        player_hitbox_size = 16
    elif pressed_keys[pygame.K_LSHIFT]:
        player_speed = 10
        player_hitbox_size = 50
    else:
        player_speed = 5
        player_hitbox_size = 32
    player_hitbox = pygame.Rect(player_x + player_rect.width/2 - player_hitbox_size/2, player_y + player_rect.height/2 - player_hitbox_size/2 , player_hitbox_size, player_hitbox_size)

    # Update the bullet positions
    for bullet in bullets:
        bullet.move_ip(0, -10)

    # Remove bullets that have left the screen
    bullets = [b for b in bullets if b.colliderect(screen.get_rect())]

    # Move the enemy
    enemy_rect.move_ip(enemy_speed, 0)

    # Check if the enemy has reached the edge of the screen
    if enemy_rect.right > screen_width or enemy_rect.left < 0:
        enemy_speed = -enemy_speed
        enemy_rect.move_ip(0, 50)

    # Check if the enemy should dodge a bullet
    for bullet in bullets:
        if abs(bullet.x - enemy_rect.x) < 50:
            enemy_rect.move_ip(0, random.uniform(-5, 5))

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

    # Update the background position
    bg_pos_y += bg_scroll_speed

    # Reset the background position if it has scrolled off the screen
    if bg_pos_y + background_image.get_height() >= screen_height + background_image.get_height():
        bg_pos_y = 0 - background_image.get_height()

    screen.blit(background_image, (0, bg_pos_y))
    screen.blit(background_image, (0, bg_pos_y  + background_image.get_height()))

    fill_surface = pygame.Surface((screen_width, screen_height))
    fill_surface.fill((0,0,0))
    fill_surface.set_alpha(180)
    # Draw the semi-opaque black fill
    screen.blit(fill_surface, (0, 0))
    # Draw the background
    # screen.blit(background_image, (0, 0))

    # Draw the player
    # screen.blit(player_image, player_rect)
    screen.blit(player_image, (player_x, player_y))
    pygame.draw.rect(screen, (200, 200, 200), player_hitbox, 2)

    # Draw the enemy
    screen.blit(enemy_image, enemy_rect)

    # Draw the health bar backgrounds
    pygame.draw.rect(screen, (255, 255, 255), player_health_bar_rect.inflate(4, 4))
    pygame.draw.rect(screen, (255, 255, 255), enemy_health_bar_rect.inflate(4, 4))

    # Draw the health bars
    pygame.draw.rect(screen, (20, 20, 220), player_health_bar_rect)
    pygame.draw.rect(screen, (255, 0, 0), enemy_health_bar_rect)

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

    # Render the message to the `screen
    font = pygame.font.Font(None, 60)

    # Render the outline
    outline_text = font.render(message[0], True, message[1])
    outline_rect = outline_text.get_rect()
    outline_rect.center = (screen_width // 2 - 1, 50 - 1)
    screen.blit(outline_text, outline_rect)
    outline_rect.center = (screen_width // 2 + 1, 50 - 1)
    screen.blit(outline_text, outline_rect)
    outline_rect.center = (screen_width // 2 - 1, 50 + 1)
    screen.blit(outline_text, outline_rect)
    outline_rect.center = (screen_width // 2 + 1, 50 + 1)
    screen.blit(outline_text, outline_rect)

    # Render the text
    text = font.render(message[0], True, message[2])
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, 50)
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
