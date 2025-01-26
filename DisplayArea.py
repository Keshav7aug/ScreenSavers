from pygame._sdl2 import Window, Renderer

class DisplayArea:
    currentTime = None
    timeInMs = None

    def __init__(self, width, height, posx, posy, whatToShow):
        self.width = width
        self.height = height
        self.x = posx
        self.y = posy
        self.whatToShow = whatToShow
        self.window = Window(size=(self.width, self.height), position=(self.x, self.y))
        self.renderer = Renderer(Window)
