import pygame
import sys
import math
import random
from ball import *

pygame.init()

windowSize = (1024, 768)

screen = pygame.display.set_mode(windowSize)

numberOfBalls = 15

ball_list = []

position = [random.randint(0,windowSize[0] - 1),random.randint(0,windowSize[1] - 1)]
radius = random.randint(10,25)
color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
ball_list.append(Ball(screen,position,radius,color=color))

while len(ball_list) < numberOfBalls:
	position = [random.randint(0,windowSize[0] - 1),random.randint(0,windowSize[1] - 1)]
	radius = random.randint(10,25)
	color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	ball = Ball(screen,position,radius,color=color)
	append = True
	for other in ball_list:
		if ball.intersects(other):
			append = False
			break
	if append: ball_list.append(ball)

balls = BallList(ball_list)


clock = pygame.time.Clock()

while 1:
	clock.tick(40)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)

	screen.fill((0, 0, 0))

	balls.move()
	balls.draw()


	pygame.display.update()