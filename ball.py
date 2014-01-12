import random
import math
import pygame



class Ball:
	def __init__(self,surface,position,radius
			,color=(255,255,255)
			,velocity=None):

		if radius < 0:
			raise Exception("Radius cannot be negative")

		self.rect_size = (2 * radius + 1, 2 * radius + 1)
		self.color = color
		self.position = position

		if velocity is not None:
			self.velocity = velocity
		else:
			self.velocity = [random.randint(-20,20),random.randint(-20,20)]

		self.surface = surface
		self.radius = radius

		self.windowSize = self.surface.get_size()

	def center(self):
		return [
				self.position[0] + int(math.ceil(self.rect_size[0]/2.0)), 
				self.position[1] + int(math.ceil(self.rect_size[1]/2.0))
			]

	def distanceFromCenters(self,other):
		deltaX = self.position[0] - other.position[0]
		deltaY = self.position[1] - other.position[1]

		return math.sqrt(deltaX * deltaX + deltaY * deltaY)

	def move_check(self):

		newXY = [self.position[0] + self.velocity[0],self.position[1] + self.velocity[1]]
		newVelocity = self.velocity

		if newXY[0] < 0:
			newXY[0] = 0
			newVelocity[0] *= -1

		if newXY[0] + self.rect_size[0] >= self.windowSize[0]:
			newXY[0] = self.windowSize[0] - self.rect_size[0]
			newVelocity[0] *= -1

		if newXY[1] < 0:
			newXY[1] = 0
			newVelocity[1] *= -1

		if newXY[1] + self.rect_size[1] >= self.windowSize[1]:
			newXY[1] = self.windowSize[1] - self.rect_size[1]
			newVelocity[1] *= -1

		return (newXY,newVelocity)

	# Returns 0 if no overlap in x-direction, -1 if self is to the left, 1 if self is to the right
	def intersectX(self,other):
		
		# Check if self overlaps and is on the left of other
		if self.position[0] <= other.position[0] and \
			self.position[0] + self.rect_size[0] >= other.position[0]:
			return -1

		# And check the right side
		if self.position[0] >= other.position[0] and \
			self.position[0] + self.rect_size[0] <= other.position[0] + other.rect_size[0]:
			return 1

		return 0

	# Same deal, remembering that y=0 is at the top!
	# Returns 1 if self is above other and overlapping
	# Returns -1 if self is below other and overlapping
	# Otherwise returns 0
	def intersectY(self,other): 

		if self.position[1] <= other.position[1] and \
			self.position[1] + self.rect_size[1] >= other.position[1] - other.rect_size[1]:
			return 1

		if self.position[1] >= other.position[1] and \
			self.position[1] + self.rect_size[1] <= other.position[1] + other.rect_size[1]:
			return -1

		return 0

	# Returns a 2-tuple to indicate overlap on x's and y's
	def intersects(self,other):
		# return self.intersectX(other) * self.intersectY(other)
		
		return self.distanceFromCenters(other) <= self.radius + other.radius


	def move(self):
		
		newXY, newVelocity = self.move_check()

		self.position = newXY
		self.velocity = newVelocity


	def draw(self):
		pygame.draw.circle(self.surface,self.color,self.center(),self.radius)

	def reverse_direction(self):
		self.velocity[0] *= -1
		self.velocity[1] *= -1


class BallList(list):
	def __init__(self,ball_list):
		for ball in ball_list:
			if not isinstance(ball,Ball):
				raise Exception("Must pass list of Ball objects!")
			self.append(ball)

	def move(self):


		# First, make sure we don't hit the walls...
		for ball in self:
			ball.move()

			

		# Iterate through all pairs of balls
		for i in list(range( len(self) - 1 )):
			for j in list(range(i + 1, len(self) )):

				if self[i].intersects(self[j]):
					if self[i].position[0] <= self[j].position[0]:
						self[i].position[0] = self[j].position[0] - self[i].rect_size[0]
					else:
						self[i].position[0] = self[j].position[0] + self[j].rect_size[0]

					if self[i].position[1] + self[i].rect_size[1] >= self[j].position[1]:
						self[i].position[1] = self[j].position[1] - self[i].rect_size[1]
					else:
						self[i].position[1] = self[j].position[1] + self[j].rect_size[1]

					self[i].reverse_direction()
					self[j].reverse_direction()

				

	def draw(self):
		for ball in self:
			ball.draw()
					


