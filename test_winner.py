import pygame as pg
import os
import neat
import pickle
from tkinter import *
from car import gameobject
from car import Ray
from boundary import Boundary




Ray.boundaries = Boundary.load_boundaries('assets//winner_test_track.txt')
def main(genome, config):
    ### CONFIG
    screen_w = 1250
    screen_h = 750

    # CAR CONFIG
    speed = 0
    speed_cap = 400
    angle_diff = 90
    acc = 100
    car1 = pg.transform.scale(pg.image.load('assets//car - Copy (2).png'), (50, 50))
    car2 = pg.transform.scale(pg.image.load('assets//car.png'), (50, 50))

    # NETWORK CONFIG
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    car = gameobject(car1, 130, 450, angle = 270, speed = speed, acc = acc, speed_cap = speed_cap, vision_rays = [Ray(0), Ray(180), Ray(90, 25), Ray(45, 16), Ray(135, 16)])
   
    player = gameobject(car2, 130, 450, angle = 270, speed = speed, acc = acc, speed_cap = speed_cap, vision_rays = [Ray(0), Ray(180), Ray(90, 25), Ray(45, 16), Ray(135, 16)])

    clock = pg.time.Clock()

    def load_track():
        nonlocal boundaries
        boundaries = Boundary.load_boundaries('assets//winner_test_track.txt')

    # pygame variables
    pg.init()
    screen = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)

    running = True
    boundaries = []
    load_track()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        keys = pg.key.get_pressed()
        if keys[pg.K_BACKSLASH]:
            Ray.draw_rays = not Ray.draw_rays

        screen.fill((245,255,237))
        delta = clock.tick(60)/1000
        temp_angle = angle_diff*delta


        output = net.activate(tuple(car.distances) + (car.speed,))
        if output[0] == 1 :
            car.rotateleft(temp_angle)
        if output[1] == 1:
            car.rotateright(temp_angle)
        if output[2] == 1:
            car.setpos(delta)

        if keys[pg.K_LEFT]:
            player.rotateleft(temp_angle)
        if keys[pg.K_RIGHT]:
            player.rotateright(temp_angle)
        if keys[pg.K_UP]:
            player.setpos(delta)

        player.update(screen, delta)
        car.update(screen, delta)
        Boundary.update_all(screen, boundaries)
        pg.display.update()



def run(config_file):
    with open('assets//Winner.txt', 'rb') as f:
        w = pickle.load(f)
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    main(w, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
    print('d')