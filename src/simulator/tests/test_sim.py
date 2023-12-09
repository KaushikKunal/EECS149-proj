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

    def draw_tyre(self, screen, x_off, y_off, width=5, height=20, color=(0,0,0)):
        # Calculate the rotated coordinates of the tire
        rotated_x = self.x + x_off * sin(radians(self.ang)) + y_off * cos(radians(self.ang))
        rotated_y = self.y + x_off * cos(radians(self.ang)) - y_off * sin(radians(self.ang))

        # pygame.draw.circle(screen, (0,0,0), (rotated_x, rotated_y), 3)
        tire_surf = pygame.Surface((height, width), pygame.SRCALPHA)
        pygame.draw.ellipse(tire_surf, color, tire_surf.get_rect())
        rotated_tire = pygame.transform.rotate(tire_surf, self.ang)
        rect = rotated_tire.get_rect()
        rect.center = (rotated_x, rotated_y)
        screen.blit(rotated_tire, rect)


class Wheel(Object):
    def __init__(self, height, width, friction, color):
        self.height = height
        self.width = width
        self.friction = friction
        self.color = color
        self.vel = 0

        self.friction = friction

    def required_acc(self, time, dist):
        """
        Returns the required acceleration to
        travel dist in the next time step
        """
        return (2 / (time * time)) * (dist - self.vel * time)
    def physics_update(self, time, acceleration):
        """ Updates wheel variables.
        Returns the distance travelled this time step.
        """
        # self.vel *= self.friction # not accurate
        dist_travelled = self.vel * time + (1/2) * acceleration * time * time # kinematic equation
        self.vel += acceleration
        return dist_travelled

    def draw(self, screen, parent, x_off, y_off):
        parent.draw_tyre(screen, x_off, y_off, self.width, self.height, self.color)



class Pololu(Object):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, color)
        self.left_wheel = Wheel(20, 5, 0.7, (255, 255, 100))
        self.right_wheel = Wheel(20, 5, 0.7, (255, 100, 100))
        self.trailer = Trailer(250, 250, 100, 50, -30, color=(229, 155, 235))
        self.radius = radius
        self.link_length = self.radius + self.trailer.length / 2  # length of link connecting pololu and trailer
        self.ang_cutoff = 2

    def physics_update(self, time, desired_angle, desired_speed):
        acc_left, acc_right = self.control_acc(time, desired_angle, desired_speed)

        trav_left = self.left_wheel.physics_update(time, acc_left)
        trav_right = self.right_wheel.physics_update(time, acc_right)

        if trav_left == trav_right:
            # driving straight
            change_y = 0
            change_x = trav_left
            change_ang = 0
        else:
            # turning
            change_ang = (trav_right - trav_left) / (2 * self.radius)
            change_x = (trav_right / change_ang - self.radius) * sin(change_ang)
            change_y = (trav_right / change_ang - self.radius) * (1 - cos(change_ang))

        self.x += cos(radians(self.ang)) * change_x + sin(radians(self.ang)) * change_y
        self.y += -sin(radians(self.ang)) * change_x + cos(radians(self.ang)) * change_y
        self.ang += change_ang * 360 / (2 * pi)
        self.ang %= 360

        self.trailer.physics_update(1, pololu, self.link_length)

    def control_acc(self, next_time, desired_angle, desired_speed):
        true_ang_err = desired_angle - self.get_trailer_ang()
        if true_ang_err > 180:
            true_ang_err -= 360
        if true_ang_err < -180:
            true_ang_err += 360
        ang_err = radians(true_ang_err)
        debugger.log_var("ang_err", true_ang_err)
        trav_right, trav_left = 0, 0
        if -5 < true_ang_err < 5:
            # driving straight
            trav_right = desired_speed
            trav_left = desired_speed
        else:
            # turning, positive speed
            trav_right = desired_speed + self.radius * ang_err
            trav_left = desired_speed - self.radius * ang_err
        acc_left = self.left_wheel.required_acc(next_time, trav_left)
        acc_right = self.right_wheel.required_acc(next_time, trav_right)
        return (acc_left, acc_right)

    def get_trailer_ang(self):
        relative_ang = self.ang - self.trailer.ang
        if relative_ang > 180:
            relative_ang -= 360
        if relative_ang < -180:
            relative_ang += 360
        return relative_ang

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        self.left_wheel.draw(screen, self, -self.radius, 0)
        self.right_wheel.draw(screen, self, self.radius, 0)
        self.trailer.draw(screen)
        line_x = self.x + self.radius * cos(radians(self.ang))
        line_y = self.y - self.radius * sin(radians(self.ang))
        pygame.draw.line(screen, (0,0,0), (self.x, self.y), (line_x, line_y))


class Trailer(Object):
    def __init__(self, x, y, length, width, axle_offset, color):
        super().__init__(x, y, color)
        self.vel = 0
        self.ang = 0

        self.length = length
        self.width = width
        self.axle_offset = axle_offset  # distance from center of trailer to axle (+ve is forward, -ve is backward)

        self.line_length = length/4  # for drawing line

    def physics_update(self, time, hitch, link_length):
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
desired_angle = 0
desired_speed = 0

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
        desired_angle += 5
    if keys[pygame.K_RIGHT]:
        desired_angle -= 5
    if keys[pygame.K_UP]:
        desired_speed += 0.3
    if keys[pygame.K_DOWN]:
        desired_speed -= 0.3

    # desired_speed -= 0.1
    # if desired_speed < 0:
    #     desired_speed = 0

    debugger.log_var("des_ang", desired_angle)
    debugger.log_var("des_spd", desired_speed)

    # Update physics
    pololu.physics_update(1, desired_angle, desired_speed)

    # Debug information
    debugger.log_var("trav_right", pololu.right_wheel.vel)
    debugger.log_var("trav_left", pololu.left_wheel.vel)

    # Draw stuff
    screen.fill((157, 162, 171))  # background
    pygame.draw.line(screen, (0,0,0), (350, 100), (350, 500))
    pololu.draw(screen)
    debugger.draw(screen)

    # Update display
    pygame.display.update()

    # Tick clock
    clock.tick(30)  # fps

pygame.quit()