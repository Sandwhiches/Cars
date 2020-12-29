import pygame as pg
import pickle


class Boundary:
    def __init__(self, screen: pg.display, start: tuple, end: tuple):
        self.start = pg.Vector2(start)
        self.end = pg.Vector2(end)
        self.image = None

    def update(self, screen: pg.display):
        self.image = pg.draw.line(screen, pg.Color('white'), self.start, self.end, 5)

    @staticmethod
    def save_boundaries(boundaries):
        with open('racetrack.txt', 'wb') as f:
            pickle.dump(boundaries, f)

    @staticmethod
    def load_boundaries():
        with open('racetrack.txt', 'rb') as f:
            boundaries = pickle.load(f)
        return boundaries
