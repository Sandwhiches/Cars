import pygame as pg
import time
import neat
import pickle
import os
from tkinter import *
from car import gameobject
from car import Ray
from boundary import Boundary
from boundary import Checkpoint


draw_checkpoints = False
end_time = 5
gen = -1
def main(genomes, config):
    global draw_checkpoints
    global end_time
    global gen
    max_fitness = 0
    gen += 1
    ### CONFIG
    screen_w = 1250
    screen_h = 750
    angle_diff = 90

    # CAR CONFIG
    speed = 0
    speed_cap = 400
    acc = 100
    car = pg.transform.scale(pg.image.load('assets//car.png'), (50, 50))

    # NETWORK CONFIG
    ge = []
    nets = []
    cars = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(gameobject(car, 130, 450, angle = 270, speed = speed, acc = acc, speed_cap = speed_cap, vision_rays = [Ray(0), Ray(180), Ray(90, 25), Ray(45, 16), Ray(135, 16)]))
        g.fitness = 0
        ge.append(g)


    clock = pg.time.Clock()

    def load_track():
        nonlocal checkpoints
        nonlocal boundaries
        boundaries = Boundary.load_boundaries()
        checkpoints = Checkpoint.load_checkpoints()

    def multlines(text, configs, fontsize):
        text = text.splitlines()
        for i, j in enumerate(text):
            screen.blit(configs.render(j, True, (255, 255, 0)), (0, fontsize*i))



    # pygame variables
    pg.init()
    status = pg.font.Font('freesansbold.ttf',25)
    screen = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)

    running = True
    checkpoints = []
    boundaries = []
    load_track()
    start_time = time.time()


    while running:
        if time.time() - start_time > end_time:
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        # changing elimination time
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            end_time += .5
        if keys[pg.K_DOWN]:
            end_time -= .5
        if keys[pg.K_LEFT]:
            draw_checkpoints = not draw_checkpoints

        screen.fill((245,204,77))
        delta = clock.tick(60)/1000
        temp_angle = angle_diff*delta

        dead = []
        for x, car in enumerate(cars):
            if car.ded:
                dead.append(x)
                continue
            output = nets[x].activate(tuple(car.distances) + (car.speed,))
            if output[0] == 1 :
                car.rotateleft(temp_angle)
            if output[1] == 1:
                car.rotateright(temp_angle)
            if output[2] == 1:
                car.setpos(delta)
            ge[x].fitness = car.fitness
            if ge[x].fitness > max_fitness:
                max_fitness = ge[x].fitness


        for x in dead[::-1]:
            ge[x].fitness -= 15
            cars.pop(x)
            nets.pop(x)
            ge.pop(x)


        gameobject.update_all(screen, delta, cars)
        if draw_checkpoints:
            Checkpoint.update_all(screen, checkpoints)
        Boundary.update_all(screen, boundaries)
        multlines(f'Gen({gen})\nTime :  {end_time}s\nFitness :  {max_fitness}\nPop :  {len(cars)}', status, 25)
        pg.display.update()
        # root.update()

        if cars == []:
            # root.destroy()
            break


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    winner = p.run(main, 200)
    with open('Winner.txt', 'wb') as w:
        pickle.dump(winner, w)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)