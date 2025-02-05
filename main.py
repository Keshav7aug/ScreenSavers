import screeninfo
import MultiWindowClock.clock as MWC
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import pathlib
import argparse
import sys
import os
import json

def getConfigDir():
    debug = True
    if not debug:
        config_dir = pathlib.Path(os.getenv("APPDATA"), "Clock_ScreenSaver")
    else:
        config_dir = pathlib.Path(".")
    return config_dir

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

def convertOrientation(orientation):
    convertor = ["%H:%M:%S", "%H", "%M", "%S", "%H:%M", "%M:%H:%S"]
    return [convertor[int(val)] for val in orientation]

def saveOrientation(orientation):
    with open(config_filepath,"w") as f:
        f.write(json.dumps(orientation, indent=2))

def init():
    numberOfMonitors = len(screeninfo.get_monitors())
    orientation = loadOrientation()
    if len(orientation) != numberOfMonitors:
        orientation = [0]*numberOfMonitors
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
        MWC.run_screensaver(convertOrientation(loadOrientation()))
    elif len(loadOrientation()) == 0 or "/c" in args:
        open_settings_dialog()
    if args == "/p":  # Preview
        MWC.run_screensaver(convertOrientation(loadOrientation()))  # You can make a mini preview here

if __name__ == "__main__":
    config_dir = getConfigDir()
    config_filepath = config_dir.joinpath("config_clock.json")
    handle_arguments()