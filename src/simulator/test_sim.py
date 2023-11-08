import pygame
import sys
from math import sin, cos, radians

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

circle_angle = 0
circle_vx = 0
circle_vy = 0

# Main game loop
running = True 
while running:
    # Check for quit event
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_LEFT]:
        circle_angle += 5
    if keys[pygame.K_RIGHT]:
        circle_angle -= 5
    if keys[pygame.K_UP]:
        circle_vx = 5 * cos(radians(circle_angle))
        circle_vy = -5 * sin(radians(circle_angle))
    if keys[pygame.K_DOWN]:
        circle_vx = -5 * cos(radians(circle_angle))
        circle_vy = 5 * sin(radians(circle_angle))

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

    line_x = circle_x + circle_radius * cos(radians(circle_angle))
    line_y = circle_y - circle_radius * sin(radians(circle_angle))
    pygame.draw.line(screen, (0,0,0), (circle_x, circle_y), (line_x, line_y))

    # Update display
    pygame.display.update()

    # Tick clock
    clock.tick(60)

pygame.quit()