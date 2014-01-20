import random
import math
import pygame
import numpy as np
from collision_handler import *
import json


class Ball:

    def __init__(self, screen, position, radius, mass=1, color=(255, 255, 255), velocity=None):

        if radius < 0:
            raise Exception("Radius cannot be negative")
        if mass < 0:
            raise Exception("Mass cannot be negative")

        self.radius = radius
        self.mass = mass

        self.rect_size = np.array([2 * radius + 1, 2 * radius + 1], np.int32)
        self.color = color
        self.position = np.array(position, np.int32)

        if velocity is not None:
            self.velocity = np.array(velocity, np.int32)
        else:
            self.velocity = np.array(
                [random.randint(-20, 20), random.randint(-20, 20)], np.int32
            )

        self.screen = screen
        self.screen_size = np.array(self.screen.get_size(), np.int32)

    def getCenter(self):
        return self.position + self.radius + 1

    def setCenter(self, center):
        center = np.array(center, np.int32)
        self.position = center - self.radius - 1

    def distanceBetweenCenters(self, other):
        return math.sqrt(np.vectorize(lambda x: x * x)(self.getCenter() - other.getCenter()).sum())

    def outOfBoundsCenter(self, center):
        return center[0] - self.radius < 0 or center[1] - self.radius < 0 or \
            center[0] + self.radius > self.screen_size[0] or \
            center[1] + self.radius + self.rect_size[1] > self.screen_size[1]

    def outOfBounds(self, pos=None):

        position = None
        if pos is None:
            position = self.position
        else:
            position = pos

        return position[0] < 0 or position[1] < 0 or \
            position[0] + self.rect_size[0] > self.screen_size[0] or \
            position[1] + self.rect_size[1] > self.screen_size[1]

    def keepInWindow(self):

        x, y = self.position

        if self.position[0] < 0:
            x = 0
            self.velocity[0] *= -1
        elif self.position[0] + self.rect_size[0] > self.screen_size[0]:
            x = self.screen_size[0] - self.rect_size[0]
            self.velocity[0] *= -1

        if self.position[1] < 0:
            y = 0
            self.velocity[1] *= -1
        elif self.position[1] + self.rect_size[1] > self.screen_size[1]:
            y = self.screen_size[1] - self.rect_size[1]
            self.velocity[1] *= -1

        self.position = np.array([x, y], np.int32)

    def intersects(self, other):
        return self.distanceBetweenCenters(other) <= self.radius + other.radius

    def render(self):
        pygame.draw.circle(self.screen, self.color,
                           self.getCenter(), self.radius)

    def move(self):
        self.position += self.velocity


class BallList(list):

    def __init__(self, ball_list):
        for ball in ball_list:
            if not isinstance(ball, Ball):
                raise Exception("Must pass list of Ball objects!")
            self.append(ball)

    def move(self):

        for ball in self:
            ball.move()

        for ball in self:
            for other in self:
                if ball != other and ball.intersects(other):
                    handleCollision(ball, other)

        for ball in self:
            ball.keepInWindow()

    def render(self):
        for ball in self:
            ball.render()
