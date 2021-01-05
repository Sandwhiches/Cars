import pygame as pg
import os
from tkinter import *
from random import randint
from car import gameobject
from car import Ray
from boundary import Boundary
from boundary import Checkpoint


def main():
    ### CONFIG
    screen_w = 800
    screen_h = 600
    border_on = False
    num_walls = 0
    num_rays = 4
    angle_diff = 90

    # CAR CONFIG
    rays = []
    rays.append(Ray(0))
    rays.append(Ray(180))
    for i in range(1, num_rays):
        angle = i * 180 / num_rays
        if i %2 == 1:
            rays.append(Ray(angle, 16))
        else:
            rays.append(Ray(angle, 25))
    speed = 0
    speed_cap = 400
    acc = 100
    car = pg.transform.scale(pg.image.load('assets//car.png'), (50, 50))
    car = gameobject(car, 130, 450, angle = 270, speed = speed, acc = acc, speed_cap = speed_cap, vision_rays = rays)

    clock = pg.time.Clock()
    # RACETRACK CONFIG
    click_once = False
    x1, y1 = 0, 0
    x2, y2 = 0, 0

    # tkinter menu
    root = Tk()
    root.geometry('189x600')
    root.geometry('+45+69')
    root.title('configs')

    def save_track(file = 'assets//racetrack.txt'):
        if not checkpoint_mode:
            Boundary.save_boundaries(boundaries, file)
            Ray.boundaries = Boundary.load_boundaries(file)
        else:
            Checkpoint.save_checkpoints(checkpoints)
            Ray.checkpoints = Checkpoint.load_checkpoints()

    def load_track(file = 'assets//racetrack.txt'):
        nonlocal checkpoints
        nonlocal boundaries
        boundaries = Boundary.load_boundaries(file)
        checkpoints = Checkpoint.load_checkpoints()

    def remove_line():
        try:
            if not checkpoint_mode:
                undo.append(boundaries.pop())
                Ray.boundaries = boundaries
            else:
                cundo.append(checkpoints.pop())
                Ray.checkpoints = checkpoints
        except IndexError:
            pass

    def re_add_line():
        try:
            if not checkpoint_mode:
                boundaries.append(undo.pop())
                Ray.boundaries = boundaries
            else:
                checkpoints.append(cundo.pop())
                Ray.checkpoints  = checkpoints
        except IndexError:
            pass

    def switch_mode():
        nonlocal checkpoint_mode
        checkpoint_mode = not checkpoint_mode
        if checkpoint_mode:
            check.set('Checkpoint Mode')
        else:
            check.set('Boundary Mode')

    def draw_checkpoint():
        nonlocal draw_checkpoints
        draw_checkpoints = not draw_checkpoints
        if draw_checkpoints:
            draw.set(f'Draw Checkpints :  ON')
        else:
            draw.set(f'Draw Checkpints :  OFF')

    def ch_custom():
        nonlocal cust
        nonlocal checkpoint_mode
        nonlocal boundaries
        if draw_checkpoints:
            draw_checkpoint()
        checkpoint_mode = False
        cust = not cust
        if cust:
            custom.set('Change back')
            button1.configure(command = lambda: save_track('assets//winner_test_track.txt'))
            button2.configure(command = lambda: load_track('assets//winner_test_track.txt'))
            button5.grid_remove()
            button6.grid_remove()
            try:
                load_track('assets//winner_test_track.txt')
            except:
                boundaries = []
        else:
            custom.set('Change to winner test track')
            button1.configure(command = lambda: save_track())
            button2.configure(command = lambda: load_track())
            button5.grid()
            button6.grid()
            load_track()

    cust = False
    custom = StringVar()
    custom.set('Change to winner test track')
    button = Button(root, textvariable = custom, command = ch_custom)
    button.grid(row = 0, column = 0, sticky = W + E + N + S, ipady = 4)

    button1 = Button(root, text = 'Save Track', command = save_track)
    button1.grid(row = 1, column = 0, sticky = W + E + N + S, ipady = 4)

    button2 = Button(root, text='Load Track', command = load_track)
    button2.grid(row = 2, column= 0, sticky = W + E + N + S, ipady = 4)

    button3 = Button(root, text='Remove Line', command = remove_line, repeatinterval = 150, repeatdelay = 200)
    button3.grid(row = 3, column= 0, sticky = W + E + N + S, ipady = 4)

    button4 = Button(root, text='Undo', command = re_add_line, repeatinterval = 150, repeatdelay = 200)
    button4.grid(row = 3, column= 1, sticky = W + E + N + S, ipady = 4)

    check = StringVar()
    check.set(f'Boundary Mode')
    button5 = Button(root, textvariable = check, command = switch_mode, repeatinterval = 150, repeatdelay = 200)
    button5.grid(row = 4, column= 0, sticky = W + E + N + S, ipady = 4)

    draw = StringVar()
    draw.set(f'Draw Checkpints :  ON')
    button6 = Button(root, textvariable = draw, command = draw_checkpoint, repeatinterval = 150, repeatdelay = 200)
    button6.grid(row = 4, column= 0, sticky = W + E + N + S, ipady = 4)




    # pygame variables
    pg.init()
    screen = pg.display.set_mode((screen_w, screen_h), pg.RESIZABLE)

    running = True
    checkpoints = []
    cundo = []
    checkpoint_mode = False
    draw_checkpoints = True
    boundaries = []
    undo = []
    load_track()


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
                    if not checkpoint_mode:
                        boundaries.append(Boundary(screen, (x1, y1), (x2, y2)))
                        Ray.boundaries = boundaries
                    elif checkpoint_mode:
                        checkpoints.append(Checkpoint(screen, (x1, y1), (x2, y2)))
                        Ray.checkpoints = checkpoints
                    click_once = False

        screen.fill((245,204,77))
        delta = clock.tick(60)/1000
        temp_angle = angle_diff*delta
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            car.rotateleft(temp_angle)

        if keys[pg.K_RIGHT]:
            car.rotateright(temp_angle)

        if keys[pg.K_UP]:
            car.setpos(delta)

        if draw_checkpoints:
            Checkpoint.update_all(screen, checkpoints)
        Boundary.update_all(screen, boundaries)
        car.update(screen, delta)
        # if car.ded:
        #     break
        pg.display.update()
        root.update()
main()
