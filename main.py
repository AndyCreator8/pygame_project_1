import pygame
import sys
from pygame.math import Vector2
import math
from pygame.examples.go_over_there import clock

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 1000, 800
TILE_SIZE = 40  # Размер одной плитки
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Карта в Pygame")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
left = 10
top = -4000
block_sprites = pygame.sprite.Group()
layout = [
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],

]

player_sprite = pygame.sprite.Group()



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_sprite)
        self.image = pygame.image.load('plane_1.png')
        self.image_2 = pygame.image.load('plane_2.png')
        self.image_3 = pygame.image.load('plane_3.png')
        self.size = 255
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.orig = self.image

    # def get_coords(self):
    #     if pygame.sprite.spritecollide(self, block_sprites, False):
    #         target = pygame.sprite.spritecollide(self, block_sprites, False)[0]
    #

    def rotate(self):
        pass

    def update(self, *args, **kwargs):
        xy = pygame.mouse.get_pos() - Vector2(self.rect.x + self.size // 2, self.rect.y + self.size // 2)
        radius, self.angle = xy.as_polar()
        self.image = pygame.transform.rotate(self.orig, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)





player = Player(WIDTH // 2 - 100, HEIGHT // 2 - 100)
class Plain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(block_sprites)
        self.image = pygame.image.load('top_view_1.jpg')
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.rect = self.image.get_rect()
        self.size = 400
        self.rect.x = x
        self.rect.y = y



class Map:
    def __init__(self, layout):
        self.layout = layout
        self.left = left
        self.top = top
        self.cell_size = 400
        self.speed = 20
        for row in range(len(self.layout)):
            for col in range(len(self.layout[0])):
                cell = layout[row][col]
                if cell == 3:
                    block = Plain(col * self.cell_size, row * self.cell_size + top)
                    block_sprites.add(block)


    def move(self):
        keys = pygame.key.get_pressed()
        for i in block_sprites.sprites():
            angle = -player.angle - 90
            print(angle, math.cos(math.radians(angle)), math.sin(math.radians(angle)))
            if round(angle) in range(-360, -90):
                angle += 180
                i.rect.y -= math.cos(math.radians(angle)) * self.speed
                i.rect.x -= math.sin(math.radians(angle)) * self.speed
            else:
                i.rect.y += math.cos(math.radians(angle)) * self.speed
                i.rect.x += math.sin(math.radians(angle)) * self.speed
            # print(math.tanh(angle))
            # if keys[pygame.K_w]:
            #     i.rect.y += 10
            # if keys[pygame.K_s]:
            #     i.rect.y -= 10
            # if keys[pygame.K_a]:
            #     player.image = player.image_2
            #     i.rect.x += 10
            # if keys[pygame.K_d]:
            #     i.rect.x -= 10
# -90 - -360



    # def render(self, screen):
    #     print(self.top)
    #     for row in range(len(self.layout)):
    #         for col in range(len(self.layout[row])):
    #             cell = layout[row][col]
    #             if cell == 3:
    #                 pass

game_map = Map(layout)





# Создание карты


# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    # game_map.render(screen)
    # player.get_coords()
    block_sprites.draw(screen)
    player_sprite.draw(screen)
    player_sprite.update()
    game_map.move()
    clock.tick(30)
    pygame.display.flip()

pygame.quit()
sys.exit()




# rel_x = mouse_x - rect.centerx
#     rel_y = mouse_y - rect.centery
#
#     # Вычисляем угол в радианах и переводим в градусы
#     angle = math.atan2(-rel_y, rel_x)  # Отрицательное значение для правильного направления
#     angle_degrees = math.degrees(angle)
#
#     # Поворачиваем изображение спрайта
#     rotated_image = pygame.transform.rotate(original_image, angle_degrees)