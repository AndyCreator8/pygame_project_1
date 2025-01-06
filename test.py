# Imports
import sys
import pygame

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 40)

menu = []


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        menu.append(self)

    def update(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


class Label():
    def __init__(self, x, y, width, height, labelText='Text'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.labelSurface = pygame.Surface((self.width, self.height))
        self.labelRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.labelSurf = font.render(labelText, True, (20, 20, 20))
        menu.append(self)

    def update(self):
        self.labelSurface.fill(self.fillColors['normal'])
        self.labelSurface.blit(self.labelSurf, [
            self.labelRect.width / 2 - self.labelSurf.get_rect().width / 2,
            self.labelRect.height / 2 - self.labelSurf.get_rect().height / 2
        ])
        screen.blit(self.labelSurface, self.labelRect)


def myFunction():
    print('Button Pressed')


Button(30, 30, 400, 100, 'Button One (onePress)', myFunction)
Label(30, 140, 400, 100, 'Text')
while True:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for object in menu:
        object.update()
    pygame.display.flip()
    fpsClock.tick(fps)
