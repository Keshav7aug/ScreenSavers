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
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import json
import os
import pathlib
debug = False
config_dir = pathlib.Path(os.getenv("APPDATA"), "Clock_ScreenSaver")
config_filepath = config_dir.joinpath("config_clock.json")

def resetConfig():
    if os.path.exists(config_filepath):
        os.remove(config_filepath)
def loadOrientation():
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    if os.path.exists(config_filepath):
        with open(config_filepath) as f:
            orientation = json.loads(f.read())
        return orientation
    return []
    
def saveOrientation(orientation):
    with open(config_filepath,"w") as f:
        f.write(json.dumps(orientation, indent=2))

def init():
    numberOfMonitors = len(screeninfo.get_monitors())
    orientation = loadOrientation()
    if len(orientation) != numberOfMonitors:
        orientation = list(range(numberOfMonitors))
    saveOrientation(orientation)
    
def onSelect(i, combo):
    orientation = loadOrientation()
    mapper = {
        "Time": 0,
        "H": 1,
        "M": 2,
        "S": 3,
        "H:M": 4
    }
    orientation[i] = mapper[combo[i].get()]
    saveOrientation(orientation)

def open_settings_dialog():
    root = tk.Tk()
    options = ["Time","H","M","S","H:M"]
    numberOfMonitors = len(screeninfo.get_monitors())
    orientation = loadOrientation()
    if numberOfMonitors != len(orientation):
        orientation = [0]*numberOfMonitors
    saveOrientation(orientation)
    combos = []
    for i in range(numberOfMonitors): 
        combo = ttk.Combobox(root, values=options)
        combo.current(orientation[i])
        combo.bind("<<ComboboxSelected>>", lambda _,idx=i : onSelect(idx, combos))
        combos.append(combo)
        combo.pack(pady=10)
    root.mainloop()

def getCurrentTime(numberOfMonitors):
    now = datetime.now().strftime("%H:%M:%S")
    theTime = now
    now = now.split(":")
    return now

def getWindows():
    monitors = screeninfo.get_monitors()
    windows = []
    monitors.sort(key=lambda x:x.x)
    for monitor in monitors:
        window = Window(size=(monitor.width, monitor.height), position=(monitor.x, monitor.y))
        windows.append((Renderer(window), window))
    return windows

def isItTimeToExit():
    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    for event in pygame.event.get():
        if event.type in haltEvents:
            return True
    return False

animation = "odometer"
def run_screensaver():
    orientation = loadOrientation()
    pygame.init()
    pygame.mouse.set_visible(False)
    background_color = (0, 0, 0)
    renderers = getWindows()

    clock = pygame.time.Clock()
    running = True

    val = 1
    numberOfMonitors = len(renderers)
    fSH = 0
    animationArgs = {}
    while not isItTimeToExit():
        currentTime = getCurrentTime(numberOfMonitors)
        
        # for i,dispInfo in enumerate(renderers):
        orientation = orientation[:numberOfMonitors]
        timeInMS = time.time()
        currentDateTime = datetime.now()
        for i, whatToShow in enumerate(orientation):
            if isItTimeToExit():
                break
            renderer, window = renderers[i]
            sw, sh = window.size
            renderer.clear()
            animatedBoard = classifier.applyAnimation(animations=animation, monitorNum=i, currentTime=currentTime, screenWidth=sw, screenHeight=sh, renderer=renderer, timeInMS=timeInMS,currentDateTime=currentDateTime, val=val, numberOfMonitors=numberOfMonitors,whatToShow=whatToShow, **animationArgs)
            for text_texture,text_rect in animatedBoard["data"]:
                renderer.blit(text_texture, text_rect)
            animationArgs = animatedBoard["args"]
            renderer.present()
        clock.tick(60)
        val *= -1
    pygame.quit()

def show_config():
    pass

def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('/s', action='store_true', help="Run the screensaver")
    parser.add_argument('/c', action='store_true', help="Configure the screensaver")
    parser.add_argument('/p', action='store_true', help="Preview the screensaver")

    args = ""
    if len(sys.argv)>1:
        args = sys.argv[1].lower()
    if args == "/s":  # Start screensaver
        init()
        run_screensaver()
    elif len(loadOrientation()) == 0 or "/c" in args:
        open_settings_dialog()
    if args == "/p":  # Preview
        run_screensaver()  # You can make a mini preview here

if __name__ == "__main__":
    handle_arguments()
                