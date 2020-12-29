import pygame as pg
from tkinter import *
from random import randint
from car import player
from boundary import Boundary
from particle import Particle
from raycast import Ray


def main():
	### CONFIG
	screen_w = 800
	screen_h = 600
	border_on = False
	num_walls = 0
	num_rays = 4
	angle_diff = 2
	# CAR CONFIG
	speed = 300
	clock = pg.time.Clock()
	# RACETRACK CONFIG
	click_once = False
	x1, y1 = 0, 0
	x2, y2 = 0, 0

	# tkinter menu
	root = Tk()
	root.geometry('186x600')
	root.geometry('+45+69')
	root.title('configs')

	def save_track():
		Boundary.save_boundaries(boundaries)

	def load_track():
		e = Boundary.load_boundaries()
		for _ in boundaries:
			boundaries.pop()
		for i in e:
			boundaries.append(i)

	def remove_line():
		try:
			undo.append(boundaries.pop())
		except IndexError:
			pass

	def re_add_line():
		try:
			boundaries.append(undo.pop())
		except IndexError:
			pass

	button = Button(root, text = 'Save Track', command = save_track)
	button.grid(row = 0, column = 0, sticky = W + E + N + S, ipady = 4)

	button1 = Button(root, text='Load Track', command = load_track)
	button1.grid(row = 1, column= 0, sticky = W + E + N + S, ipady = 4)

	button1 = Button(root, text='Remove Line', command = remove_line, repeatinterval = 150, repeatdelay = 200)
	button1.grid(row = 2, column= 0, sticky = W + E + N + S, ipady = 4)

	button1 = Button(root, text='Undo', command = re_add_line, repeatinterval = 150, repeatdelay = 200)
	button1.grid(row = 2, column= 1, sticky = W + E + N + S, ipady = 4)



	# pygame variables
	pg.init()
	screen = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)

	running = True
	pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

	p = Particle()
	boundaries = []
	undo = []
	rays = []
	load_track()

	if border_on:
		boundaries.append(Boundary(screen, (0, 0), (screen_w, 0)))
		boundaries.append(Boundary(screen, (screen_w, 0), (screen_w, screen_h)))
		boundaries.append(Boundary(screen, (screen_w, screen_h), (0, screen_h)))
		boundaries.append(Boundary(screen, (0, screen_h), (0, 0)))

	for i in range(num_walls):
		boundaries.append(Boundary(screen, (randint(0, screen_w), randint(0, screen_h)), (randint(0, screen_w), randint(0, screen_h))))

	angle = 0
	rays.append(Ray(p, 0))
	rays.append(Ray(p, 180))
	for i in range(1, num_rays):
		angle = i * 180 / num_rays
		rays.append(Ray(p, angle))

	while running:
		mx, my = pg.mouse.get_pos()
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

			if event.type == pg.MOUSEBUTTONUP:
				if not click_once:
					x1, y1 = mx, my
					click_once = True
				else:
					x2, y2 = mx, my
					boundaries.append(Boundary(screen,(x1, y1), (x2, y2)))
					click_once = False

		screen.fill((0, 0, 0))
		delta = clock.tick(60)/1000
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			Ray.rotate_rays(-angle_diff, rays)
			player.rotateleft(angle_diff)

		if keys[pg.K_RIGHT]:
			Ray.rotate_rays(angle_diff, rays)
			player.rotateright(angle_diff)

		if keys[pg.K_UP]:
			player.setpos(speed*delta)

		if keys[pg.K_DOWN]:
			player.setpos(-speed*delta)



		for b in boundaries:
			b.update(screen)

		for r in rays:
			r.update(screen, p, boundaries)

		# p.update(screen, mx, my)
		p.update(screen, player.x ,player.y)
		player.update(screen)

		pg.display.update()
		root.update()


if __name__ == "__main__":
	main()
