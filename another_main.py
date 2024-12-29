import os
import sys
from math import sin, cos, asin, acos
import pygame

pygame.init()
size = width, height = 1000, 1000
map_size = 10000, 10000
screen = pygame.display.set_mode(size)
center = (width // 2, height // 2)


def scale(image, sizex, sizey):
    return pygame.transform.scale(image, (sizex, sizey))


def rotate(image, angle):
    return pygame.transform.rotate(image, angle)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_music(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Аудиофайл '{fullname}' не найден")
        sys.exit()
    music = pygame.mixer.music.load(fullname)
    return music


class Vector:
    def __init__(self, value=0, angle=0):
        self.value = value
        self.vx, self.vy = self.value * cos(angle), self.value * sin(angle)
        self.angle = angle

    def get_x(self):
        return self.vx

    def get_y(self):
        return self.vy

    def get_xy(self):
        return (self.get_x(), self.get_y())

    def __add__(self, self2):
        vx = self.vx + self2.vx
        vy = self.vy + self2.vy
        v = (vx ** 2 + vy ** 2) ** 0.5
        angle = acos(vx / v)
        return Vector(v, angle)

    def __sub__(self, self2):
        return self + Vector(-self2.value, self2.angle)

    def __mul__(self, k):
        return Vector(self.value * k, self.angle)


class BasedMapObject(pygame.sprite.Sprite):
    def __init__(self, image, vector, pos):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.v = vector
        self.realv = self.v - glvector
        self.t = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.tick = lambda: self.clock.tick()

    def update(self, *args):
        self.t += self.tick() / 1000
        print(self.t)
        self.rect.move(self.realv.get_xy())


class Map(BasedMapObject):
    mapim = scale(load_image("map.jpg"), *map_size)

    def __init__(self):
        super().__init__(Map.mapim, Vector(), center)


class Bomb(BasedMapObject):
    bomb = scale(rotate(load_image("bomb.png"), 225), 100, 100)
    boom = scale(load_image("boom.png"), 100, 100)

    def __init__(self):
        super().__init__(Bomb.bomb, glvector * 0.2, center)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = width // 2, height // 2
        self.flytime = 2
        self.expltime = 2

    def update(self, *args):
        super().update()
        if self.t >= self.flytime:
            self.image = Bomb.boom
            print(0)
        if self.t >= self.flytime + self.expltime:
            del self


pygame.init()
pygame.display.set_caption('BOOM')
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites.draw(screen)
clock = pygame.time.Clock()
glvector = Vector(10, 270)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            btest = Bomb()
    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
