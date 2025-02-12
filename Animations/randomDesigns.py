import random
import pygame
from Animations.lib import Colors
class randomDesigns:
    def __init__(self, display):
        self.display = display
        self.oldArgs = []

    def getRandomColor(self):
        color = []
        for i in range(4):
            color.append(random.randint(0,254))
        return color

    def drawLine(self, pos):
        color = self.oldArgs[pos][-1]
        sx = self.oldArgs[pos][0]
        sy = self.oldArgs[pos][1]
        ex = self.oldArgs[pos+1][0]
        ey = self.oldArgs[pos+1][1]
        self.display.renderer.draw_color = color
        self.display.renderer.draw_line((sx, sy), (ex, ey))

    
    def drawCircle(self, cx, cy, radius, color):
        self.display.renderer.draw_color = color
        for x in range(cx - radius, cx + radius):
            for y in range(cy - radius, cy + radius):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    self.display.renderer.draw_point((x, y))

    def animate(self):
        center = (self.display.width//2, self.display.height//2)
        cx = random.randint(0, self.display.width)
        cy = random.randint(0, self.display.height)
        radius = random.randint(0,50)
        color = self.getRandomColor()

        self.oldArgs.append((cx, cy, color))
        if len(self.oldArgs)>500:
            self.oldArgs = self.oldArgs[-500:]
        for i in range(len(self.oldArgs)-1):
            self.drawLine(i)
        # self.drawCircle(cx, cy, radius, color)

        
        return []