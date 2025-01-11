# Imports
import sys
import pygame

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = screen.get_size()
in_game = True
paused = False
center = centery, centerx = (width // 2, height // 2)
print(pygame.font.get_fonts())

menu = []
clocks = []


def play(era, level, playerparams=None):
    pass


class Clock:
    def __init__(self, fps):
        clocks.append(self)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.t = 0

    def update(self):
        dt = self.clock.tick(self.fps) / 1000
        self.t += dt

    def get_clock(self):
        return Clock(self.fps)

    def time(self):
        return self.t


def wait(time):
    cl = pygame.time.wait(int(time * 1000))


def load_erachoice():
    wait(0.125)
    global menu
    menu = []
    era1color, era1size, era1pos, era1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "ERA I"
    era1 = Button(*posf(era1pos, era1size), *era1size, color=era1color, buttonText=era1text,
                  onclickFunction=load_era1lvls, onePress=True, fontsize=75, bold=True)

    era2color, era2size, era2pos, era2text = (128, 0, 0), (400, 100), (width // 2, height // 2), "ERA II"
    era2 = Button(*posf(era2pos, era2size), *era2size, color=era2color, buttonText=era2text,
                  onclickFunction=load_era2lvls, onePress=True, fontsize=75, bold=True)

    era3color, era3size, era3pos, era3text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "ERA III"
    era3 = Button(*posf(era3pos, era3size), *era3size, color=era3color, buttonText=era3text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)


def load_era1lvls():
    wait(0.125)
    global menu
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 240), "LEVEL I"
    lvl1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl2color, lvl2size, lvl2pos, lvl2text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "LEVEL I"
    lvl2 = Button(*posf(lvl2pos, lvl2size), *lvl2size, color=lvl2color, buttonText=lvl2text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl3color, lvl3size, lvl3pos, lvl3text = (128, 0, 0), (400, 100), (width // 2, height // 2), "LEVEL I"
    lvl3 = Button(*posf(lvl3pos, lvl3size), *lvl3size, color=lvl3color, buttonText=lvl3text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl4color, lvl4size, lvl4pos, lvl4text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "LEVEL I"
    lvl4 = Button(*posf(lvl4pos, lvl4size), *lvl4size, color=lvl4color, buttonText=lvl4text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl5color, lvl5size, lvl5pos, lvl5text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 240), "LEVEL I"
    lvl5 = Button(*posf(lvl5pos, lvl5size), *lvl5size, color=lvl5color, buttonText=lvl5text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)


def load_era2lvls():
    wait(0.125)
    global menu
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 240), "LEVEL I"
    lvl1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl2color, lvl2size, lvl2pos, lvl2text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "LEVEL I"
    lvl2 = Button(*posf(lvl2pos, lvl2size), *lvl2size, color=lvl2color, buttonText=lvl2text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl3color, lvl3size, lvl3pos, lvl3text = (128, 0, 0), (400, 100), (width // 2, height // 2), "LEVEL I"
    lvl3 = Button(*posf(lvl3pos, lvl3size), *lvl3size, color=lvl3color, buttonText=lvl3text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl4color, lvl4size, lvl4pos, lvl4text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "LEVEL I"
    lvl4 = Button(*posf(lvl4pos, lvl4size), *lvl4size, color=lvl4color, buttonText=lvl4text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)

    lvl5color, lvl5size, lvl5pos, lvl5text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 240), "LEVEL I"
    lvl5 = Button(*posf(lvl5pos, lvl5size), *lvl5size, color=lvl5color, buttonText=lvl5text,
                  onclickFunction=load_ingameui, onePress=True, fontsize=75, bold=True)


def posf(targetpos, size):
    return (targetpos[0] - size[0] // 2, targetpos[1] - size[1] // 2)


def load_menu():
    wait(0.125)
    global menu, in_game
    in_game = False
    menu = []
    playcolor, playsize, playpos, playtext = (128, 0, 0), (500, 200), (width // 2, height // 2 - 110), "PLAY"
    play = Button(*posf(playpos, playsize), *playsize, color=playcolor, buttonText=playtext,
                  onclickFunction=load_erachoice, onePress=True, fontsize=75, bold=True)
    exitcolor, exitsize, exitpos, exittext = (128, 0, 0), (500, 200), (width // 2, height // 2 + 110), "EXIT"
    exit = Button(*posf(exitpos, exitsize), *exitsize, color=exitcolor, buttonText=exittext,
                  onclickFunction=pygame.quit, onePress=True, fontsize=75, bold=True)


def pause_game():
    wait(0.125)
    global menu
    menu = []
    backcolor, backsize, backpos, backtext = (128, 0, 0), (500, 200), (width // 2, height // 2 - 110), "CONTINUE?"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=load_ingameui,
                  onePress=True, fontsize=75, bold=True)
    exittomenucolor, exittomenusize, exittomenupos, exittomenutext = (128, 0, 0), (500, 200), (
    width // 2, height // 2 + 110), "MAIN MENU"
    exittomenu = Button(*posf(exittomenupos, exittomenusize), *exittomenusize, color=exittomenucolor,
                        buttonText=exittomenutext,
                        onclickFunction=load_menu,
                        onePress=True, fontsize=75, bold=True)
    # exittomenu.update()


def load_ingameui():
    global menu, params, boolparams, in_game
    in_game = True
    menu = []
    # titlecolor, titlesize, titlepos, titletext = (128, 0, 0), (500, 200), (width // 2, 150), "VOLAR"
    # title = Label(*posf(titlepos, titlesize), *titlesize, color=titlecolor, labelText=titletext)
    # title.update()

    menucolor, menusize, menupos, menutext = (128, 0, 0), (100, 100), (width - 75, 75), "II"
    menubtn = Button(*posf(menupos, menusize), *menusize, color=menucolor, buttonText=menutext,
                     onclickFunction=pause_game, onePress=True, fontsize=75, bold=True)
    # menubtn.update()
    if boolparams:
        x, y = width - 200, 150
        prcolor, prfontsize, prh = (255, 255, 255), 40, 100
        for i in params:
            y += prh
            # print(y)
            Text((x, y), f"{i}: {params[i]}", fontsize=prfontsize, fontcolor=prcolor)


class Button():
    def __init__(self, x, y, width, height, color, buttonText='Button', onclickFunction=None, onePress=False,
                 onclickParams=0, fontsize=30, bold=False, fontname="Arial"):
        self.bold = bold
        self.font = pygame.font.SysFont(fontname, fontsize, bold=self.bold)
        self.x = x
        self.y = y
        self.dw = 5
        self.dh = 5
        self.bcolor = color
        self.d = 30
        self.k1, self.k2 = (max(self.bcolor) - self.d) / max(self.bcolor), (max(self.bcolor) - self.d * 2) / max(
            self.bcolor)
        # print(self.k1, self.k2)
        self.bwidth = width
        self.bheight = height
        self.onclickParams = onclickParams
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

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))
        menu.append(self)

    def update(self):
        self.buttonSurface = pygame.Surface((self.bwidth, self.bheight))
        self.buttonRect = pygame.Rect(self.x, self.y, self.bwidth, self.bheight)
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface = pygame.Surface((self.bwidth + self.dw * 2, self.bheight + self.dh * 2))
                self.buttonRect = pygame.Rect(self.x - self.dw, self.y - self.dh, self.bwidth + self.dw,
                                              self.bheight + self.dh)
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    if self.onclickParams:
                        self.onclickFunction(**self.onclickParams)
                    else:
                        self.onclickFunction()
                elif not self.alreadyPressed:
                    if self.onclickParams:
                        self.onclickFunction(**self.onclickParams)
                    else:
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
        self.buttonSurf = self.font.render(newtext, True, (20, 20, 20))


class Text:
    def __init__(self, pos, text, fontsize, bold=False, fontname="Arial", fontcolor=(0, 0, 0)):
        menu.append(self)
        self.pos = pos
        self.fontcolor = fontcolor
        self.font = pygame.font.SysFont(fontname, fontsize, bold=bold)
        self.surf = self.font.render(text, True, self.fontcolor)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = posf(self.pos, self.surf.get_size())
        # print(self.rect.x, self.rect.y)

    def change_text(self, text):
        self.surf = self.font.render(text, True, self.fontcolor)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = posf(self.pos, self.surf.get_size())
        print(self.rect.x, self.rect.y)

    def update(self):
        screen.blit(self.surf, self.rect)


# Button(30, 30, 400, 100, (255, 255, 255), 'Button One (onePress)', myFunction)
# Text((500, 500), "Caramba!", bold=True, fontsize=100, fontcolor=(255, 255, 255))
t = Clock(30)
boolparams = True
params = {"SPEED": 100, "Debils": 1, "Which one?": "Me!"}
load_ingameui()

print(menu)
print(clocks)
while True:
    screen.fill((20, 20, 20))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE and in_game:
            if paused:
                load_ingameui()
            else:
                pause_game()
            paused = not paused
            # Maybe
            boolparams = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_TAB:
            print("tab changed")
            boolparams = not boolparams
            load_ingameui()
    screen.fill((0, 0, 0))
    for object in menu:
        object.update()
    for object in clocks:
        object.update()
    pygame.display.flip()
    fpsClock.tick(fps)
