import pygame
import sys

# def tick_sim():


# Initialize Pygame 
pygame.init()

# Set up the display surface 
screen = pygame.display.set_mode((500, 500))

# Set up the clock
clock = pygame.time.Clock()

# Circle properties
circle_x = 250 
circle_y = 250
circle_radius = 50
circle_color = (0, 0, 255)

# Circle velocity
circle_vx = 0
circle_vy = 0

# Main game loop
running = True 
while running:

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keyboard input    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("LEFTU")
                circle_vx = -5
            elif event.key == pygame.K_RIGHT:
                circle_vx = 5   
            elif event.key == pygame.K_UP:
                circle_vy = -5
            elif event.key == pygame.K_DOWN:
                circle_vy = 5
        
        # Reset velocity on key release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pass
                # circle_vx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                pass
                # circle_vy = 0

    # Update circle position
    circle_x += circle_vx
    circle_y += circle_vy

    circle_vx *= 0.9
    circle_vy *= 0.9

    # Bounce off edges
    if circle_x < 0 or circle_x > 500:
        circle_vx = -circle_vx
    if circle_y < 0 or circle_y > 500:
        circle_vy = -circle_vy

    # Draw background
    screen.fill((255, 255, 255))

    # Draw circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # Update display
    pygame.display.update()

    # Tick clock
    clock.tick(60)

pygame.quit()