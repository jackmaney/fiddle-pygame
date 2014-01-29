import pygame
import numpy as np
import sys

pygame.init()

pygame.mouse.set_visible(False)

windowSize = (1024, 768)

screen = pygame.display.set_mode(windowSize)

rect = pygame.Surface((50, 50))

rect.fill((100, 0, 100))

position = np.array([100, 100], np.int32)

maxSpeed = 20

clock = pygame.time.Clock()

maxSpeed = 20

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill((0, 0, 0))

    mousePos = np.array(pygame.mouse.get_pos(), np.int32)

    displacement = mousePos - position

    if np.linalg.norm(displacement) > 10:
        velocity = displacement / np.linalg.norm(displacement)
        velocity *= maxSpeed
        position += velocity

    screen.blit(rect, position)

    pygame.display.update()
