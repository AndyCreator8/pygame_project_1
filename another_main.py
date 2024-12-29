import math
import os
import sys
from math import sin, cos, asin, acos
import pygame

pygame.init()
size = width, height = 1000, 1000
map_size = 10000, 10000
screen = pygame.display.set_mode(size)
center = (width // 2, height // 2)


def posf(targetpos, size):
    return (targetpos[0] - size[0] // 2, targetpos[1] - size[1] // 2)


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
        self.angle = angle
        self.vx, self.vy = self.value * cos(math.radians(angle)), self.value * sin(math.radians(angle))

    def get_x(self):
        return self.vx

    def get_y(self):
        return self.vy

    def get_xy(self):
        return (self.get_x(), self.get_y())

    def get_int_xy(self):
        return (int(self.get_x()), int(self.get_y()))

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

    def __str__(self):
        return f"{self.value}, {self.vx}, {self.vy}"


class BasedMapObject(pygame.sprite.Sprite):
    def __init__(self, image, vector, pos):
        super().__init__(all_sprites)
        self.image = image
        self.pos = pos
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = posf(pos, self.size)
        self.v = vector
        self.realv = self.v - plane.vector
        print(self.realv, type(self))
        self.t = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.tick = lambda: self.clock.tick()

    def update(self, *args):
        self.t += self.tick() / 1000
        self.rect.x -= plane.vector.vx
        self.rect.y += plane.vector.vy
        print(plane.vector.vx)


class Map(BasedMapObject):
    mapim = scale(load_image("map.jpg"), *map_size)

    def __init__(self):
        super().__init__(Map.mapim, Vector(), center)


class Bomb(BasedMapObject):
    bomb = scale(rotate(load_image("bomb.png"), 225), 100, 100)
    boom = scale(load_image("boom.png"), 100, 100)
    crater = scale(load_image("crater.webp"), 50, 50)

    def __init__(self):
        super().__init__(Bomb.bomb, plane.vector * 0.2, center)
        self.rect = self.image.get_rect()
        self.rect.move(*self.realv.get_int_xy())
        self.rect.x, self.rect.y = posf(self.pos, self.size)
        self.size = (100, 100)
        self.flytime = 2
        self.expltime = 2

    def update(self, *args):
        if self.t >= self.flytime and self.image == Bomb.bomb:
            self.image = Bomb.boom
            self.size = (100, 100)
        if self.t >= self.flytime + self.expltime and self.image == Bomb.boom:
            self.image = Bomb.crater
            self.size = (50, 50)

        super().update()


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player)
        self.image = load_image('0.png', -1)
        self.animations = []
        for i in range(-3, 4):
            self.animations.append(load_image(f'{i}.png', -1))
            if i != 0:
                self.animations.append(load_image(f'{i}.png', -1))
        # self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = center[0]
        self.rect.centery = center[1]
        self.vector = Vector(10, 90)
        self.orig = self.image
        self.animation_sc = 6

    def update(self, *args, **kwargs):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.vector.angle += 4 - self.animation_sc // 2
            self.animation_sc -= 1 if self.animation_sc > 0 else 0
            self.image = self.animations[self.animation_sc]
            self.image = pygame.transform.rotate(self.animations[self.animation_sc], self.vector.angle - 90)
        elif key[pygame.K_d]:
            self.vector.angle -= self.animation_sc // 4
            self.animation_sc += 1 if self.animation_sc < 12 else 0
            self.image = self.animations[self.animation_sc]
            self.image = pygame.transform.rotate(self.animations[self.animation_sc], self.vector.angle - 90)
        else:
            self.image = self.orig
            if self.animation_sc < 6:
                self.animation_sc += 1
            elif self.animation_sc > 6:
                self.animation_sc -= 1
            self.image = pygame.transform.rotate(self.animations[self.animation_sc], self.vector.angle - 90)
        if key[pygame.K_LSHIFT]:
            self.vector.value = 15
        else:
            self.vector.value = 10
        self.rect = self.image.get_rect(center=self.rect.center)
        self.vector.vx, self.vector.vy = self.vector.value * cos(
            math.radians(self.vector.angle)), self.vector.value * sin(math.radians(self.vector.angle))


pygame.init()
pygame.display.set_caption('BOOM')
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

all_sprites.draw(screen)
player = pygame.sprite.Group()
plane = Plane()
Map()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            btest = Bomb()

    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    player.draw(screen)
    player.update()
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
