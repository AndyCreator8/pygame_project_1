import json
import math
import os
import random
import sys
from math import sin, cos, acos, degrees, radians
import pygame
import screeninfo
pygame.init()
map_size = 10000, 10000
for monitor in screeninfo.get_monitors():
    screen = pygame.display.set_mode((monitor.width, monitor.height), pygame.FULLSCREEN)
    break
size = width, height = screen.get_size()
center = (width // 2, height // 2)
font = pygame.font.Font(None, 40)
in_game = False
paused = True
boolparams = True
params = {}
menu = []
results = {
    "Planes destroyed": 0,
    "Ground targets destroyed": 0,
    "Damage dealt": 0,
    "Damage taken": 0,
    "Time survived": 0,
    "status": "DRAW"
}
era2, level2 = 1, 1

with open('data/planes.json', 'r', encoding='utf8') as file:
    planes = json.load(file)
print(f'Выберите самолет:')
for j, i in enumerate(planes):
    print(j + 1, i)
# chosen_plane = planes[list(planes.keys())[int(input()) - 1]]


class Clock:
    def __init__(self, fps):
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


def load_game(era, level, chosen_plane):
    global planes, map, tcr, target, r, plane, in_game, paused, t, era2, level2
    era2, level2 = era, level
    t = 0
    in_game = True
    paused = False
    if era == 1:
        i = 4, 2, 7
    elif era == 2:
        i = 0, 5, 7
    else:
        i = 3, 1
    chosen_plane = planes[chosen_plane]
    print(chosen_plane)
    enemytypes = [[], [4, 2, 7], [0, 5, 7], [1, 3]]
    plane = Plane(**chosen_plane)
    map = Map()
    tcr = TargetCross()
    target = Target()
    r = Radar(range=4000, rtspeed=3 + era)
    enemiesc = level
    enemyvars = enemytypes[era]
    print(enemyvars)
    for i in range(enemiesc):
        j = random.choice(enemyvars)
        print(j)
        Enemy(0, (random.choice(range(-4000, 4000)), random.choice(range(-4000, 4000))), **planes[list(planes.keys())[j]])
    #enemy1 = Enemy(0, (1000, 1000), *planes[random.choice(list(planes.keys()))].values())
    # enemy2 = Enemy(90, (0, 0), *planes[random.choice(list(planes.keys()))].values())
    #enemy2 = Enemy(90, (0, 0), *planes[random.choice(list(planes.keys()))].values())


def load_results():
    global results, enemies, targets, plane, planes_sprites, all_sprites, in_game, t, width, height, paused, menu, era2, level2, player, radar
    all_sprites = pygame.sprite.Group()
    player = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    planes_sprites = pygame.sprite.Group()
    radar = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    menu = []
    plane.mgsnd.stop()
    plane.sound.stop()
    if not in_game:
        return None
    paused = True
    for i in enemies.sprites():
        results["Damage dealt"] += i.dmgtkn
    for i in targets.sprites():
        results["Damage dealt"] += i.dmgtkn
    results["Damage taken"] = plane.maxhealth - plane.health
    results["Time survived"] = round(t, 2)

    titlepos, titlecolor, titlefontsize = (width // 2, height // 2 - 600), (255, 255, 255), 75
    title = Text(titlepos, f"A STORM ON A HOT DAY", fontsize=titlefontsize, fontcolor=titlecolor, bold=True)

    stpos, stcolor, stfontsize = (width // 2, height // 2 - 350), (255, 255, 255), 150
    st = Text(stpos, f"{results['status']}", fontsize=stfontsize, fontcolor=stcolor)

    pdpos, pdcolor, pdfontsize = (width // 2, height // 2 - 200), (255, 255, 255), 75
    pd = Text(pdpos, f"Planes destroyed: {results['Planes destroyed']}", fontsize=pdfontsize, fontcolor=pdcolor)

    gtdpos, gtdcolor, gtdfontsize = (width // 2, height // 2 - 100), (255, 255, 255), 75
    gtd = Text(gtdpos, f"Ground targets destroyed: {results['Ground targets destroyed']}", fontsize=gtdfontsize, fontcolor=gtdcolor)

    ddpos, ddcolor, ddfontsize = (width // 2, height // 2), (255, 255, 255), 75
    dd = Text(ddpos, f"Damage dealt: {results['Damage dealt']}", fontsize=ddfontsize,
               fontcolor=ddcolor)

    dtpos, dtcolor, dtfontsize = (width // 2, height // 2 + 100), (255, 255, 255), 75
    dt = Text(dtpos, f"Damage taken: {results['Damage taken']}", fontsize=dtfontsize,
              fontcolor=dtcolor)

    dtpos, dtcolor, dtfontsize = (width // 2, height // 2 + 200), (255, 255, 255), 75
    dt = Text(dtpos, f"Time survived: {results['Time survived']}", fontsize=dtfontsize,
              fontcolor=dtcolor)

    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=load_menu, onePress=True, fontsize=75, bold=True)

    retrycolor, retrysize, retrypos, retrytext = (128, 0, 0), (300, 100), (width - 175, height - 75), "RETRY"
    retry = Button(*posf(retrypos, retrysize), *retrysize, color=retrycolor, buttonText=retrytext,
                  onclickFunction=load_game, onclickParams={"era": era2, "level": level2, "chosen_plane": plane.name}, onePress=True, fontsize=75, bold=True)


def load_erachoice():
    wait(0.125)
    global menu
    menu = []
    era1color, era1size, era1pos, era1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "WW1"
    era1 = Button(*posf(era1pos, era1size), *era1size, color=era1color, buttonText=era1text,
                  onclickFunction=select_plane_for_1_era, onePress=True, fontsize=75, bold=True)

    era2color, era2size, era2pos, era2text = (128, 0, 0), (400, 100), (width // 2, height // 2), "WW2"
    era2 = Button(*posf(era2pos, era2size), *era2size, color=era2color, buttonText=era2text,
                  onclickFunction=select_plane_for_2_era, onePress=True, fontsize=75, bold=True)

    era3color, era3size, era3pos, era3text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "COLD WAR"
    era3 = Button(*posf(era3pos, era3size), *era3size, color=era3color, buttonText=era3text,
                  onclickFunction=select_plane_for_3_era, onePress=True, fontsize=75, bold=True)

    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=load_menu, onePress=True, fontsize=75, bold=True)


def load_era1lvls(chosen_plane):
    wait(0.125)
    global menu
    chosen_plane = chosen_plane
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 240), "LEVEL I"
    lvl1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_game, onclickParams={"era":1, "level":1, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl2color, lvl2size, lvl2pos, lvl2text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "LEVEL II"
    lvl2 = Button(*posf(lvl2pos, lvl2size), *lvl2size, color=lvl2color, buttonText=lvl2text,
                  onclickFunction=load_game, onclickParams={"era":1, "level":2, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl3color, lvl3size, lvl3pos, lvl3text = (128, 0, 0), (400, 100), (width // 2, height // 2), "LEVEL III"
    lvl3 = Button(*posf(lvl3pos, lvl3size), *lvl3size, color=lvl3color, buttonText=lvl3text,
                  onclickFunction=load_game, onclickParams={"era":1, "level":3, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl4color, lvl4size, lvl4pos, lvl4text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "LEVEL IV"
    lvl4 = Button(*posf(lvl4pos, lvl4size), *lvl4size, color=lvl4color, buttonText=lvl4text,
                  onclickFunction=load_game, onclickParams={"era":1, "level":4, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl5color, lvl5size, lvl5pos, lvl5text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 240), "LEVEL V"
    lvl5 = Button(*posf(lvl5pos, lvl5size), *lvl5size, color=lvl5color, buttonText=lvl5text,
                  onclickFunction=load_game, onclickParams={"era":1, "level":5, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=select_plane_for_1_era, onePress=True, fontsize=75, bold=True)


def select_plane_for_1_era():
    wait(0.125)
    global menu
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 4, height // 4), "I-16"
    title = Text((width // 2, height // 8), f"Chose plane", fontsize=100, fontcolor=(255, 255, 255))
    plane_1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_era1lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75, bold=True, buttonImg='I-16/0.png')
    lvl1pos, lvl1text = (width // 4 + lvl1size[0] + 100, height // 4), "I-153"
    plane_2 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                     onclickFunction=load_era1lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75,
                     bold=True, buttonImg='I-153/0.png')
    lvl1pos, lvl1text = (width // 4 + lvl1size[0] * 2 + 200, height // 4), "Hurricane"
    plane_3 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                     onclickFunction=load_era1lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75,
                     bold=True, buttonImg='Hurricane/0.png')
    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=load_erachoice, onePress=True, fontsize=75, bold=True)
    # *posf(era2pos, era2size), *era2size, color = era2color, buttonText = era2text,
    # onclickFunction = load_era2lvls, onePress = True, fontsize = 75, bold = True

def select_plane_for_2_era():
    wait(0.125)
    global menu
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 4, height // 4), "Bf 109"
    title = Text((width // 2, height // 8), f"Chose plane", fontsize=100, fontcolor=(255, 255, 255))
    plane_1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_era2lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75, bold=True, buttonImg=f'{lvl1text}/0.png')
    lvl1pos, lvl1text = (width // 4 + lvl1size[0] + 100, height // 4), "Spitfire"
    plane_2 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                     onclickFunction=load_era2lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75,
                     bold=True, buttonImg=f'{lvl1text}/0.png')
    lvl1pos, lvl1text = (width // 4 + lvl1size[0] * 2 + 200, height // 4), "Ki-43"
    plane_3 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                     onclickFunction=load_era2lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75,
                     bold=True, buttonImg=f'{lvl1text}/0.png')
    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=load_erachoice, onePress=True, fontsize=75, bold=True)
    # *posf(era2pos, era2size), *era2size, color = era2color, buttonText = era2text,
    # onclickFunction = load_era2lvls, onePress = True, fontsize = 75, bold = True


def select_plane_for_3_era():
    wait(0.125)
    global menu
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 4, height // 4), "F-86"
    title = Text((width // 2, height // 8), f"Chose plane", fontsize=100, fontcolor=(255, 255, 255))
    plane_1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_era3lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75, bold=True, buttonImg=f'{lvl1text}/0.png')
    lvl1pos, lvl1text = (width // 4 + lvl1size[0] + 100, height // 4), "Me 163"
    plane_2 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                     onclickFunction=load_era3lvls, onclickParams={"chosen_plane": lvl1text}, onePress=True, fontsize=75,
                     bold=True, buttonImg=f'{lvl1text}/0.png')
    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=load_erachoice, onePress=True, fontsize=75, bold=True)
    # *posf(era2pos, era2size), *era2size, color = era2color, buttonText = era2text,
    # onclickFunction = load_era2lvls, onePress = True, fontsize = 75, bold = True



def load_era2lvls(chosen_plane):
    wait(0.125)
    global menu

    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 240), "LEVEL I"
    lvl1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_game, onclickParams={"era":2, "level":1, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl2color, lvl2size, lvl2pos, lvl2text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "LEVEL II"
    lvl2 = Button(*posf(lvl2pos, lvl2size), *lvl2size, color=lvl2color, buttonText=lvl2text,
                  onclickFunction=load_game, onclickParams={"era":2, "level":2, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl3color, lvl3size, lvl3pos, lvl3text = (128, 0, 0), (400, 100), (width // 2, height // 2), "LEVEL III"
    lvl3 = Button(*posf(lvl3pos, lvl3size), *lvl3size, color=lvl3color, buttonText=lvl3text,
                  onclickFunction=load_game, onclickParams={"era":2, "level":3, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl4color, lvl4size, lvl4pos, lvl4text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "LEVEL IV"
    lvl4 = Button(*posf(lvl4pos, lvl4size), *lvl4size, color=lvl4color, buttonText=lvl4text,
                  onclickFunction=load_game, onclickParams={"era":2, "level":4, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl5color, lvl5size, lvl5pos, lvl5text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 240), "LEVEL V"
    lvl5 = Button(*posf(lvl5pos, lvl5size), *lvl5size, color=lvl5color, buttonText=lvl5text,
                  onclickFunction=load_game, onclickParams={"era":2, "level":5, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=select_plane_for_2_era, onePress=True, fontsize=75, bold=True)


def load_era3lvls(chosen_plane):
    wait(0.125)
    global menu
    menu = []
    lvl1color, lvl1size, lvl1pos, lvl1text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 240), "LEVEL I"
    lvl1 = Button(*posf(lvl1pos, lvl1size), *lvl1size, color=lvl1color, buttonText=lvl1text,
                  onclickFunction=load_game, onclickParams={"era":3, "level":1, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl2color, lvl2size, lvl2pos, lvl2text = (128, 0, 0), (400, 100), (width // 2, height // 2 - 120), "LEVEL II"
    lvl2 = Button(*posf(lvl2pos, lvl2size), *lvl2size, color=lvl2color, buttonText=lvl2text,
                  onclickFunction=load_game, onclickParams={"era":3, "level":2, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl3color, lvl3size, lvl3pos, lvl3text = (128, 0, 0), (400, 100), (width // 2, height // 2), "LEVEL III"
    lvl3 = Button(*posf(lvl3pos, lvl3size), *lvl3size, color=lvl3color, buttonText=lvl3text,
                  onclickFunction=load_game, onclickParams={"era":3, "level":3, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl4color, lvl4size, lvl4pos, lvl4text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 120), "LEVEL IV"
    lvl4 = Button(*posf(lvl4pos, lvl4size), *lvl4size, color=lvl4color, buttonText=lvl4text,
                  onclickFunction=load_game, onclickParams={"era":3, "level":4, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    lvl5color, lvl5size, lvl5pos, lvl5text = (128, 0, 0), (400, 100), (width // 2, height // 2 + 240), "LEVEL V"
    lvl5 = Button(*posf(lvl5pos, lvl5size), *lvl5size, color=lvl5color, buttonText=lvl5text,
                  onclickFunction=load_game, onclickParams={"era":3, "level":5, "chosen_plane": chosen_plane}, onePress=True, fontsize=75, bold=True)

    backcolor, backsize, backpos, backtext = (128, 0, 0), (300, 100), (175, height - 75), "BACK"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=select_plane_for_3_era, onePress=True, fontsize=75, bold=True)


def posf(targetpos, size):
    return (targetpos[0] - size[0] // 2, targetpos[1] - size[1] // 2)


def load_menu():
    wait(0.125)
    global menu, in_game, all_sprites, horizontal_borders, vertical_borders, player, targets, planes_sprites, radar, enemies

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    player = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    planes_sprites = pygame.sprite.Group()
    radar = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    in_game = False
    menu = []
    playcolor, playsize, playpos, playtext = (128, 0, 0), (500, 200), (width // 2, height // 2 - 110), "PLAY"
    play = Button(*posf(playpos, playsize), *playsize, color=playcolor, buttonText=playtext,
                  onclickFunction=load_erachoice, onePress=True, fontsize=75, bold=True)
    exitcolor, exitsize, exitpos, exittext = (128, 0, 0), (500, 200), (width // 2, height // 2 + 110), "EXIT"
    exit = Button(*posf(exitpos, exitsize), *exitsize, color=exitcolor, buttonText=exittext,
                  onclickFunction=pygame.quit, onePress=True, fontsize=75, bold=True)


def pause_game():
    # wait(0.125)
    global menu, paused
    paused = True
    print(1)
    plane.sound.stop()
    # paused = False
    menu = []
    backcolor, backsize, backpos, backtext = (128, 0, 0), (500, 200), (width // 2, height // 2 - 110), "CONTINUE"
    back = Button(*posf(backpos, backsize), *backsize, color=backcolor, buttonText=backtext,
                  onclickFunction=continue_game,
                  onePress=True, fontsize=75, bold=True)
    exittomenucolor, exittomenusize, exittomenupos, exittomenutext = (128, 0, 0), (500, 200), (
    width // 2, height // 2 + 110), "MAIN MENU"
    exittomenu = Button(*posf(exittomenupos, exittomenusize), *exittomenusize, color=exittomenucolor,
                        buttonText=exittomenutext,
                        onclickFunction=load_menu,
                        onePress=True, fontsize=75, bold=True)
    # exittomenu.update()
    print(check_enemies())


def continue_game():
    plane.sound.play(loops=-1)
    load_ingameui()


def load_ingameui():
    if not check_enemies():
        global menu, boolparams, in_game, params, plane, paused
        paused = False
        params = {"SPEED": round(plane.speed, 2), "THROTTLE": round(plane.throttle, 2), "ROCKETS": plane.rocketlimit, "BOMBS": plane.bomblimit, "AMMO": plane.bulletlimit, "HEALTH": round(plane.health, 2)}
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
            x, y = width - 200, 0
            prcolor, prfontsize, prh = (255, 255, 255), 40, 100
            for i in params:
                y += prh
                # print(y)
                Text((x, y), f"{i}: {params[i]}", fontsize=prfontsize, fontcolor=prcolor)
    else:
        global results
        results["status"] = "VICTORY!"
        load_results()


def check_enemies():
    global enemies, targets
    return not (enemies.sprites() or targets.sprites())


class Button():
    def __init__(self, x, y, width, height, color, buttonText='Button', onclickFunction=None, onePress=False,
                 onclickParams=0, fontsize=30, bold=False, fontname="Arial", buttonImg=None):
        self.bold = bold
        self.font = pygame.font.SysFont(fontname, fontsize, bold=self.bold)
        self.image = None
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
        if buttonImg:
            self.image = scale(load_image(buttonImg), self.bwidth, 300)
            self.img_rect = self.image.get_rect()
            self.img_rect.x = self.x
            self.img_rect.y = self.y + self.bheight

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))
        menu.append(self)
        self.pos = (x, y)
        self.fontcolor = color
        self.font = pygame.font.SysFont(fontname, fontsize, bold=bold)
        self.surf = self.font.render(buttonText, True, self.fontcolor)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = posf(self.pos, self.surf.get_size())
        # print(self.rect.x, self.rect.y)

    def change_text(self, text):
        self.surf = self.font.render(text, True, self.fontcolor)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = posf(self.pos, self.surf.get_size())
        print(self.rect.x, self.rect.y)

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

        if self.image:
            screen.blit(self.image, self.img_rect)

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


def posf(targetpos, size1):
    return (targetpos[0] - size1[0] // 2, targetpos[1] - size1[1] // 2)


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
    music = pygame.mixer_music.load(fullname)
    return music


def play(name, volume=5, loops=0):
    pygame.mixer_music.load(f"sounds/{name}")
    pygame.mixer_music.set_volume(volume)
    pygame.mixer_music.play(loops)
    global paused
    paused = False


def stop():
    global paused
    paused = True
    pygame.mixer_music.stop()


def pause():
    global paused
    if paused:
        pygame.mixer_music.unpause()
        paused = False
    else:
        pygame.mixer_music.unpause()
        paused = True


class FPS:
    def __init__(self):
        pass

    def draw(self, text):
        text_surface = font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(100, 50))
        screen.blit(text_surface, text_rect)


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
        try:
            angle = degrees(acos(vx / v))
        except ZeroDivisionError:
            angle = plane.vector.angle
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
        self.rect.x, self.rect.y = posf(self.centerpos, self.image.get_size())

        # self.rect.x -= plane.vector.vx
        # self.rect.y += plane.vector.vy


class Map(BasedMapObject):
    mapim = scale(load_image("map2.jpg"), *map_size)

    def __init__(self):
        super().__init__(Map.mapim, Vector(), center)


class Bomb(BasedMapObject):
    # boom = scale(load_image("boom.png"), 100, 100)
    # crater = scale(load_image("crater.webp"), 50, 50)

    def __init__(self, damage=200):
        self.dmg = damage
        self.bombsize = self.dmg // 2
        self.boomsize = self.bombsize * 4
        self.cratersize = self.boomsize // 2
        # self.bombsize = 100
        # self.boomsize = self.bombsize
        # self.cratersize = 50
        self.bomb = scale(rotate(load_image("bomb.png"), 225), self.bombsize, self.bombsize)
        self.boom = scale(load_image("boom.png"), self.boomsize, self.boomsize)
        self.crater = scale(load_image("crater.webp"), self.cratersize, self.cratersize)
        super().__init__(self.bomb, plane.vector * 0.2, center)
        self.snd = pygame.mixer.Sound("sounds/bombsnd.wav")
        self.snd.set_volume(0.1)
        self.snd.play()
        self.explotionsnd = pygame.mixer.Sound("sounds/bomb_explotano.wav")
        self.explotionsnd.set_volume(0.4)
        self.explosion_imgs = []
        for i in range(0, 5):
            self.explosion_imgs.append(
                scale(load_image(f'{i}.png', 'data/plane_explosion_animation', -1), self.boomsize,
                      self.boomsize))
            self.explosion_imgs.append(
                scale(load_image(f'{i}.png', 'data/plane_explosion_animation', -1), self.boomsize,
                      self.boomsize))
        # self.image = rotate(self.image, (plane.vector.angle + 270) % 360)
        self.rect = self.image.get_rect()
        self.rect.move(*self.realv.get_int_xy())
        self.rect.x, self.rect.y = posf(self.pos, self.size)
        self.size = (self.bombsize, self.bombsize)
        self.explosion_sc = 0
        self.flytime = 3
        self.expltime = 2
        self.status = "bomb"

    def update(self, *args):
        super().update()
        # print(self.t)
        # print(self.flytime + self.expltime)
        if self.t < self.flytime:
            self.bombsize = int(self.bombsize * (1 - self.t / (self.flytime * 400)))
            self.size = (self.bombsize, self.bombsize)
            self.image = scale(self.bomb, *self.size)
            self.image = rotate(self.image, self.v.angle - 90)
        elif self.t >= self.flytime and self.status == "bomb":
            self.v = Vector()
            prev_rect = self.rect.center
            self.explotionsnd.play()
            self.image = self.explosion_imgs[self.explosion_sc]
            self.rect = self.image.get_rect()
            self.rect.center = prev_rect
            self.explosion_sc += 1
            self.size = (self.boomsize, self.boomsize)
            if self.explosion_sc == 10:
                self.status = "boom"
        elif self.t >= self.flytime + self.expltime and self.status == "boom":
            self.status = "crater"
            self.image = self.crater
            self.size = (self.cratersize, self.cratersize)
            self.snd.stop()
        if pygame.sprite.spritecollideany(self, targets) and self.status == "boom":
            t = pygame.sprite.spritecollideany(self, targets)
            if pygame.sprite.collide_mask(self, t):
                t.health -= self.dmg


class Rocket(BasedMapObject):
    def __init__(self, vector, pos, target, parent, damage=25):
        image = scale(load_image('missile.png'), 15, 73)
        # self.add(rockets)
        self.parent = parent
        self.sound = pygame.mixer.Sound('sounds/rct_launch.wav')
        self.sound.set_volume(0.2)
        self.sound.play()
        self.expl_sound = pygame.mixer.Sound('sounds/bomb_explotano.wav')
        self.expl_sound.set_volume(0.5)
        self.target = target
        self.damage = damage
        self.explosion_imgs = [load_image(f'{i // 2}.png', 'data/rocket_explosion_animation', -1) for i in range(22)]
        super().__init__(image, vector, pos)
        self.killed = False
        self.animation_sc = 0
        self.orig = image
        self.image = pygame.transform.rotate(image, vector.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x, self.rect.y = posf(pos, self.size)
        self.v = vector
        self.distance = 10000
        self.tv = self.rect.centerx - self.target.rect.centerx, self.rect.centery - self.target.rect.centery

    def update(self, *args):
        self.image = pygame.transform.rotate(self.orig, -self.v.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.v.vx, self.v.vy = self.v.value * cos(
            math.radians(self.v.angle)), self.v.value * sin(math.radians(self.v.angle))
        if self.killed is False:
            super().update()
            if self.get_angle(self.v.angle + 3) < self.get_angle(self.v.angle - 3):
                self.v = Vector(self.v.value, self.v.angle + 3)
            elif self.get_angle(self.v.angle + 3) > self.get_angle(self.v.angle - 3):
                self.v = Vector(self.v.value, self.v.angle - 3)
            self.image = pygame.transform.rotate(self.orig, self.v.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.v.vx, self.v.vy = self.v.value * sin(
                math.radians(self.v.angle)), self.v.value * cos(math.radians(self.v.angle))
            self.distance -= abs(self.v.vy)
            self.distance -= abs(self.v.vx)
            if self.distance <= 0:
                self.kill()


            if pygame.sprite.collide_mask(self, self.target):
                self.killed = True
                self.target.health -= self.damage
        else:
            self.expl_sound.play()
            self.explosion()


    def get_angle(self, angle):
        try:
            self.tv = self.rect.centerx - self.target.rect.centerx, self.rect.centery - self.target.rect.centery

            vx, vy = self.v.value * sin(
                math.radians(angle + 90)), self.v.value * cos(math.radians(angle + 90))
            mod_a = (vx ** 2 + vy ** 2) ** 0.5
            mod_b = (self.tv[0] ** 2 + self.tv[1] ** 2) ** 0.5
            pr = vx * self.tv[0] + vy * self.tv[1]
            res = pr / (mod_a * mod_b)
            if res < 0:
                ans = -math.degrees(math.acos(res))
            else:
                ans = math.degrees(math.acos(res))
            return ans
        except Exception:
            return 0

    def explosion(self):
        self.parent.launched_rockets -= 1
        self.image = self.explosion_imgs[self.animation_sc]
        self.rect = self.image.get_rect()
        self.rect.center = self.target.rect.center
        self.animation_sc += 1

        if self.animation_sc == 22:
            self.kill()


class Bullet(BasedMapObject):
    image = pygame.Surface((1, 5))

    def __init__(self, vector, pos, damage=0.1, spread=4):
        # self.add(bullets)
        super().__init__(Bullet.image, vector, pos)
        self.image.fill('black')
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x, self.rect.y = posf(pos, self.size)
        self.orig = self.image
        self.explosion_imgs = [scale(load_image(f'{i // 2}.png', 'data/rocket_explosion_animation', -1), 20, 20) for i in
                               range(22)]
        self.animation_sc = 0
        self.distance = 3000
        self.killed = False
        self.damage = damage
        self.spread = spread

    def update(self):
        self.image = pygame.transform.rotate(self.orig, -self.v.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.v.vx, self.v.vy = self.v.value * cos(
            math.radians(self.v.angle)), self.v.value * sin(math.radians(self.v.angle))
        self.distance -= abs(self.v.vx)
        self.distance -= abs(self.v.vy)
        if self.distance <= 0:
            self.kill()

        # self.rect.y -= self.v.vx
        # self.rect.x -= self.v.vy
        if self.killed is False:
            super().update()
            self.image = pygame.transform.rotate(self.orig, self.v.angle - 90)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.v.angle += random.choice(range(-self.spread, self.spread))
            self.v.vx, self.v.vy = self.v.value * sin(
                math.radians(self.v.angle)), self.v.value * cos(math.radians(self.v.angle))
            if pygame.sprite.spritecollideany(self, planes_sprites):
                t = pygame.sprite.spritecollideany(self, planes_sprites)
                if pygame.sprite.collide_mask(self, t):
                    self.killed = True
                    t.health -= self.damage
        else:
            self.explosion()

    def explosion(self):
        self.image = self.explosion_imgs[self.animation_sc]
        self.rect = self.image.get_rect(center=self.rect.center)

        self.animation_sc += 1
        # self.rect.x -= plane.vector.vx
        # self.rect.y += plane.vector.vy
        if self.animation_sc == 22:
            self.kill()


class Plane(pygame.sprite.Sprite):
    def __init__(self, name, size, health, max_speed, mobility, max_bullets, rockets, max_rockets,
                 max_bombs, bullet_speed, bullet_damage, rocket_damage, bomb_damage, spread, guns):
        # print(bomb_damage)
        super().__init__(player, planes_sprites, all_sprites)


        if name == 'F-86' or name == 'Me 163':
            self.mgsnd = pygame.mixer.Sound("sounds/a10a-brrt-original-—-сделано-в-Clipchamp.mp3")
        else:
            self.mgsnd = pygame.mixer.Sound("sounds/mgsnd.mp3")
        self.mgsnd.set_volume(0.5)
        self.sound = pygame.mixer.Sound('sounds/planesnd.wav')
        self.sound.set_volume(0.2)
        self.sound.play(loops=-1)
        self.name = name

        self.explosion_imgs = []
        self.image = load_image('0.png', f'data/{name}', -1)
        for i in range(0, 5):
            self.explosion_imgs.append(
                scale(load_image(f'{i}.png', 'data/plane_explosion_animation', -1), self.image.get_width() * size, self.image.get_height() * size))
            self.explosion_imgs.append(
                scale(load_image(f'{i}.png', 'data/plane_explosion_animation', -1), self.image.get_width() * size, self.image.get_height() * size))
        self.mask = pygame.mask.from_surface(self.image)
        self.animations = []
        self.animations_shoot = []
        self.explosion_sc = 0
        for i in range(-3, 4):
            img = load_image(f'{i}.png', f'data/{name}', -1)
            self.animations.append(scale(img, img.get_width() * size, img.get_height() * size))
            if i != 0:
                self.animations.append(scale(img, img.get_width() * size, img.get_height() * size))
        self.explotionsnd = pygame.mixer.Sound("sounds/bomb_explotano.wav")
        self.explotionsnd.set_volume(0.4)
        self.bulletlimit = max_bullets
        self.rocketlimit = max_rockets
        self.bulletspeed = bullet_speed
        self.blltdmg = bullet_damage
        self.rctdmg = rocket_damage
        self.health = self.maxhealth = health
        self.rockets = rockets
        self.launched_rockets = 0
        self.bombing = False
        self.bomblimit = max_bombs
        self.autobombing = False
        self.spamenabled = False
        self.bombenabled = True
        self.bombt = 0
        self.bombdmg = bomb_damage
        self.bombfr = 0.25
        self.crosst = 0.05
        self.spread = spread
        self.guns = guns

        self.t = 0
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.tick = lambda: self.clock.tick(60)
        self.deltat = 0

        self.rect = self.image.get_rect()
        self.rect.centerx = center[0]
        self.rect.centery = center[1]

        self.shiftcoef = 1.25
        self.maxspeed = max_speed
        self.mobility = mobility
        self.throttle = 1
        self.speed = self.maxspeed * self.throttle
        self.vector = Vector(self.speed, 90)

        self.orig = self.image
        self.animation_sc = 6
        self.prev_rocket_t = 0
        self.prev_bullet_t = 0

    def update(self, *args, **kwargs):
        # print(self.health)
        if self.health <= 0:
            global results
            results["status"] = "DEFEAT"
            self.explosion()
        self.deltat = self.tick() / 1000
        self.t += self.deltat

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            if self.throttle + self.deltat / 10 <= 1:
                self.throttle += self.deltat / 10
        elif key[pygame.K_s]:
            if self.throttle - self.deltat / 10 >= 0.5:
                self.throttle -= self.deltat / 10

        if key[pygame.K_a]:
            self.vector.angle += self.mobility
            self.animation_sc -= 1 if self.animation_sc > 0 else 0
            self.image = self.animations[self.animation_sc]
            self.image = pygame.transform.rotate(self.animations[self.animation_sc], self.vector.angle - 90)

        elif key[pygame.K_d]:
            self.vector.angle -= self.mobility
            self.animation_sc += 1 if self.animation_sc < 12 else 0
            self.image = self.animations[self.animation_sc]
            self.image = pygame.transform.rotate(self.animations[self.animation_sc], self.vector.angle - 90)

        else:
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
        self.mask = pygame.mask.from_surface(self.image)

        if key[pygame.K_SPACE] and self.bombenabled and self.bomblimit > 0:
            self.bombing = True
            self.bombt = self.t
            Bomb(int(self.bombdmg))
            if not self.spamenabled:
                self.bombenabled = False
                self.bomblimit -= 1
        if self.t - self.bombt >= self.bombfr and not self.bombenabled:
            self.bombenabled = True
        if self.t - self.bombt >= self.crosst:
            self.bombing = False

        if key[pygame.K_f] and self.rockets:
            if self.rocketlimit and self.launched_rockets < 2 and self.t - self.prev_rocket_t >= 4:
                if enemies.sprites():
                    enemy = self.closest()
                    if self.t - self.prev_rocket_t >= 1:
                        self.rocketlimit -= 1
                        self.launched_rockets += 1
                        Rocket(Vector(25, self.vector.angle), self.rect.center, enemy, self, self.rctdmg)
                        self.prev_rocket_t = self.t
                    else:
                        print('Ракета перезаряжаются')
                else:
                    print("Противников не обнаружено")
        if pygame.sprite.spritecollideany(self, enemies):
            target = pygame.sprite.spritecollideany(self, enemies)
            if pygame.sprite.collide_mask(self, target):
                results["status"] = "CRASHED"
                self.explosion()

    def fire(self):
        if self.bulletlimit > 1 and self.t - self.prev_bullet_t >= 0.1:
            angle_rad = math.radians(-self.vector.angle - 90)
            if self.guns == 1:
                new_x = self.rect.centerx + (math.cos(angle_rad)) - (100 * math.sin(angle_rad))
                new_y = self.rect.centery + (math.sin(angle_rad)) + (100 * math.cos(angle_rad))
                Bullet(Vector(self.bulletspeed, self.vector.angle), (new_x, new_y), self.blltdmg, self.spread)
                self.bulletlimit -= 1
            else:
                new_x = self.rect.centerx + (50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
                new_y = self.rect.centery + (50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(self.bulletspeed, self.vector.angle), (new_x, new_y), self.blltdmg, self.spread)
                new_x = self.rect.centerx + (-50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
                new_y = self.rect.centery + (-50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(self.bulletspeed, self.vector.angle), (new_x, new_y), self.blltdmg, self.spread)
                self.bulletlimit -= 2
            self.prev_bullet_t = self.t

    def closest(self):
        ses = [abs(x.get_vector_from_plane().value) for x in enemies.sprites()]
        # print(ses)
        return min(enemies.sprites(), key=lambda x: abs(x.get_vector_from_plane().value))

    def explosion(self):
        prev_rect = self.rect.center
        self.image = self.explosion_imgs[self.explosion_sc]
        self.rect = self.image.get_rect()
        self.rect.center = prev_rect
        self.explosion_sc += 1
        self.explotionsnd.play()
        self.sound.stop()
        self.mgsnd.stop()
        if self.explosion_sc == 10:
            load_results()
            self.kill()


class TargetCross(pygame.sprite.Sprite):
    image = scale(load_image("targetcross.png"), 100, 100)

    def __init__(self):
        super().__init__(all_sprites)
        self.image1 = TargetCross.image
        self.size2 = (125, 125)
        self.image2 = scale(self.image1, *self.size2)
        self.image = self.image1
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.coef = 16
        self.posvector = plane.vector * self.coef
        self.centerpos = (center[0] + int(self.posvector.vx), center[1] - int(self.posvector.vy))
        self.rect.x, self.rect.y = posf(self.centerpos, self.size)
        # print(self.rect.x, self.rect.y)

    def update(self, *args):
        self.posvector = plane.vector * self.coef
        self.centerpos = (center[0] + int(self.posvector.vx), center[1] - int(self.posvector.vy))
        if plane.bombing:
            self.image = self.image2
            self.rect.x, self.rect.y = posf(self.centerpos, self.size2)
        else:
            self.image = self.image1
            self.rect.x, self.rect.y = posf(self.centerpos, self.size)
        # print(self.rect.x, self.rect.y)


class Enemy(BasedMapObject):
    image = load_image('0.png', 'data/Me 163', -1)

    def __init__(self, angle, pos, name, size, health, max_speed, mobility, max_bullets, rockets, max_rockets,
                 max_bombs, bullet_speed, bullet_damage, rocket_damage, spread, guns, bomb_damage=0):
        super().__init__(Enemy.image, Vector(max_speed, angle), pos)
        self.add(enemies, planes_sprites)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos
        self.animations = []
        for i in range(-3, 4):
            img = load_image(f'{i}.png', f'data/{name}', -1)
            self.animations.append(scale(img, img.get_width() * size, img.get_height() * size))
            if i != 0:
                self.animations.append(scale(img, img.get_width() * size, img.get_height() * size))
        self.explosion_imgs = []
        for i in range(0, 5):
            self.explosion_imgs.append(scale(load_image(f'{i}.png', 'data/plane_explosion_animation', -1), self.size[0], self.size[1]))
            self.explosion_imgs.append(scale(load_image(f'{i}.png', 'data/plane_explosion_animation', -1), self.size[0], self.size[1]))
        self.orig = self.image
        self.image = pygame.transform.rotate(self.orig, self.v.angle - 90)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.explotionsnd = pygame.mixer.Sound("sounds/bomb_explotano.wav")
        self.explotionsnd.set_volume(0.4)
        self.caught = False
        self.target = plane
        self.rockets = rockets
        self.explosion_sc = 0
        self.animation_sc = 6
        self.fire_rate = -1
        self.prev_bullet_t = 0
        self.prev_rocket_t = 0
        self.range = r.range
        self.bulletlimit = max_bullets
        self.rocketlimit = max_rockets
        self.launched_rockets = 0
        self.bulletspeed = bullet_speed
        self.bltdmg = bullet_damage
        self.rctdmg = rocket_damage
        self.health = self.maxhealth = health
        self.dmgtkn = 0
        self.maxspeed = max_speed
        self.mobility = mobility
        self.status = None
        self.spread = spread
        self.guns = guns

    def update(self):
        self.dmgtkn = self.maxhealth - self.health
        try:
            angle, range = self.get_angle(self.v.angle)
            if range <= self.range:
                self.attack()
            else:
                self.fly()
        except ZeroDivisionError:
            pass
        if self.health > 0:
            self.image = pygame.transform.rotate(self.animations[self.animation_sc], self.v.angle - 90)
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(center=self.rect.center)
            super().update()
        else:
            self.explosion()
        # super().update()
        # self.move()

    def fly(self):
        self.v = Vector(self.v.value, self.v.angle + 3)
        self.image = pygame.transform.rotate(self.orig, self.v.angle - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def circle_attack(self, angle):
        more_angle = self.get_angle(self.v.angle + 1)[0]
        less_angle = self.get_angle(self.v.angle - 1)[0]
        if angle > 0:
            # print(self.get_angle(self.v.angle)[1])
            if round(more_angle) <= round(less_angle):
                self.turn_right()
            elif round(more_angle) >= round(less_angle):
                self.turn_left()
        elif angle < 0:
            # print(self.get_angle(self.v.angle)[1])
            if round(more_angle) <= round(less_angle):
                self.turn_left()
            elif round(more_angle) >= round(less_angle):
                self.turn_right()

    def turn_right(self, seconds=1):
        self.v = Vector(self.v.value, self.v.angle - self.mobility)
        self.animation_sc += 1 if self.animation_sc < 12 else 0
        self.image = self.animations[self.animation_sc]

    def turn_left(self, seconds=1):
        self.v = Vector(self.v.value, self.v.angle + self.mobility)
        self.animation_sc -= 1 if self.animation_sc > 0 else 0
        self.image = self.animations[self.animation_sc]

    def dodge(self):
        if self.status == 'right':
            self.turn_left()
        else:
            self.turn_right()

    def attack(self):
        # self.v = Vector(self.v.value, plane.vector.angle)
        # self.image = pygame.transform.rotate(self.orig, self.v.angle - 90)
        angle, range = self.get_angle(self.v.angle)
        if -175 > angle > -195:
            if -150 > angle > -210:
                if range < 700:
                    self.shoot()
            if self.animation_sc < 6:
                self.animation_sc += 1
            elif self.animation_sc > 6:
                self.animation_sc -= 1
            if range > 200:
                if self.rockets and self.launched_rockets < 2 and self.rocketlimit and self.t - self.prev_rocket_t >= 4:
                    self.launched_rockets += 1
                    Rocket(Vector(25, self.v.angle), self.rect.center, plane, self)
                    self.rocketlimit -= 1
                    self.prev_rocket_t = self.t
        else:
            self.circle_attack(angle)

    def get_angle(self, angle):
        ans = math.degrees(0)
        try:
            self.tv = self.rect.centerx - self.target.rect.centerx, self.rect.centery - self.target.rect.centery
            range = (abs(self.tv[0]) ** 2 + abs(self.tv[1]) ** 2) ** 0.5
            vx, vy = self.v.value * sin(
                math.radians(angle + 90)), self.v.value * cos(math.radians(angle + 90))
            mod_a = (vx ** 2 + vy ** 2) ** 0.5
            mod_b = (self.tv[0] ** 2 + self.tv[1] ** 2) ** 0.5
            pr = vx * self.tv[0] + vy * self.tv[1]
            res = pr / (mod_a * mod_b)
            if res < 0:
                ans = (-math.degrees(math.acos(res)), range)
            else:
                ans = (math.degrees(math.acos(res)), range)
        except Exception:
            ans = (math.degrees(0), 0)
        return ans

    def shoot(self):
        if self.bulletlimit > 1 and self.t - self.prev_bullet_t >= 0.1:
            angle_rad = math.radians(-self.v.angle - 90)
            if self.guns == 1:
                new_x = self.rect.centerx + (math.cos(angle_rad)) - (math.sin(angle_rad))
                new_y = self.rect.centery + (50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(self.bulletspeed, self.v.angle), (new_x, new_y), self.bltdmg, self.spread)
                self.bulletlimit -= 1
            else:
                new_x = self.rect.centerx + (50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
                new_y = self.rect.centery + (50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(self.bulletspeed, self.v.angle), (new_x, new_y), self.bltdmg, self.spread)
                new_x = self.rect.centerx + (-50 * math.cos(angle_rad)) - (50 * math.sin(angle_rad))
                new_y = self.rect.centery + (-50 * math.sin(angle_rad)) + (50 * math.cos(angle_rad))
                Bullet(Vector(self.bulletspeed, self.v.angle), (new_x, new_y), self.bltdmg, self.spread)
                self.bulletlimit -= 2
            self.prev_bullet_t = self.t

    def explosion(self):
        prev_rect = self.rect.center
        self.image = self.explosion_imgs[self.explosion_sc]
        self.rect = self.image.get_rect()
        self.rect.center = prev_rect
        self.explosion_sc += 1
        self.explotionsnd.play()

        if self.explosion_sc == 10:
            global results
            results["Planes destroyed"] += 1
            self.kill()

    def get_vector_from_plane(self):
        x, y = self.centerpos[0] - center[0], self.centerpos[1] - center[1]
        s = (x ** 2 + y ** 2) ** 0.5
        if not s:
            return Vector()
        angle = degrees(acos(x / s))
        if y > 0:
            angle = 360 - angle
        return Vector(s, angle)
    #
    # def move(self):
    #     self.v = Vector(self.v.value, self.v.angle)
    #     self.image = pygame.transform.rotate(self.orig, self.v.angle - 90)
    #     self.mask = pygame.mask.from_surface(self.image)
    #     self.rect = self.image.get_rect(center=self.centerpos)


class Target(BasedMapObject):
    image = scale(load_image('Targets/plank.jpeg'), 100, 100)
    images = [scale(load_image('Targets/plank.jpeg'), 100, 100)]

    def __init__(self):
        arr = [i.pos for i in targets.sprites()]
        x, y = random.randint(0, width), random.randint(0, height)
        while (x, y) in arr:
            x, y = random.randint(0, width), random.randint(0, height)
        self.pos = (x, y)
        super().__init__(random.choice(Target.images), Vector(), self.pos)
        self.add(targets)
        self.health = self.maxhealth = 400
        self.dmgtkn = 0

    def update(self):
        self.dmgtkn = self.maxhealth - self.health
        if self.health <= 0:
            global results
            results["Ground targets destroyed"] += 1
            plane.rocketlimit += 5
            plane.bulletlimit += 600
            self.kill()
        super().update()


class Radar(pygame.sprite.Sprite):
    def __init__(self, range=1000, rtspeed=12):
        super().__init__(radar, all_sprites)
        self.image = scale(load_image('radar.png', 'data'), 200, 200)
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.x0 = self.rect.centerx
        self.y0 = self.rect.centery
        self.r = 80
        self.angle = 0
        self.enemy = False
        self.range = range
        self.rtspeed = rtspeed
        self.caught = []

    def update(self, *args, **kwargs):
        self.x = self.x0 + self.r * math.cos(math.radians(self.angle))
        self.y = self.y0 + self.r * math.sin(math.radians(self.angle))
        pygame.draw.line(screen, 'green', (self.x0, self.y0), (self.x, self.y), width=2)
        self.check()
        self.angle = (self.angle + self.rtspeed) % 360
        self.redraw()

    def check(self):
        for enemy in enemies.sprites():
            s = enemy.get_vector_from_plane()
            # print(int(s.angle), self.angle)
            if s.value < self.range and int(s.angle) - int(s.angle) % self.rtspeed == 360 - self.angle and not enemy.caught:
                posx = self.rect.centerx + (s.vx / self.range * self.r)
                posy = self.rect.centery - (s.vy / self.range * self.r)
                enemy.caught = True
                self.caught.append([posx, posy, self.angle, enemy])
                pygame.draw.circle(screen, (0, 255, 0), (posx, posy), 5)

    def redraw(self):
        newarr = []
        for i in range(len(self.caught)):
            if self.angle == self.caught[i][2]:
                self.caught[i][3].caught = False
            else:
                newarr.append(self.caught[i])
                pygame.draw.circle(screen, (0, 255, 0), tuple(self.caught[i][:2]), 5)
        self.caught = newarr


pygame.display.set_caption('A STORM ON A HOT DAY')
screen.fill((255, 255, 255))
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
player = pygame.sprite.Group()
targets = pygame.sprite.Group()
planes_sprites = pygame.sprite.Group()
radar = pygame.sprite.Group()
enemies = pygame.sprite.Group()

fpslabel = FPS()
load_menu()
# play("salam.mp3")
clock = pygame.time.Clock()
t = 0
firing = False
running = True
plane = None

while running:
    # print(in_game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and in_game:
            if paused:
                plane.sound.play()
                load_ingameui()
            else:
                print("pause")

                pause_game()
            # paused = not paused
            # Maybe
            boolparams = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_TAB:
            print("tab changed")
            boolparams = not boolparams
            load_ingameui()
        elif plane in planes_sprites:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT and paused is False:
                print('a')
                firing = True
                plane.mgsnd.play(loops=-1)
            elif event.type == pygame.MOUSEBUTTONUP:
                plane.mgsnd.stop()
                firing = False
    if in_game and paused is False:
        load_ingameui()
    if plane:
        if firing:
            plane.fire()

    screen.fill((0, 0, 0))

    all_sprites.draw(screen)
    player.draw(screen)
    if paused is False:
        all_sprites.update()
        player.update()
    fpslabel.draw(f'FPS: {round(clock.get_fps())}')
    for object in menu:
        object.update()
    pygame.display.flip()
    if not paused:
        t += clock.tick(30) / 1000
pygame.quit()
