from Animations.TimeAnimation import TimeAnimation
from pygame._sdl2 import Texture
import pygame
import random
import time

from Animations.lib import Colors


class ParticleEffect(TimeAnimation):

    def __init__(self, display):
        super().__init__(display)
        self.font = 'helveticaneuecondensed'
        self.startPos = 0
        self.initialized = False

    def whatToShow(self):
        if self._whatToShow == None:
            return super().whatToShow()
        return self._whatToShow
    
    def timeToInitialise(self):
        self._whatToShow = None
        fontSize = self.getFontSize()
        font = pygame.font.SysFont(self.font, fontSize)
        self.text_surface = font.render(self.whatToShow(), True, Colors.white)
        posx, posy = self.display.x + (self.display.width // 2), (self.display.height // 2) 
        self.text_rect = self.text_surface.get_rect(center=(posx, posy))
        self.display.displayScreen.renderer.clear()
        self.texture = Texture(self.display.displayScreen.renderer, (self.display.displayScreen.width, self.display.displayScreen.height), target=True)

    def drawPoint(self, point, color):
        self.display.displayScreen.renderer.target = self.texture
        if len(color) == 3:
            color = color + (255,)
        self.display.displayScreen.renderer.draw_color = color
        self.display.displayScreen.renderer.draw_point(point)
        self.display.displayScreen.renderer.target = None
        # pass
        # self.display.displayScreen.renderer.draw_color = color
        # self.display.displayScreen.renderer.draw_point(point)

    def drawLine(self, p1, p2, color):

        self.display.displayScreen.renderer.draw_color = color
        self.display.displayScreen.renderer.draw_line(p1, p2)

    def animate(self):
        if not self.initialized:
            self.timeToInitialise()
            self.initialized = True
        startTime = time.time()
        for y in range(self.startPos, self.text_rect.height):
            for x in range(self.text_rect.width):
                if self.text_surface.get_at((x, y)) == Colors.white:
                    px = self.text_rect.x + x + random.choice([1,-1])
                    py = self.text_rect.y + y + random.choice([1,-1])
                    px += random.choice((-1,1))*random.uniform(0.5, 2.0)
                    py += random.choice((-1,1))*random.uniform(0.5, 2.0)
                    self.drawPoint((px, py), Colors.white)
            self.startPos = y+1
            if y == self.text_rect.height - 1:
                # print("initialized", y)
                self.timeToInitialise()
            return []
        # self.timeToInitialise()
        return []

