import pygame
import sys
from math import *

# def tick_sim():


# Initialize Pygame 
pygame.init()

# Set up the display surface 
screen = pygame.display.set_mode((500, 500))

# Set up the clock
clock = pygame.time.Clock()

# get the direction from x1, y1 to x2, y2
def get_dir_to(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return degrees(-atan2(dy, dx))

# get the distance from x1, y1 to x2, y2
def get_dist_to(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx**2 + dy**2)

class Pololu:
    def __init__(self, x, y, radius, color):
        self.x = x 
        self.y = y
        self.vel = 0
        self.ang = 0  # degrees
        self.acc = 0
        self.ang_acc = 0  # degrees per second

        self.radius = radius
        self.color = color

    def physics_update(self):
        self.ang += self.ang_acc
        self.vel += self.acc

        self.x += self.vel * cos(radians(self.ang))
        self.y -= self.vel * sin(radians(self.ang))

        self.acc = 0
        self.ang_acc = 0

        # friction
        self.vel *= 0.95

        # # Bounce off edges
        # if circle_x < 0 or circle_x > 500:
        #     circle_vx = -circle_vx
        # if circle_y < 0 or circle_y > 500:
        #     circle_vy = -circle_vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        line_x = self.x + self.radius * cos(radians(self.ang))
        line_y = self.y - self.radius * sin(radians(self.ang))
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (line_x, line_y))


class Trailer:
    def __init__(self, x, y, length, width, color):
        self.x = x 
        self.y = y
        self.vel = 0
        self.ang = 0

        self.length = length
        self.width = width
        self.color = color

    def physics_update(self, pololu):
        self.ang = get_dir_to(self.x, self.y, pololu.x, pololu.y)
        dist = get_dist_to(self.x, self.y, pololu.x, pololu.y)
        move_dist = dist - pololu.radius - self.length/2
        self.x += move_dist * cos(radians(self.ang))
        self.y -= move_dist * sin(radians(self.ang))
        # pass


    def draw(self, screen):
        # trailer_rect = pygame.Rect(self.x - self.width/2, self.y - self.length/2, 
        #                    self.width, self.length)
        # pygame.draw.rect(screen, self.color, trailer_rect)
        # Rotate trailer
        # Create trailer surface 

        # TODO CAN BE OPTIMIZED BY CREATING COPY OF SURFACE, SEE https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame
        trailer_surf = pygame.Surface((self.length, self.width))
        trailer_surf.set_colorkey((0,0,0))
        trailer_surf.fill(self.color)

        # Rotate trailer surface
        # self.ang += 1
        rotated_trailer = pygame.transform.rotate(trailer_surf, self.ang) 

        # Position rotated trailer
        rect = rotated_trailer.get_rect()
        rect.center = (self.x, self.y)

        # Draw rotated trailer
        screen.blit(rotated_trailer, rect)

        line_x = self.x + 5 * cos(radians(self.ang))
        line_y = self.y - 5 * sin(radians(self.ang))
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (line_x, line_y))

        # Rotate tire positions
        # Positions based on trailer rect
        # tire_x1 = rotated_trailer.get_rect().left + 5  
        # tire_y1 = rotated_trailer.get_rect().bottom - 5
        # tire_x2 = rotated_trailer.get_rect().right - 5
        # tire_y2 = rotated_trailer.get_rect().bottom - 5

        # tire_x1, tire_y1 = pygame.transform.rotate((tire_x1, tire_y1), self.ang)
        # tire_x2, tire_y2 = pygame.transform.rotate((tire_x2, tire_y2), self.ang)

        # # Draw tires
        # tire_width = 10
        # tire_height = 20
        # pygame.draw.ellipse(screen, (0,0,0), (tire_x1, tire_y1, tire_width, tire_height))
        # pygame.draw.ellipse(screen, (0,0,0), (tire_x2, tire_y2, tire_width, tire_height))


        

pololu = Pololu(250, 250, 20, color=(235, 234, 206))
trailer = Trailer(250, 250, 100, 50, color=(229, 155, 235))

# Main game loop
running = True 
while running:
    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    # Check for quit event
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # key presses
    if keys[pygame.K_LEFT]:
        pololu.ang += 1
    if keys[pygame.K_RIGHT]:
        pololu.ang -= 1
    if keys[pygame.K_UP]:
        pololu.acc = 0.1
    if keys[pygame.K_DOWN]:
        pololu.acc = -0.1

    # Update physics
    pololu.physics_update()
    trailer.physics_update(pololu)

    # Draw stuff
    screen.fill((94, 99, 110))  # background
    pololu.draw(screen)
    trailer.draw(screen)

    # Update display
    pygame.display.update()

    # Tick clock
    clock.tick(120)  # 60 fps

pygame.quit()