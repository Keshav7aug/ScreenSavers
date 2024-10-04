import random
import screeninfo
from datetime import datetime, timedelta
import pygame
from pygame._sdl2 import Renderer, Window, Texture
import time
import math
from Animations import classifier
import argparse
import sys
debug = False
orientation = [1]
def getCurrentTime(numberOfMonitors):
    now = datetime.now().strftime("%H:%M:%S")
    theTime = now
    now = now.split(":")
    now.append(theTime)
    if numberOfMonitors == 1:
        now = [f"{now[0]} : {now[1]} : {now[2]}"]
    return now

def getWindows():
    monitors = screeninfo.get_monitors()
    windows = []
    monitors.sort(key=lambda x:x.x)
    print(monitors)
    for monitor in monitors:
        window = Window(size=(monitor.width, monitor.height), position=(monitor.x, monitor.y))
        windows.append((Renderer(window), window))
    return windows

animation = "jitter"
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
            animatedBoard = animator.animate(monitorNum=i, currentTime=currentTime, screenWidth=sw, screenHeight=sh, renderer=renderer, timeInMS=timeInMS,currentDateTime=currentDateTime, val=val)
            for text_texture,text_rect in animatedBoard:
                renderer.blit(text_texture, text_rect)
            renderer.present()
        clock.tick(60)
        val *= -1
    pygame.quit()

def show_config():
    pass

def handle_arguments():
    global orientation
    if not debug:
        orientation = list(range(4))
    parser = argparse.ArgumentParser()
    parser.add_argument('/s', action='store_true', help="Run the screensaver")
    parser.add_argument('/c', action='store_true', help="Configure the screensaver")
    parser.add_argument('/p', action='store_true', help="Preview the screensaver")

    args = ""
    if len(sys.argv)>1:
        args = sys.argv[1].lower()
    if args == "/s":  # Start screensaver
        run_screensaver()
    elif args == "/c":  # Configuration (if needed)
        show_config()
    elif args == "/p":  # Preview
        run_screensaver()  # You can make a mini preview here
    else:
        run_screensaver()

handle_arguments()
                