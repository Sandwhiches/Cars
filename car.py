import pygame
import math

class gameobject():
	def __init__(self, image, x, y, angle):
		self.x = x
		self.y = y
		self.image = image
		self.rotated_image = self.image
		self.ded = False
		self.angle = angle

	def rotateright(self):
		self.angle -= 2
		self.angle %= 360

	def rotateleft(self):
		self.angle += 2
		self.angle %= 360

	def setpos(self, diff):
		self.x += diff*(math.cos(math.radians(self.angle)))
		self.y -= diff*(math.sin(math.radians(self.angle)))

	def update(self, screen):
		self.rotated_image = pygame.transform.rotate(self.image, self.angle)
		screen.blit(self.rotated_image, (self.x - int(self.rotated_image.get_width()/2), self.y - int(self.rotated_image.get_height()/2)))

car = pygame.transform.scale(pygame.image.load('assets//paper-plane.png'), (50, 25))
player = gameobject(car, 375, 485, angle = 270)

