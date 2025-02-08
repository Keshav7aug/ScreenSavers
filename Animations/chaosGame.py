import random
import pygame
from Animations.lib import Colors
from pygame._sdl2 import Texture

class chaosGame:

    def __init__(self, display):
        self.display = display
        self.colors = [(237, 87, 12, 255), (66, 33, 22, 255), (17, 66, 214, 255), (142, 17, 214, 255), (158, 16, 111, 255), (20, 199, 44, 255), (252, 186, 3, 255), (13, 214, 204, 255)]
        self.surface = pygame.Surface((self.display.width, self.display.height))
        self.initialise()


    def triangle(self):
        self.numberOfPoints = 3
        self.factor = 0.5
        self.corners = [
            ((self.display.width)/2, 0),
            ((0, self.display.height)),
            (self.display.width, self.display.height)
        ]

    def rectangle(self):
        diceRoll = random.randint(0,1)
        points = [
            (0, 0),
            (self.display.width, 0),
            (self.display.width, self.display.height),
            (0, self.display.height)
        ]
        if diceRoll == 0:
            self.numberOfPoints = 5
            self.factor = 2/3
            points.append(((points[0][0]+points[1][0])/2, (points[0][1]+points[3][1])/2))
        elif diceRoll == 1:
            self.numberOfPoints = 8
            self.factor = 2/3
            newPoints = []
            for i in range(4):
                nIdx = (i+1)%4
                npx = (points[i][0]+points[nIdx][0])/2
                npy = (points[i][1]+points[nIdx][1])/2
                newPoints.append((npx, npy))
            points += newPoints
        self.corners = points

    def initialise(self):
        diceRoll = random.randint(3,4)
        if diceRoll == 3:
            self.triangle()
        elif diceRoll == 4:
            self.rectangle()
        
        self.tracePointsData = [((random.randint(1, self.display.width), random.randint(1, self.display.height)), Colors.black)]

    def drawPoint(self, point, color):
        self.display.renderer.draw_color = color
        self.display.renderer.draw_point(point)
        # posx = int(point[0])
        # posy = int(point[1])
        # self.surface.set_at((posx, posy), color)
        # theTexture = Texture.from_surface(self.display.renderer, self.surface)
        # theRect = theTexture.get_rect(centerx = posx, centery = posy)
        # return (theTexture, theRect)

    def getThePoint(self, p1, p2):
        ratio = (self.factor)/(1-self.factor)
        x1, y1 = p1
        x2, y2 = p2
        nx1 = (x1+(ratio*x2))/(1+ratio)
        nx2 = (y1+(ratio*y2))/(1+ratio)
        return (nx1, nx2)

    def animate(self):
        thresh = 10**7
        if len(self.tracePointsData)>thresh:
            self.tracePointsData = self.tracePointsData[-(thresh):]
        for i, corner in enumerate(self.corners):
            self.drawPoint(corner, self.colors[i])
        
        cornerSelection = random.randint(0, self.numberOfPoints-1)
        newTracePoint = self.getThePoint(self.tracePointsData[-1][0], self.corners[cornerSelection])
        color = self.colors[cornerSelection]
        self.tracePointsData.append((newTracePoint, color))
        
        for point in self.tracePointsData:
            self.drawPoint(point[0], point[1])
        return []
