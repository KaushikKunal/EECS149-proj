import pygame

# Initialize Pygame 
pygame.init()

# Set up the display surface 
screen = pygame.display.set_mode((500, 500))

# Set up the clock
clock = pygame.time.Clock() 

# Define circle properties
circle_x = 250
circle_y = 250
circle_radius = 50
circle_color = (0, 0, 255) 

# Main game loop
running = True
while running:

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw background
    screen.fill((255, 255, 255))

    # Draw circle
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

    # Update the display
    pygame.display.update()

    # Tick the clock
    clock.tick(60)

pygame.quit()