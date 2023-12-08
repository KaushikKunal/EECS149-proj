import pygame
import sys
from math import *
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Initialize Pygame 
pygame.init()
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
error_history = []

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

    def physics_update(self, pivot, link_length):
        # rotate hitch towards pivot
        self.ang = get_dir_to(self.x, self.y, pivot.x, pivot.y)

        # attach hitch to pivot (dist constraint)
        dist = get_dist_to(self.x, self.y, pivot.x, pivot.y)
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

class Truck():
    def __init__(self, x, y, num_pivots):
        self.num_pivots = num_pivots
        self.pololu = Pololu(x, y, 20, (235, 234, 206))
        self.hitches = [Hitch(x, y, 5, (20, 20, 20)) for i in range(self.num_pivots - 1)]
        self.trailer = Trailer(x, y, 100, 50, -30, (229, 155, 235))

        self.error_last = np.array([0, 0])
        self.integral_error = np.array([0, 0])

    def brain(self, target_x, target_y):
        # target_dir = get_dir_to(self.trailer.x, self.trailer.y, target_x, target_y)
        # debugger.log_var("target dir", target_dir)
        # debugger.log_var("current dir", (self.trailer.ang - target_dir) % 360)

        timestep = 1/60
        kp = 0.36
        kd = 0.001
        ki = 40

        self.error = np.array([target_x - self.pololu.x, target_y - self.pololu.y]) 
        self.integral_error = self.integral_error + self.error * timestep
        self.derivative_error = (self.error - self.error_last) / timestep
        self.error_last = self.error
        error_history.append(self.error[0])

        debugger.log_var("error", self.error)
        output = kp * self.error + kd * self.derivative_error + ki * self.integral_error

        debugger.log_var("output", output)
        self.pololu.x += output[0]
        self.pololu.y += output[1]

        # self.pololu.ang = degrees(-atan2(output[1], output[0]))
        # debugger.log_var("norm", np.linalg.norm(output))
        # self.pololu.acc = np.linalg.norm(output)

        # pos_error = np.array([target_x - self.trailer.x, target_y - self.trailer.y])
        # vel_error = 0
        # desired_acc = kp * pos_error + kd * vel_error
        # self.pololu.ang = degrees(-atan2(desired_acc[1], desired_acc[0]))
        # self.pololu.acc = 0.1

        # debugger.log_var("desired acc", desired_acc)
        # debugger.log_var("desired ang", degrees(-atan2(desired_acc[1], desired_acc[0])))

        # ziegler nichols
        # response saturation



        
        # ang_error = (self.trailer.ang - target_dir) % 360


    def physics_update(self):
        self.pololu.physics_update()
        link_length = self.pololu.radius
        prev_hitch = self.pololu
        for hitch_i in range(len(self.hitches)):
            hitch = self.hitches[hitch_i]
            prev_link_length = link_length
            link_length += hitch.radius
            hitch.physics_update(prev_hitch, link_length)
            prev_hitch = hitch
            link_length -= prev_link_length
        link_length += self.trailer.length/2
        self.trailer.physics_update(prev_hitch, link_length)

    def draw(self, screen):
        self.pololu.draw(screen)
        for hitch in self.hitches:
            hitch.draw(screen)
        self.trailer.draw(screen)
        

# pololu = Pololu(250, 250, 20, color=(235, 234, 206))
# hitch = Hitch(250, 250, 5, color=(0, 0, 0))
# trailer = Trailer(250, 250, 100, 50, -30, color=(229, 155, 235))

truck = Truck(250, 250, 1)
# Main game loop
running = True 
tick = 0
while running:
    fps = int(clock.get_fps())
    debugger.log_var("fps", fps)

    keys = pygame.key.get_pressed()
    events = pygame.event.get()

    # Check for quit event
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_SPACE]:
        truck.brain(250, 250)
    else:
        # key presses
        if keys[pygame.K_LEFT]:
            truck.pololu.ang += 1
        if keys[pygame.K_RIGHT]:
            truck.pololu.ang -= 1
        if keys[pygame.K_UP]:
            truck.pololu.acc = 0.1
        if keys[pygame.K_DOWN]:
            truck.pololu.acc = -0.1
    
    # debugger.log_var("ang", truck.pololu.ang)
    

    # Update physics
    truck.physics_update()

    # Draw stuff
    screen.fill((157, 162, 171))  # background
    pygame.draw.line(screen, (0,0,0), (350, 100), (350, 500))
    truck.draw(screen)
    debugger.draw(screen)

    # Update display
    pygame.display.update()
    if (tick % 60 == 0):
        ax.clear()
        ax.plot(error_history[-200:])
        ax.set_title('Error History')
        ax.set_xlabel('Timestep')
        ax.set_ylabel('Error')
        plt.draw()
        plt.pause(0.001)

    # Tick clock
    clock.tick(60)  # fps
    tick += 1

plt.ioff()


pygame.quit()