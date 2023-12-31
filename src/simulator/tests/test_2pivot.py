import pygame
import sys
from math import *
import random

# Initialize Pygame 
pygame.init()

class Debugger:
    def __init__(self):
        self.debug_lines = []
        self.fontsize = 15
        self.font = pygame.font.SysFont("sfcompact", self.fontsize)
        self.margin = 2

    def log_text(self, text):
        self.debug_lines.append(text)

    def log_var(self, var_name, var):
        if (type(var) == float):
            self.debug_lines.append(f"{var_name}: {var:.2f}")
        else:
            self.debug_lines.append(f"{var_name}: {var}")

    def draw(self, screen):
        for i, line in enumerate(self.debug_lines):
            text_surface = self.font.render(line, True, (0, 0, 0))
            # text_surface = self.font.render(line, True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  # PARTY MODE
            screen.blit(text_surface, (self.margin, self.margin + (self.margin + self.fontsize)*i))
        self.debug_lines = ["DEBUG"]  # clear debug lines

debugger = Debugger()

# def tick_sim():




# Set up the display surface 
screen = pygame.display.set_mode((700, 600))

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
        

class Object:
    def __init__(self, x, y, color):
        self.x = x 
        self.y = y
        self.color = color

        self.vel = 0
        self.ang = 0  # degrees

    def draw_tyre(self, screen, x_off, y_off, width=5, height=20):
        # Calculate the rotated coordinates of the tire
        rotated_x = self.x + x_off * sin(radians(self.ang)) + y_off * cos(radians(self.ang))
        rotated_y = self.y + x_off * cos(radians(self.ang)) - y_off * sin(radians(self.ang))

        # pygame.draw.circle(screen, (0,0,0), (rotated_x, rotated_y), 3)
        tire_surf = pygame.Surface((height, width), pygame.SRCALPHA)
        pygame.draw.ellipse(tire_surf, (0,0,0), tire_surf.get_rect())
        rotated_tire = pygame.transform.rotate(tire_surf, self.ang)
        rect = rotated_tire.get_rect()
        rect.center = (rotated_x, rotated_y)
        screen.blit(rotated_tire, rect)


class Pololu(Object):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, color)
        self.vel = 0
        self.ang = 0  # degrees
        self.acc = 0
        self.ang_acc = 0  # degrees per second

        self.radius = radius

    def physics_update(self):
        self.ang += self.ang_acc
        self.vel += self.acc

        self.x += self.vel * cos(radians(self.ang))
        self.y -= self.vel * sin(radians(self.ang))

        self.acc = 0
        self.ang_acc = 0

        # friction
        self.vel *= 0.95

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.draw_tyre(screen, self.radius, 0)
        self.draw_tyre(screen, -self.radius, 0)
        line_x = self.x + self.radius * cos(radians(self.ang))
        line_y = self.y - self.radius * sin(radians(self.ang))
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (line_x, line_y))

class Hitch(Object):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, color)
        self.radius = radius

    def physics_update(self, pololu, link_length):
        # rotate hitch towards pololu
        self.ang = get_dir_to(self.x, self.y, pololu.x, pololu.y)

        # attach trailer to hitch
        dist = get_dist_to(self.x, self.y, pololu.x, pololu.y)
        move_dist = dist - link_length
        self.x += move_dist * cos(radians(self.ang))
        self.y -= move_dist * sin(radians(self.ang))
        debugger.log_var("hitch ang", self.ang)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Trailer(Object):
    def __init__(self, x, y, length, width, axle_offset, color):
        super().__init__(x, y, color)
        self.vel = 0
        self.ang = 0

        self.length = length
        self.width = width
        self.axle_offset = axle_offset  # distance from center of trailer to axle (+ve is forward, -ve is backward)

        self.line_length = length/4  # for drawing line

    def physics_update(self, hitch, link_length):
        # rotate trailer about axle
        axle_x = self.x + self.axle_offset * cos(radians(self.ang))
        axle_y = self.y - self.axle_offset * sin(radians(self.ang))
        self.ang = get_dir_to(axle_x, axle_y, hitch.x, hitch.y)
        self.x = axle_x - self.axle_offset * cos(radians(self.ang))
        self.y = axle_y + self.axle_offset * sin(radians(self.ang))
        
        # attach trailer to hitch
        dist = get_dist_to(self.x, self.y, hitch.x, hitch.y)
        move_dist = dist - link_length
        self.x += move_dist * cos(radians(self.ang))
        self.y -= move_dist * sin(radians(self.ang))
        debugger.log_var("trailer ang", self.ang)


    def draw(self, screen):
        # TODO CAN BE OPTIMIZED BY CREATING COPY OF SURFACE, SEE https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame
        trailer_surf = pygame.Surface((self.length, self.width))
        trailer_surf.set_colorkey((0,0,0))
        trailer_surf.fill(self.color)

        # Rotate trailer surface
        rotated_trailer = pygame.transform.rotate(trailer_surf, self.ang) 

        # Position rotated trailer
        rect = rotated_trailer.get_rect()
        rect.center = (self.x, self.y)

        # Draw rotated trailer
        screen.blit(rotated_trailer, rect)

        line_x = self.x + self.line_length * cos(radians(self.ang))
        line_y = self.y - self.line_length * sin(radians(self.ang))
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (line_x, line_y))

        self.draw_tyre(screen, self.width/2, self.axle_offset)
        self.draw_tyre(screen, -self.width/2, self.axle_offset)


        

pololu = Pololu(250, 250, 20, color=(235, 234, 206))
hitch = Hitch(250, 250, 5, color=(0, 0, 0))
trailer = Trailer(250, 250, 100, 50, -30, color=(229, 155, 235))

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

    link1_length = pololu.radius + hitch.radius  # length of link connecting pololu and hitch
    link2_length = trailer.length/2 + hitch.radius  # length of link connecting hitch and trailer
    pololu.physics_update()
    hitch.physics_update(pololu, link1_length)
    trailer.physics_update(hitch, link2_length)

    # Draw stuff
    screen.fill((157, 162, 171))  # background
    pygame.draw.line(screen, (0,0,0), (350, 100), (350, 500))
    pololu.draw(screen)
    hitch.draw(screen)
    trailer.draw(screen)
    debugger.draw(screen)

    # Update display
    pygame.display.update()

    # Tick clock
    clock.tick(120)  # fps

pygame.quit()