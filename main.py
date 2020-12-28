import pygame as pg
from random import randint
from car import player
from boundary import Boundary
from particle import Particle
from raycast import Ray


def main():
    ### CONFIG
    screen_w = 800
    screen_h = 600
    border_on = True
    num_walls = 9
    num_rays = 5
    angle_diff = 2
    # CAR CONFIG
    speed = 300
    clock = pg.time.Clock()
    
    ### END CONFIG

    pg.init()
    screen = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)

    running = True
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    p = Particle()
    boundaries = []
    rays = []

    if border_on:
        boundaries.append(Boundary(screen, (0, 0), (screen_w, 0)))
        boundaries.append(Boundary(screen, (screen_w, 0), (screen_w, screen_h)))
        boundaries.append(Boundary(screen, (screen_w, screen_h), (0, screen_h)))
        boundaries.append(Boundary(screen, (0, screen_h), (0, 0)))

    for i in range(num_walls):
        boundaries.append(Boundary(screen,
                                   (randint(0, screen_w), randint(0, screen_h)),
                                   (randint(0, screen_w), randint(0, screen_h))))

    angle = 0
    for i in range(num_rays):
        angle = i * 180 / num_rays
        rays.append(Ray(p, angle))

    while running:
        mx, my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill((0, 0, 0))
        delta = clock.tick(60)/1000

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            Ray.rotate_rays(-angle_diff, rays)
            player.rotateleft()

        if keys[pg.K_RIGHT]:
            Ray.rotate_rays(angle_diff, rays)
            player.rotateright()

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


if __name__ == "__main__":
    main()
