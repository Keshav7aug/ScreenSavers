import screeninfo
from datetime import datetime
import pygame
from pygame._sdl2 import Renderer, Window, Texture
import time
from Animations import classifier
from DisplayArea import DisplayArea

def getAnimatorObjs(orientation, animation):
    monitors = screeninfo.get_monitors()
    animators = []
    for i, monitor in enumerate(monitors):
        window = DisplayArea(monitor.width, monitor.height, monitor.x, monitor.y, orientation[i])
        animator = classifier.getAnimator("odometer", window)
        animators.append(animator)
    return animators

def isItTimeToExit():
    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    for event in pygame.event.get():
        if event.type in haltEvents:
            return True
    return False

def run_screensaver(orientation, animation = "odometer"):
    pygame.init()
    pygame.mouse.set_visible(False)
    animatorObjs = getAnimatorObjs(orientation, animation)

    clock = pygame.time.Clock()
    running = True
    numberOfMonitors = len(animatorObjs)
    animationArgs = None
    while not isItTimeToExit():
        DisplayArea.currentTime = datetime.now()
        DisplayArea.timeInMs = time.time()
        for animator in animatorObjs:
            if isItTimeToExit():
                break
            renderer = animator.display.renderer
            renderer.clear()
            animatedBoard = animator.animate()
            for text_texture,text_rect in animatedBoard:
                renderer.blit(text_texture, text_rect)
            renderer.present()
        clock.tick(60)
    pygame.quit()
   