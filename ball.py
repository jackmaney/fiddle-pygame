import random
import math
import pygame
import numpy as np


class Ball:

    def __init__(self, screen, position, radius, color=(255, 255, 255), velocity=None):

        if radius < 0:
            raise Exception("Radius cannot be negative")

        self.radius = radius

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

    def changeDirection(self, other):

        dist = self.distanceBetweenCenters(other)

        # (I used http://stackoverflow.com/a/3349134 to double-check
        # my reasoning and calculations here)
        #
        # Now is where we need a bit of a mathematical explanation.
        # Denote self.getCenter() and other.getCenter() by C1 and C2.
        # Let d be the distance from C1 to C2, and let the radii of
        # self and other be r1 and r2, respectively.
        #
        # Since this method is only called when there's an intersection,
        # we'll assume that d <= r1 + r2. Since the tangent case is easy
        # (no position change, just a velocity change), we'll assume that
        # d < r1 + r2 so that we have two points of intersection.
        #
        # Let L denote the line through these points of intersection. We know
        # that L is orthogonal to the line between C1 and C2. We seek the
        # point of intersection of these lines, which I'll call Q.
        #
        # Let a denote the distance from C1 to Q, let b denote the distance
        # from C2 to Q, and let h denote the distance from Q to either of the
        # intersection points. Pythagoras tells us that:
        #
        #       a^2 + h^2 == r1^2 and b^2 + h^2 == r2^2.
        #
        # Therefore,
        #
        #       a^2 - b^2 == r1^2 - r2^2
        #
        # and taking advantage of the fact that d == a + b, we have
        #
        #       a^2 - (d - a)^2 == r1^2 - r2^2
        #
        # which simplifies to:
        #
        #       -d^2 + 2*a*d == r1^2 - r2^2
        #
        # and solving for a, we get:
        #
        #       a == (r1^2 - r2^2 + d^2) / 2*d
        #
        # We can play a similar trick and get
        #
        #       b == (r2^2 - r1^2 + d^2) / 2*d
        #
        # In particular, this means that
        #
        #   Q = C1 + a(C2 - C1) / d
        #
        # All that we have to do now is move each of the circles away from each other
        # along the line between the centers, and in the amounts that are the distances
        # between Q and the edges of each circle (which are r1 - a and r2 - b, respectively).
        #
        # So, we move C1 to C1 + (r1 - a)*(C1 - C2)/r1 and C2 to C2 + (r2 - b)*(C2 - C1)/r2
        #
        # Note that we've also assumed that neither of the centers are included in the other circle
        # (ie d > max(r1,r2)). We'll deal with this case--and the case of d == r1 + r2 (ie one point of
        # intersection) below.
        #

        d = self.distanceBetweenCenters(other)
        r1 = self.radius
        r2 = other.radius

        # First, though, a really dumb case...
        if d == 0:
            # Move self to the left, or if we can't, move self to the right
            if self.position[0] > r1 + r2:
                self.position[0] -= r1 + r2
            else:
                self.position[0] += r1 + r2

        else:

            C1 = self.getCenter().astype(float)
            C2 = other.getCenter().astype(float)
            a = float(r1 * r1 - r2 * r2 + d * d) / float(2 * d)
            b = float(r2 * r2 - r1 * r1 + d * d) / float(2 * d)

            centerCandidate = self.getCenter()
            otherCenterCandidate = other.getCenter()

            if d > r1 and d > r2:

                centerCandidate = np.around(
                    C1 + (r1 - a) * (C1 - C2) / r1).astype(np.int32)
                otherCenterCandidate = np.around(
                    C2 + (r2 - b) * (C2 - C1) / r2).astype(np.int32)

                # Are these candidates in bounds?

                if self.outOfBoundsCenter(otherCenterCandidate):
                    # Move self the extra mile
                    otherCenterCandidate = other.getCenter()
                    centerCandidate += np.around((r2 - b)
                                                 * (C1 - C2) / r2).astype(np.int32)
                elif self.outOfBoundsCenter(centerCandidate):
                    # Likewise...
                    centerCandidate = self.getCenter()
                    otherCenterCandidate += np.around((r1 - a)
                                                      * (C2 - C1) / r1).astype(np.int32)

            elif d > r1:
                # If this is the case, then d <= r2, which means that C2 is inside of
                # the ball for self. We'll cheat and move other the hell out of
                # dodge.

                otherCenterCandidate = np.around(
                    C2 + (d - r1 + r2) * (C2 - C1) / r2).astype(np.int32)

                if self.outOfBoundsCenter(otherCenterCandidate):
                    # Unless we can't...mumble grumble...
                    otherCenterCandidate = other.getCenter()

                    centerCandidate = np.around(
                        C1 + (d - r2 + r1) * (C1 - C2) / r1).astype(np.int32)

            elif d > r2:
                # Similar case: d <= r1, so move self the hell out of dodge

                centerCandidate = np.around(
                    C1 + (d - r2 + r1) * (C1 - C2) / r1).astype(np.int32)

                if self.outOfBoundsCenter(centerCandidate):
                    centerCandidate = self.getCenter()
                    otherCenterCandidate = np.around(
                        C2 + (d - r1 + r2) * (C2 - C1) / r2).astype(np.int32)
            else:
                # If d <= r1 and d <= r2, then C1 is inside other and C2 is inside self
                # Again, we'll cheat and move self out of dodge.

                centerCandidate = np.around(
                    C1 + (r2 - d + r1) * (C1 - C2) / r1).astype(np.int32)

                if self.outOfBoundsCenter(centerCandidate):
                    centerCandidate = self.getCenter()
                    otherCenterCandidate = np.around(
                        C2 + (r1 - d + r2) * (C2 - C1) / r2).astype(np.int32)

            self.setCenter(centerCandidate)
            other.setCenter(otherCenterCandidate)

        # TODO: Make more realistic

        self.velocity *= -1
        other.velocity *= -1

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
                    ball.changeDirection(other)

        for ball in self:
            ball.keepInWindow()

    def render(self):
        for ball in self:
            ball.render()
