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
    def __init__(self, x, y, width, height, color, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.dw = 5
        self.dh = 5
        self.bcolor = color
        self.d = 30
        self.k1, self.k2 = (max(self.bcolor) - self.d) / max(self.bcolor), (max(self.bcolor) - self.d * 2) / max(self.bcolor)
        print(self.k1, self.k2)
        self.bwidth = width
        self.bheight = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': self.bcolor,
            'hover': tuple([int(i * self.k1) for i in self.bcolor]),
            'pressed': tuple([int(i * self.k2) for i in self.bcolor])
        }
        self.buttonSurface = pygame.Surface((self.bwidth, self.bheight))
        self.buttonRect = pygame.Rect(self.x, self.y, self.bwidth, self.bheight)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        menu.append(self)

    def update(self):
        self.buttonSurface = pygame.Surface((self.bwidth, self.bheight))
        self.buttonRect = pygame.Rect(self.x, self.y, self.bwidth, self.bheight)
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface = pygame.Surface((self.bwidth + self.dw, self.bheight + self.dh))
                self.buttonRect = pygame.Rect(self.x - self.dw, self.y + self.dh, self.bwidth, self.bheight)
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

    def updatetext(self, newtext):
        self.buttonSurf = font.render(newtext, True, (20, 20, 20))


class Label():
    def __init__(self, x, y, width, height, color, labelText='Text'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color
        self.labelSurface = pygame.Surface((self.width, self.height))
        self.labelRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.labelSurf = font.render(labelText, True, (20, 20, 20))
        menu.append(self)

    def update(self):
        self.labelSurface.fill(self.color)
        self.labelSurface.blit(self.labelSurf, [
            self.labelRect.width / 2 - self.labelSurf.get_rect().width / 2,
            self.labelRect.height / 2 - self.labelSurf.get_rect().height / 2
        ])
        screen.blit(self.labelSurface, self.labelRect)


def myFunction():
    print('Button Pressed')


Button(30, 30, 400, 100, (255, 255, 255), 'Button One (onePress)', myFunction)
Label(30, 140, 400, 100, (255, 0, 0), 'Text')
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
