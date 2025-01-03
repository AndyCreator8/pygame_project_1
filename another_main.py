import math
import os
import random
import sys
from math import sin, cos, asin, acos, degrees, radians
import pygame

pygame.init()
size = width, height = 1000, 800
map_size = 10000, 10000
screen = pygame.display.set_mode(size)
center = (width // 2, height // 2)


def posf(targetpos, size):
    return (targetpos[0] - size[0] // 2, targetpos[1] - size[1] // 2)


def scale(image, sizex, sizey):
    return pygame.transform.scale(image, (sizex, sizey))


def rotate(image, angle):
    return pygame.transform.rotate(image, angle)


def load_image(name, path='data', colorkey=None):
    fullname = os.path.join(path, name)
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
        self.vx, self.vy = self.value * cos(radians(angle)), self.value * sin(radians(angle))

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
        angle = degrees(acos(vx / v))
        if vy > 0:
            angle = 360 - angle
        new = Vector(v, angle)
        return new

    def __sub__(self, self2):
        return self + Vector(-self2.value, self2.angle)

    def __mul__(self, k):
        return Vector(self.value * k, self.angle)

    def __str__(self):
        return f"{self.value}, {self.vx}, {self.vy}"

    def findangle(self, self2, mode="cos"):
        vx1, vy1 = self.get_xy()
        vx2, vy2 = self2.get_xy()
        v1, v2 = self.value, self2.value
        cosgamma = (vx1 * vx2 + vy1 * vy2) / (v1 * v2)
        if mode == "cos":
            return cosgamma
        elif mode == "sin":
            return sin(acos(cosgamma))
        elif mode == "angle":
            return degrees(acos(cosgamma))


class BasedMapObject(pygame.sprite.Sprite):
    def __init__(self, image, vector, pos):
        super().__init__(all_sprites)
        self.image = image
        self.pos = pos
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = posf(pos, self.size)
        self.centerpos = pos
        self.v = vector
        self.realv = self.v - plane.vector
        # print(self.realv, type(self))
        self.t = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.tick = lambda: self.clock.tick(60)

    def update(self, *args):
        self.realv = self.v - plane.vector
        self.t += self.tick() / 1000
        # Move object
        self.centerpos = (self.centerpos[0] + int(self.realv.get_x()), self.centerpos[1] + int(self.realv.get_y()))
        self.rect.x, self.rect.y = posf(self.centerpos, self.size)

        # self.rect.x -= plane.vector.vx
        # self.rect.y += plane.vector.vy


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
        self.image = rotate(self.image, (plane.vector.angle + 270) % 360)
        self.bomb = self.image
        self.rect = self.image.get_rect()
        self.rect.move(*self.realv.get_int_xy())
        self.rect.x, self.rect.y = posf(self.pos, self.size)
        self.size = (100, 100)
        self.flytime = 2
        self.expltime = 2

    def update(self, *args):
        super().update()
        if self.t >= self.flytime and self.image == self.bomb:
            self.v = Vector()
            self.image = Bomb.boom
            self.size = (100, 100)
        if self.t >= self.flytime + self.expltime and self.image == Bomb.boom:
            self.image = Bomb.crater
            self.size = (50, 50)


class Rocket(BasedMapObject):
    image = scale(load_image('missile.png'), 23, 110)
    def __init__(self, vector, pos, target):
        self.target = target
        self.orig = self.image
        super().__init__(Rocket.image, vector, pos)
        self.image = pygame.transform.rotate(self.image, vector.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.distance = 3000



    def update(self, *args):
        if self.target:
            x, y = self.rect.centerx, self.rect.centery
            tx, ty = target.rect.centerx, target.rect.centery
            # print(x - tx, y - ty)
            self.image = pygame.transform.rotate(self.orig, self.v.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.v.vx, self.v.vy = self.v.value * cos(
                math.radians(self.v.angle)), self.v.value * sin(math.radians(self.v.angle))
            self.rect.y -= self.v.vx
            self.rect.x -= self.v.vy
        else:
            self.image = pygame.transform.rotate(self.orig, self.v.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.v.vx, self.v.vy = self.v.value * cos(
                math.radians(self.v.angle)), self.v.value * sin(math.radians(self.v.angle))


class Bullet(BasedMapObject):
    image = pygame.Surface((1, 5))

    def __init__(self, vector, pos):
        super().__init__(Bullet.image, vector, pos)
        self.image.fill('white')
        self.orig = self.image

    def update(self):
        self.image = pygame.transform.rotate(self.orig, -self.v.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.v.vx, self.v.vy = self.v.value * cos(
            math.radians(self.v.angle)), self.v.value * sin(math.radians(self.v.angle))
        super().update()
        # self.rect.y -= self.v.vx
        # self.rect.x -= self.v.vy


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player)
        self.image = load_image('0.png','data\plane_1', -1)
        self.animations = []
        self.animations_shoot = []
        for i in range(-3, 4):
            self.animations.append(load_image(f'{i}.png', 'data\plane_1', -1))
            if i != 0:
                self.animations.append(load_image(f'{i}.png', 'data\plane_1', -1))
        for i in range(-3, 4):
            self.animations_shoot.append((load_image(f'{i}.png', 'data\plane_1_shooting', -1), load_image(f'{i} — копия.png', 'data\plane_1_shooting', -1)))
        # self.image = pygame.transform.scale(self.image, (100, 100))
        self.bulletspeed = 20

        self.t = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.tick = lambda: self.clock.tick(60)
        self.deltat = 0

        self.rect = self.image.get_rect()
        self.rect.centerx = center[0]
        self.rect.centery = center[1]

        self.shiftcoef = 1.25
        self.maxspeed = 10
        self.throttle = 1
        self.speed = self.maxspeed * self.throttle
        self.vector = Vector(self.speed, 90)

        self.orig = self.image
        self.animation_sc = 6
        self.prev_t = -5

    def update(self, *args, **kwargs):
        self.deltat = self.tick() / 1000
        self.t += self.deltat
        # print(self.vector)
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            if self.throttle + self.deltat / 10 <= 1:
                self.throttle += self.deltat / 10
        elif key[pygame.K_s]:
            if self.throttle - self.deltat / 10 >= 0.5:
                self.throttle -= self.deltat / 10

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
        self.speed = self.maxspeed * self.throttle
        if key[pygame.K_LSHIFT]:
            self.vector.value = self.speed * self.shiftcoef
        else:
            self.vector.value = self.speed
        self.rect = self.image.get_rect(center=self.rect.center)
        self.vector.vx, self.vector.vy = self.vector.value * cos(
            math.radians(self.vector.angle)), self.vector.value * sin(math.radians(self.vector.angle))
        print(self.vector.vx, self.vector.vy)

        if key[pygame.K_SPACE]:
            Bomb()

        if key[pygame.K_f]:
            if int(map.t) - self.prev_t >= 1:
                Rocket(Vector(20, self.vector.angle - 90), self.rect.center, target)
                self.prev_t = map.t
            else:
                print('Ракета перезаряжаются')

    def fire(self):
        angle_rad = math.radians(-self.vector.angle - 90)
        new_x = self.rect.centerx + (50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
        new_y = self.rect.centery + (50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
        Bullet(Vector(self.bulletspeed, self.vector.angle), (new_x, new_y))
        new_x = self.rect.centerx + (-50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
        new_y = self.rect.centery + (-50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
        Bullet(Vector(self.bulletspeed, self.vector.angle), (new_x, new_y))
        self.image = random.choice(self.animations_shoot[self.animation_sc // 2])
        self.image = pygame.transform.rotate(self.image, self.vector.angle - 90)


class TargetCross(pygame.sprite.Sprite):
    image = scale(load_image("targetcross.png"), 100, 100)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = TargetCross.image
        self.rect = self.image.get_rect()
        self.posvector = plane.vector * 0.2
        self.rect.x, self.rect.y = center[0] + self.posvector.vx, center[1] + self.posvector.vy

    def update(self, *args):
        self.posvector = plane.vector * 0.2
        self.rect.x, self.rect.y = center[0] + self.posvector.vx, center[1] + self.posvector.vy





class Target(BasedMapObject):
    image = scale(load_image('plank.jpeg'), 200, 200)

    def __init__(self):
        super().__init__(Target.image, Vector(), (500, 500))


class Button(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        self.add(all_sprites)
        super().__init__()



pygame.init()
pygame.display.set_caption('BOOM')
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
player = pygame.sprite.Group()

plane = Plane()
tcr = TargetCross()
map = Map()
target = Target()
all_sprites.draw(screen)



clock = pygame.time.Clock()
firing = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            firing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            firing = False
    if firing:
        plane.fire()

    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    player.draw(screen)
    player.update()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()