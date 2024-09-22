import random
import screeninfo
from datetime import datetime, timedelta
import pygame
from pygame._sdl2 import Renderer, Window, Texture
import time
import math

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
    elif animation == "odometer":
        if monitorN>2:
            return 0
        currentTime*=1000
        divisiors = [3600,60,1]
        divisor = divisiors[monitorN]*1000
        prevTimeUnit = divisor*(math.floor(currentTime/divisor))
        timeElapsed =  currentTime - prevTimeUnit
        return (timeElapsed/divisor)*(fSH)
    return 0   

def getNextTime(monitorN):
    currentTime = datetime.now()
    if monitorN == 0:
        val = (currentTime+timedelta(hours=1)).hour
    elif monitorN == 1:
        val = (currentTime+timedelta(minutes=1)).minute
    elif monitorN == 2:
        val = (currentTime+timedelta(seconds=1)).second
    if val<10:
        return f"0{val}"
    return f"{val}"

def getWindows():
    monitors = screeninfo.get_monitors()
    windows = []
    for monitor in monitors:
        window = Window(size=(monitor.width, monitor.height), position=(monitor.x, monitor.y))
        windows.append((Renderer(window), window))
    return windows

def getFont(nextVal,i,timeText,sw,sh,selectedFont,renderer):
    r1 = 0.625
    r2 = 1.1111111111111112
    fontSize = int(min(sw*r1, sh*r2))
    if nextVal == True:
        text = f"{timeText}"
        text_color = Colors.grey
    else:
        text = timeText[i]
        text_color = Colors.red
    fontSize = (2*fontSize)//(len(text.replace(" ","")) - text.count(":"))
    print(nextVal,fontSize,text)
    font = pygame.font.SysFont(selectedFont, fontSize)
    text_surface = font.render(text, True, text_color)
    # sdl2_surface = pygame._sdl2.surface.Surface.from_surface(text_surface)
    text_texture = Texture.from_surface(renderer, text_surface)
    return font.size(text)[1],text_texture

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

animation = "no"
def run_screensaver():
    pygame.init()
    background_color = (0, 0, 0)
    renderers = getWindows()

    clock = pygame.time.Clock()
    running = True

    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    val = 1
    numberOfMonitors = len(renderers)
    fSH = 0
    selectedFont = 'helveticaneuecondensed'
    while running:
        for event in pygame.event.get():
            if event.type in haltEvents:
                running = False
        currentTime = getCurrentTime(numberOfMonitors)
        
        # for i,dispInfo in enumerate(renderers):
        for j,i in enumerate(Orientation):
            renderer, window = renderers[j]
            sw, sh = window.size
            renderer.clear()
            renderer.draw_color = Colors.black
            if animation == "odometer":
                nextTime = getNextTime(i)
            fSH, text_texture = getFont(False,i,currentTime,sw,sh,selectedFont,renderer)
            if animation == "odometer":
                _,text_texture_next = getFont(True,i,nextTime,sw,sh,selectedFont,renderer)
            totalHeight = (sh+(fSH/2))/2
            jitter_x, jitter_y = getAnimationArgs(val,totalHeight,i)
            if animation == "jitter":
                pos1,pos2 = (sw//2)+jitter_x, (sh//2)+jitter_y
            elif animation == "odometer":
                # jitter_y=0
                pos1,pos2 = (sw//2), (sh//2)+jitter_y
                # print(pos1,pos2,jitter_y,jitterPerc)
            else:
                pos1,pos2 = (sw//2), (sh//2)
            text_rect = text_texture.get_rect(centerx = pos1, centery=pos2)
            if animation == "odometer":
                text_rect_next = text_texture_next.get_rect(centerx=pos1,centery=pos2-((sh+fSH)/2))
            renderer.blit(text_texture, text_rect)
            if animation == "odometer":
                renderer.blit(text_texture_next, text_rect_next)
            renderer.present()
        clock.tick(60)
        val *= -1
    pygame.quit()

Orientation = [3]
run_screensaver()
                