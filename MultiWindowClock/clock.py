import random
import screeninfo
import datetime
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
    now = datetime.datetime.now().strftime("%H:%M:%S:%x")
    now = now.split(":")
    if numberOfMonitors == 1:
        now = [f"{now[0]}  {now[1]}"]
    return now

def getProgress(val):
    currentTime = time.time()
    if animation == "jitter":
        nextMinute = 60*(math.ceil(currentTime/60))
        secleft = nextMinute - currentTime
        threshHold = 5
        if(secleft<threshHold):
            return val*((threshHold-secleft)/threshHold)
        return 0
    elif animation == "odometer":
        prevMinute = 60*(math.floor(currentTime/60))
        minElapsed =  currentTime - prevMinute
        threshHold = 60
        return (minElapsed/threshHold)

def getWindows():
    monitors = screeninfo.get_monitors()
    windows = []
    for monitor in monitors:
        window = Window(size=(monitor.width, monitor.height), position=(monitor.x, monitor.y))
        windows.append((Renderer(window), window))
    return windows

def getFont(i,timeText,sw,sh,selectedFont,renderer):
    r1 = 0.625
    r2 = 1.1111111111111112
    fontSize = int(min(sw*r1, sh*r2))
    font = pygame.freetype.SysFont(selectedFont, fontSize)
    text = timeText[i]
    text_color = Colors.grey
    text_surface, _ = font.render(text, text_color)
    # sdl2_surface = pygame._sdl2.surface.Surface.from_surface(text_surface)
    text_texture = Texture.from_surface(renderer, text_surface)
    return text_texture

animation = "jitter"
def run_screensaver():
    pygame.init()
    background_color = (0, 0, 0)
    renderers = getWindows()

    clock = pygame.time.Clock()
    running = True

    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    val = 1
    numberOfMonitors = len(renderers)
    while running:
        for event in pygame.event.get():
            if event.type in haltEvents:
                running = False
        currentTime = getCurrentTime(numberOfMonitors)
        jitterPerc = getProgress(val)
        if animation == "jitter":
            selectedFont = 'helveticaneuecondensed' if jitterPerc == 0 else 'chiller'
            jitter_x = jitter_intensity*jitterPerc
            jitter_y = jitter_intensity*jitterPerc
        else:
            selectedFont = 'helveticaneuecondensed'
            jitter_y = odo_intensity*jitterPerc
        for i,dispInfo in enumerate(renderers):
            renderer, window = dispInfo
            sw, sh = window.size
            renderer.clear()
            renderer.draw_color = Colors.black
            text_texture = getFont(i,currentTime,sw,sh,selectedFont,renderer)
            if animation == "jitter":
                pos1,pos2 = (sw//2)+jitter_x, (sh//2)+jitter_y
            elif animation == "odometer":
                pos1,pos2 = (sw//2), (sh//2)+jitter_y
                # print(pos1,pos2,jitter_y,jitterPerc)
            text_rect = text_texture.get_rect(center = (pos1,pos2))
            renderer.blit(text_texture, text_rect)
            renderer.present()
        clock.tick(60)
        val *= -1
    pygame.quit()
run_screensaver()
                