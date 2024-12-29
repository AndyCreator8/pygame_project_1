import pygame
import math
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поворот персонажа")

# Цвета
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('plane_1.png').convert_alpha()  # Замените на путь к вашему изображению
        self.orig_image = self.image  # Сохраняем оригинальное изображение
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.last_update = pygame.time.get_ticks()  # Время последнего обновления
        self.update_interval = 100  # Интервал обновления в миллисекундах

    def update(self):
        # Получаем координаты курсора мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()
        xy = pygame.math.Vector2(mouse_x, mouse_y) - pygame.math.Vector2(self.rect.center)

        # Вычисляем угол поворота
        target_angle = math.degrees(math.atan2(-xy.y, xy.x)) - 90

        now = pygame.time.get_ticks()
        if now - self.last_update > self.update_interval:
            self.last_update = now

            # Поворачиваем изображение спрайта
            self.angle = target_angle
            self.image = pygame.transform.rotate(self.orig_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

clock = pygame.time.Clock()
# Создаем игрока
player = Player(WIDTH // 2, HEIGHT // 2)

# Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление игрока и отрисовка на экране
    player.update()

    screen.fill(WHITE)  # Очистка экрана белым цветом
    player.draw(screen)  # Отрисовка игрока
    clock.tick(60)
    pygame.display.flip()  # Обновление экрана

pygame.quit()
sys.exit()