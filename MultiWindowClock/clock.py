import screeninfo
from datetime import datetime
import pygame
import time
from DisplayArea import DisplayScreen
from Animations.lib import Colors

def getDisplayObjs(orientation, animation):
    monitors = screeninfo.get_monitors()
    displays = []
    for i, monitor in enumerate(monitors):
        displayScreen = DisplayScreen(monitor, orientation[i], "odometer")
        displays.append(displayScreen)
            
    return displays

def isItTimeToExit():
    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    for event in pygame.event.get():
        if event.type in haltEvents:
            return True
    return False

def run_screensaver(orientation, animation = "odometer"):
    pygame.init()
    pygame.mouse.set_visible(False)
    displays = getDisplayObjs(orientation, animation)

    clock = pygame.time.Clock()
    while not isItTimeToExit():
        DisplayScreen.currentTime = datetime.now()
        DisplayScreen.timeInMs = time.time()

        for display in displays:
            renderer = display.renderer
            renderer.draw_color = Colors.black
            renderer.clear()
            for unit in display.units:
                animatedBoards = unit.animator.animate()
                for text_texture,text_rect in animatedBoards:
                    renderer.blit(text_texture, text_rect)
            renderer.present()
        clock.tick(60)
    pygame.quit()
   