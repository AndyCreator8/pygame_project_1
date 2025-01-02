import math
import os
import random
import sys
from math import sin, cos, asin, acos, degrees, radians
import pygame

pygame.init()
size = width, height = 1000, 800
map_size = 1000, 1000
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
        angle = acos(vx / v)
        return Vector(v, degrees(angle))

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
        self.v = vector
        self.realv = self.v - plane.vector
        # print(self.realv, type(self))
        self.t = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.tick = lambda: self.clock.tick(60)

    def update(self, *args):
        self.t += self.tick() / 10
        self.rect.x -= plane.vector.vx
        self.rect.y += plane.vector.vy





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


class Rocket(pygame.sprite.Sprite):
    image = scale(load_image('missile.png'), 23, 110)
    def __init__(self, vector, pos, target):
        self.target = target
        self.orig = self.image
        self.explosion_imgs = [load_image(f'{i // 2}.png', 'data\explosion_animation', -1) for i in range(22)]
        super().__init__(rockets)
        self.killed = False
        self.animation_sc = 0
        self.image = pygame.transform.rotate(self.image, vector.angle)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x, self.rect.y = posf(pos, self.size)
        self.v = vector
        self.distance = 3000
        self.v.vx, self.v.vy = self.v.value * sin(
            math.radians(self.v.angle)), self.v.value * cos(math.radians(self.v.angle))
        self.tv = self.rect.centerx - self.target.rect.centerx, self.rect.centery - self.target.rect.centery
        self.mod_a = (self.v.vx ** 2 + self.v.vy ** 2) ** 0.5
        self.mod_b = (self.tv[0] ** 2 + self.tv[1] ** 2) ** 0.5
        self.pr = self.v.vx * self.tv[0] + self.v.vy * self.tv[1]
        self.angle = self.pr / (self.mod_a * self.mod_b)
        if self.angle < 0:
            self.angle = -math.degrees(math.acos(self.angle))
        else:
            self.angle = math.degrees(math.acos(self.angle))
        print(self.angle)





    def update(self, *args):
        if self.killed is False:
            direction = pygame.math.Vector2(target.rect.center) - pygame.math.Vector2(self.rect.center)
            self.angle = math.degrees(math.atan2(-direction.y, direction.x))
            if self.v.angle > self.angle - 90:
                self.v.angle -= 5
            else:
                self.v.angle += 5
            # self.v.angle = self.angle - 90
            print(self.angle)
            self.v.vx, self.v.vy = self.v.value * sin(
                math.radians(self.v.angle)), self.v.value * cos(math.radians(self.v.angle))

            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect.y -= self.v.vy
            self.rect.x -= self.v.vx
            self.distance -= abs(self.v.vy)
            self.distance -= abs(self.v.vx)
            if self.distance <= 0:
                self.kill()
            self.image = pygame.transform.rotate(self.orig, self.v.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            if pygame.sprite.spritecollideany(self, blocks):
                self.killed = True
        else:
            self.explotion()

    def explotion(self):
        self.image = self.explosion_imgs[self.animation_sc]
        self.animation_sc += 1
        self.rect.x -= plane.vector.vx
        self.rect.y += plane.vector.vy
        if self.animation_sc == 22:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    image = pygame.Surface((1, 5))
    def __init__(self, vector, pos):
        self.v = vector
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x, self.rect.y = posf(pos, self.size)
        super().__init__(bullets)
        self.image.fill('red')
        self.orig = self.image
        self.explosion_imgs = [scale(load_image(f'{i // 2}.png', 'data\explosion_animation', -1), 20, 20) for i in range(22)]
        self.animation_sc = 0
        self.killed = False

    def update(self):
        if self.killed is False:
            self.image = pygame.transform.rotate(self.orig, -self.v.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.v.angle += random.choice(range(-3, 4))
            self.v.vx, self.v.vy = self.v.value * sin(
                math.radians(self.v.angle)), self.v.value * cos(math.radians(self.v.angle))
            self.rect.y -= self.v.vy
            self.rect.x -= self.v.vx
            if pygame.sprite.spritecollideany(self, blocks):
                self.killed = True
        else:
            self.explosion()

    def explosion(self):
        self.image = self.explosion_imgs[self.animation_sc]
        self.animation_sc += 1
        self.rect.x -= plane.vector.vx
        self.rect.y += plane.vector.vy
        if self.animation_sc == 22:
            self.kill()


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
        self.rect = self.image.get_rect()
        self.rect.centerx = center[0]
        self.rect.centery = center[1]
        self.vector = Vector(10, 90)
        self.orig = self.image
        self.animation_sc = 6
        self.fire_rate = -1
        self.prev_t = -5

    def update(self, *args, **kwargs):
        # print(self.vector)
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
        if key[pygame.K_SPACE]:
            if int(map.t) - self.fire_rate >= 10:
                angle_rad = math.radians(-self.vector.angle - 90)
                new_x = self.rect.centerx + (50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
                new_y = self.rect.centery + (50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(20, self.vector.angle - 90), (new_x, new_y))
                new_x = self.rect.centerx + (-50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
                new_y = self.rect.centery + (-50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(20, self.vector.angle - 90), (new_x, new_y))
                self.image = random.choice(self.animations_shoot[self.animation_sc // 2])
                self.image = pygame.transform.rotate(self.image, self.vector.angle - 90)
                self.fire_rate = map.t


        if key[pygame.K_f]:
            if int(map.t) - self.prev_t  >= 100:
                Rocket(Vector(20, self.vector.angle - 90), self.rect.center, target)
                self.prev_t = map.t
            else:
                print('Ракета перезаряжаются')






class Target(BasedMapObject):
    image = scale(load_image('plank.jpeg'), 200, 200)

    def __init__(self):
        super().__init__(Target.image, Vector(), (500, 500))


pygame.init()
pygame.display.set_caption('BOOM')
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = pygame.sprite.Group()
rockets = pygame.sprite.Group()
plane = Plane()
map = Map()
target = Target()
blocks.add(target)

all_sprites.draw(screen)



clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            btest = Bomb()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    rockets.draw(screen)
    rockets.update()
    player.draw(screen)
    player.update()
    bullets.draw(screen)
    bullets.update()
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
