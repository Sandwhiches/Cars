import pygame as pg
import pickle


class Boundary:
    def __init__(self, screen: pg.display, start: tuple, end: tuple):
        self.start = pg.Vector2(start)
        self.end = pg.Vector2(end)
        self.image = None

    def update(self, screen: pg.display):
        self.image = pg.draw.line(screen, (0, 0, 0), self.start, self.end, 5)

    @staticmethod
    def save_boundaries(boundaries: list):
        with open('racetrack.txt', 'wb') as f:
            pickle.dump(boundaries, f)

    @staticmethod
    def load_boundaries():
        with open('racetrack.txt', 'rb') as f:
            boundaries = pickle.load(f)
        return boundaries

    @staticmethod
    def update_all(screen: pg.display, boundaries: list):
        for boundary in boundaries:
            boundary.update(screen)

class Checkpoint(Boundary):
    def init(self, screen: pg.display, start: tuple, end: tuple):
        super().__init__(screen, start, end)

    def update(self, screen: pg.display):
        self.image = pg.draw.line(screen, (150, 255, 150), self.start, self.end, 3)

    @staticmethod
    def save_checkpoints(checkpoints: list):
        with open('checkpoint.txt', 'wb') as f:
            pickle.dump(checkpoints, f)

    @staticmethod
    def load_checkpoints():
        with open('checkpoint.txt', 'rb') as f:
            checkpoints = pickle.load(f)
        return checkpoints