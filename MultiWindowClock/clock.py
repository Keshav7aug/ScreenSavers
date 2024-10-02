import random
import screeninfo
from datetime import datetime, timedelta
import pygame
from pygame._sdl2 import Renderer, Window, Texture
import time
import math
from Animations import classifier

jitter_intensity = 50
odo_intensity = 1000
class Colors:
    black = (0,0,0,255)
    white = (255,255,255,255)
    grey = (127,127,127,255)
    red = (200,0,0,255)
    blue = (0,0,255,255)
    CARD_COLOR = (30, 30, 30,255)
    yellow = (255,255,0,255)

def getCurrentTime(numberOfMonitors):
    now = datetime.now().strftime("%H:%M:%S")
    theTime = now
    now = now.split(":")
    now.append(theTime)
    # if numberOfMonitors == 1:
    #     now = [f"{now[0]} : {now[1]}"]
    return now

def getProgress(val,fSH,monitorN):
    currentTime = time.time()
    if animation == "jitter":
        nextMinute = 60*(math.ceil(currentTime/60))
        secleft = nextMinute - currentTime
        threshHold = 5
        if(secleft<threshHold):
            return val*((threshHold-secleft)/threshHold)
        return 0
    return 0   

def getWindows():
    monitors = screeninfo.get_monitors()
    windows = []
    monitors.sort(key=lambda x:x.x)
    print(monitors)
    for monitor in monitors:
        window = Window(size=(monitor.width, monitor.height), position=(monitor.x, monitor.y))
        windows.append((Renderer(window), window))
    return windows

def getAnimationArgs(val,fSH, monitorN):
    jitterPerc = getProgress(val,fSH,monitorN)
    jitter_x=0
    if animation == "jitter":
        # selectedFont = 'helveticaneuecondensed' if jitterPerc == 0 else 'chiller'
        jitter_x = jitter_intensity*jitterPerc
        jitter_y = jitter_intensity*jitterPerc
    else:
        # selectedFont = 'helveticaneuecondensed'
        jitter_y = jitterPerc
    return jitter_x, jitter_y

animation = "odometer"
def run_screensaver():
    global orientation
    pygame.init()
    background_color = (0, 0, 0)
    renderers = getWindows()

    clock = pygame.time.Clock()
    running = True

    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    val = 1
    numberOfMonitors = len(renderers)
    fSH = 0
    while running:
        for event in pygame.event.get():
            if event.type in haltEvents:
                running = False
        currentTime = getCurrentTime(numberOfMonitors)
        
        # for i,dispInfo in enumerate(renderers):
        orientation = orientation[:numberOfMonitors]
        timeInMS = time.time()
        currentDateTime = datetime.now()
        for j, i in enumerate(orientation):
            renderer, window = renderers[j]
            sw, sh = window.size
            renderer.clear()
            animator = classifier.classifyAnimation(animation)
            animatedBoard = animator.animate(monitorNum=i, currentTime=currentTime, screenWidth=sw, screenHeight=sh, renderer=renderer, timeInMS=timeInMS,currentDateTime=currentDateTime)
            if animation == "jitter":
                pos1,pos2 = (sw//2)+jitter_x, (sh//2)+jitter_y
            else:
                pos1,pos2 = (sw//2), (sh//2)
            for text_texture,text_rect in animatedBoard:
                renderer.blit(text_texture, text_rect)
            renderer.present()
        clock.tick(60)
        val *= -1
    pygame.quit()
orientation = [0,1,2,3]
run_screensaver()
                