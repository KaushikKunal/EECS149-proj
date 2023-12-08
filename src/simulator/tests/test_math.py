import sys
from math import *
import random
import time


class Model:
    def __init__(self, q, d):
        self.q = q
        self.d = d
        self.phi = 0.2
        self.theta = 0.1
        self.velocity = 0

    def model_response(self, left, right):
        change_phi = (right - left) / self.d
        if change_phi == 0:
            # driving straight
            self.velocity = right
        else:
            r = (self.d / 2) - (right / change_phi)
            self.velocity = -r * (sin(self.phi) * (1-cos(change_phi)) + cos(self.phi)*sin(change_phi))
            change_theta = (r / self.q) * (cos(self.phi) * (1 - cos(change_phi)) - sin(self.phi) * sin(change_phi))
            print("phi: ", self.phi, "change_phi: ", change_phi)
            print("theta: ", self.theta, "change_theta: ", change_theta)
            self.phi += change_phi
            self.theta += change_theta


        rand_phi = 0.001 * random.randrange(-100, 100)
        rand_theta = 0.001 * random.randrange(-100, 100)
        # print("rand_phi: ", rand_phi, " rand_theta: ", rand_theta)

        # self.phi += rand_phi
        # self.theta += rand_theta

    def calculate_control_right(self, velocity):
        return 
        # return - self.phi * (velocity/(cos(2*self.phi) - cos(self.phi)) + self.d/2)

    def calculate_control_left(self, velocity, right):
        
        # return right - (self.d * right)/(self.d/2 - (self.q * self.theta)/(cos(2*self.phi) - cos(self.phi)))

    def control(self, velocity):
        # order matters
        right = self.calculate_control_right(velocity)
        left = self.calculate_control_left(velocity, right)
        return left, right



def main():
    model = Model(2, 1)
    while (True):
        inp = input("press enter")  # for pausing
        left, right = model.control(1)
        # print("left: ", left, " right:", right)
        print("phi: ", model.phi, " theta: ", model.theta)
        model.model_response(left, right)
        time.sleep(0.2)



if __name__ == "__main__":
    main()