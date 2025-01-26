import screeninfo
from datetime import datetime
import pygame
from pygame._sdl2 import Renderer, Window, Texture
import time
from Animations import classifier
from DisplayArea import DisplayArea

def getWindows(orientation):
    monitors = screeninfo.get_monitors()
    windows = []
    for i, monitor in enumerate(monitors):
        window = DisplayArea(monitor.width, monitor.height, monitor.x, monitor.y, orientation[i])
        windows.append(window)
    return windows

def isItTimeToExit():
    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    for event in pygame.event.get():
        if event.type in haltEvents:
            return True
    return False

animation = "odometer"
def run_screensaver(orientation):
    pygame.init()
    pygame.mouse.set_visible(False)
    displayAreas = getWindows(orientation)

    clock = pygame.time.Clock()
    running = True
    numberOfMonitors = len(renderers)
    animationArgs = None
    while not isItTimeToExit():
        DisplayArea.currentTime = datetime.now()
        DisplayArea.timeInMs = time.time()
        for displayArea in displayAreas:
            if isItTimeToExit():
                break
            renderer = displayArea.renderer
            renderer.clear()
            animatedBoard = classifier.applyAnimation(theDisplay)
            for text_texture,text_rect in animatedBoard:
                renderer.blit(text_texture, text_rect)
            renderer.present()
        clock.tick(60)
    pygame.quit()

   