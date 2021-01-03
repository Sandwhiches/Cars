import pygame as pg
import math

class gameobject():
    def __init__(self, image, x: int, y: int, angle: int, speed: int, acc: int, speed_cap: int, vision_rays: list):
        self.x = x
        self.y = y
        self.image = image
        self.rotated_image = self.image
        self.angle = angle
        self.speed = speed
        self.acc = acc
        self.speed_cap = speed_cap
        self.rays = vision_rays
        for ray in self.rays:
            ray.player = self
        self.distances: list = []
        self.status = False
        self.delta = 1
        self.place = 0
        self.fitness = 0
        self.distances = [232.1820256396821, 83.45159946065338, 270.00023021719556, 155.84132183618638, 95.52866196664567]
        self.ded = False

    @staticmethod
    def update_all(screen: pg.display, delta: float, cars: list):
        for car in cars:
            car.update(screen, delta)


    def rotateright(self, angle_diff: float):
        self.angle -= angle_diff
        self.angle %= 360
        Ray.rotate_rays(angle_diff, self.rays)

    def rotateleft(self, angle_diff: float):
        self.angle += angle_diff
        self.angle %= 360
        Ray.rotate_rays(-angle_diff, self.rays)

    def setpos(self, delta: float):
        acc = self.acc*delta
        self.speed += acc
        if self.speed > self.speed_cap:
            self.speed = self.speed_cap
        speed = self.speed*delta
        self.x += speed*(math.cos(math.radians(self.angle)))
        self.y -= speed*(math.sin(math.radians(self.angle)))
        self.status = True

    def deacc(self, delta: float):
        acc = self.acc*delta
        if self.speed > 0:
            self.speed -= 2*acc
        if self.speed < 0:
            self.speed = 0
        if self.speed == 0:
            # self.fitness -= 1
            self.ded = True
            return
        speed = self.speed*delta
        self.x += speed*(math.cos(math.radians(self.angle)))
        self.y -= speed*(math.sin(math.radians(self.angle)))

    def update(self, screen: pg.display, delta: float):
        if not self.status:
            self.deacc(delta)
        start = pg.Vector2(self.x, self.y)
        self.distances = Ray.update_all(screen, self.rays, start)
        if not all(self.distances):
            self.ded = True
        self.rays[2].pass_checkpoint(start)
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        screen.blit(self.rotated_image, (self.x - int(self.rotated_image.get_width()/2), self.y - int(self.rotated_image.get_height()/2)))
        self.status = False


from boundary import Boundary
from boundary import Checkpoint

drawline = pg.draw.line
class Ray:
    boundaries = Boundary.load_boundaries()
    checkpoints = Checkpoint.load_checkpoints()
    draw_rays = False
    def __init__(self, heading: float = 0, crash: int = -1, player: gameobject = None):
        self.heading = heading
        self.end: pg.math.Vector2 = pg.math.Vector2()
        self.image = None
        self.crash = crash
        self.player = player

    def pass_checkpoint(self, start: pg.Vector2):
        self.start = start
        self.end.from_polar((100000, self.heading))

        closest = float("inf")
        new_end = pg.Vector2()

        x3 = self.start.x
        x4 = self.end.x
        y3 = self.start.y
        y4 = self.end.y

        checkpoint = Ray.checkpoints[self.player.place]
        x1 = checkpoint.start.x
        x2 = checkpoint.end.x
        y1 = checkpoint.start.y
        y2 = checkpoint.end.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return

        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        t = t_num / den
        u_num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))
        u = u_num / den

        if u >= 0 and 0 <= t <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            dist = self.start.distance_to((x, y))
            if dist <= self.crash:
                self.player.fitness += 5
                self.player.place += 1
                if self.player.place == len(Ray.checkpoints):
                    self.player.place = 0


    @staticmethod
    def rotate_rays(diff: float, rays: list):
        for ray in rays:
            ray.heading += diff
            ray.heading %= 360

    @staticmethod
    def update_all(screen: pg.display, rays: list, start: pg.Vector2):
        dist = []
        for ray in rays:
            dist.append(ray.update(screen, start))
        return dist

    def update(self, screen: pg.display, start: pg.Vector2):
        self.start = start
        self.end.from_polar((100000, self.heading))

        closest = float("inf")
        new_end = pg.Vector2()

        x3 = self.start.x
        x4 = self.end.x
        y3 = self.start.y
        y4 = self.end.y

        for b in Ray.boundaries:
            x1 = b.start.x
            x2 = b.end.x
            y1 = b.start.y
            y2 = b.end.y

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                return

            t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
            t = t_num / den
            u_num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))
            u = u_num / den

            if u >= 0 and 0 <= t <= 1:
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                dist = self.start.distance_to((x, y))
                if dist < closest:
                    closest = dist
                    new_end.xy = x, y

        if closest == float("inf"):
            if Ray.draw_rays:
                self.image = drawline(screen, (255, 0, 0),  self.start, self.end)
        else:
            self.end = new_end
            if Ray.draw_rays:
                self.image = drawline(screen, (255, 0, 0),  self.start, self.end)
            if closest <= self.crash:
                if self.player.fitness == 0:
                    self.player.fitness -= 100
                self.player.fitness -= 15
                self.player.ded = True
                return False
            return closest
