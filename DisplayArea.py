from pygame._sdl2 import Window, Renderer, Texture
from Animations import classifier

class DisplayUnit:

    def __init__(self, displayScreen, width, height, x, y, whatToShow, animation):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.whatToShow = whatToShow
        self.displayScreen = displayScreen
        self.animator = classifier.getAnimator(animation)(self)

class DisplayScreen:
    currentTime = None
    timeInMs = None

    def __init__(self, monitor, whatToShow, animation):
        whatToShow = whatToShow.split(":")
        numberOfUnits = len(whatToShow)
        self.orientation = "portrait" if monitor.width < monitor.height else "landscape"
        
        if self.orientation == "landscape":
            widthOfUnit = monitor.width/numberOfUnits
            heightOfUnit = monitor.height
        else:
            widthOfUnit = monitor.width
            heightOfUnit = monitor.height/numberOfUnits
        
        window = Window(size=(monitor.width, monitor.height), position=(monitor.x, monitor.y))
        self.renderer = Renderer(window)
        
        self.units = []
        x = 0
        y = 0
        for timeUnit in whatToShow:
            self.units.append(DisplayUnit(self, widthOfUnit, heightOfUnit, x, y, timeUnit, animation))
            if self.orientation == "landscape":
                x += widthOfUnit
            else:
                y += heightOfUnit

