import pygame
import numpy as np
import sys

pygame.init()

pygame.mouse.set_visible(False)

windowSize = (1024, 768)

screen = pygame.display.set_mode(windowSize)

class thingGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

class movingThing(pygame.sprite.Sprite):
    def __init__(self, grp, maxSpeed=20):
        pygame.sprite.Sprite.__init__(self, grp)
        self.image = pygame.Surface((100, 100))
        self.image.fill((100, 0, 100))
        self.rect = self.image.get_rect()
        self.maxSpeed = maxSpeed

    def getPosition(self):
        return np.array([self.rect.x, self.rect.y], np.int32)

    def setPosition(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self):
        mousePos = np.array(pygame.mouse.get_pos(), np.int32)
        displacement = mousePos - self.getPosition()

        if np.linalg.norm(displacement) > 10:
            velocity = displacement.astype(float) / np.linalg.norm(displacement)
            velocity *= self.maxSpeed
            self.rect.x += velocity[0]
            self.rect.y += velocity[1]


clock = pygame.time.Clock()

group = thingGroup()
thing = movingThing(group)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill((0, 0, 0))

    thing.move()

    group.draw(screen)

    pygame.display.update()
