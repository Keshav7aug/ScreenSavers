import random
import pygame
from Animations.lib import Colors
from pygame._sdl2 import Texture

class chaosGame:

    def __init__(self, display):
        self.display = display
        self.colors = [(237, 87, 12, 255), (255,255,255,255), (17, 66, 214, 255), (142, 17, 214, 255), (158, 16, 111, 255), (20, 199, 44, 255), (252, 186, 3, 255), (13, 214, 204, 255)]
        self.colors = [
            (0, 255, 255),    # Bright Cyan
            (44, 117, 255),   # Electric Blue
            (50, 205, 50),    # Lime Green
            (255, 0, 255),    # Magenta
            (255, 105, 180),  # Hot Pink
            (255, 255, 0),    # Neon Yellow
            (255, 165, 0),    # Orange
            (220, 20, 60),    # Crimson Red
            (181, 126, 220),  # Lavender
            (64, 224, 208)    # Turquoise
        ]
        self.surface = pygame.Surface((self.display.width, self.display.height))
        self.texture = Texture(self.display.renderer, (self.display.width, self.display.height), target=True)
        self.chosenOnethresh = 2
        self.lastSelectedVertex = [-1]*self.chosenOnethresh
        self.initialisePolygon()


    def triangle(self):
        self.numberOfPoints = 3
        self.corners = [
            ((self.display.width)/2, 0),
            ((0, self.display.height)),
            (self.display.width, self.display.height)
        ]

    def rectangle(self):
        diceRoll = random.randint(0,5)
        points = [
            (0, 0),
            (self.display.width, 0),
            (self.display.width, self.display.height),
            (0, self.display.height)
        ]
        self.numberOfPoints = 4
        if diceRoll == 0:
            self.getAvailableVertex = self.dontChooseCurrent
        elif diceRoll == 1:
            self.getAvailableVertex = self.choseOnePlaceAwayAnti
        elif diceRoll == 2:
            self.getAvailableVertex = self.choseOnePlaceAway
        elif diceRoll == 3:
            self.getAvailableVertex = self.last2AndWhatNot
        if diceRoll == 4:
            self.numberOfPoints = 5
            self.factor = 2/3
            points.append(((points[0][0]+points[1][0])/2, (points[0][1]+points[3][1])/2))
        elif diceRoll == 5:
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

    def pentagon(self):
        diceRoll = random.randint(0,1)
        self.numberOfPoints = 5
        points = [
            ((self.display.width)/2, 0),
            (self.display.width, self.display.height/2),
            (self.display.width, self.display.height),
            (0, self.display.height),
            (0, self.display.height/2)
        ]
        if diceRoll == 0:
            self.getAvailableVertex = self.dontChooseCurrent
        elif diceRoll == 1:
            self.getAvailableVertex = self.last2AndWhatNot
        self.corners = points

    def initialisePolygon(self):
        self.getAvailableVertex = self.defaultSelection
        self.factor = 0.5
        diceRoll = random.randint(3,4)
        if diceRoll == 3:
            self.triangle()
        elif diceRoll == 4:
            self.rectangle()
        elif diceRoll == 5:
            self.pentagon()
        
        for i, corner in enumerate(self.corners):
            self.drawPoint(corner, self.colors[i])

        firstPoint = (random.randint(1, self.display.width), random.randint(1, self.display.height))

        self.drawPoint(firstPoint, Colors.black)

        self.lastPoint = firstPoint

    def drawPoint(self, point, color):
        self.display.renderer.target = self.texture
        if len(color) == 3:
            color = color + (255,)
        self.display.renderer.draw_color = color
        self.display.renderer.draw_point(point)
        self.display.renderer.target = None

    def getThePoint(self, p1, p2):
        ratio = (self.factor)/(1-self.factor)
        x1, y1 = p1
        x2, y2 = p2
        nx1 = (x1+(ratio*x2))/(1+ratio)
        nx2 = (y1+(ratio*y2))/(1+ratio)
        return (nx1, nx2)

    def defaultSelection(self):
        availableVertex = list(range(self.numberOfPoints))
        return availableVertex

    def dontChooseCurrent(self):
        availableVertex = [vertex for vertex in range(self.numberOfPoints) if vertex != self.lastSelectedVertex[-1]]
        return availableVertex

    def choseOnePlaceAwayAnti(self):
        availableVertex = [vertex for vertex in range(self.numberOfPoints) if vertex != (self.lastSelectedVertex[-1]-1+self.numberOfPoints) % self.numberOfPoints]
        return availableVertex

    def choseOnePlaceAway(self):
        availableVertex = [self.lastSelectedVertex[-1]+1, self.lastSelectedVertex[-1]-1]
        availableVertex = [(vertex+self.numberOfPoints) % self.numberOfPoints for vertex in availableVertex]
        return availableVertex

    def last2AndWhatNot(self):
        if self.lastSelectedVertex[-1] == self.lastSelectedVertex[-2]:
            availableVertex = [vertex for vertex in range(self.numberOfPoints) if vertex != (self.lastSelectedVertex[-1]-1+self.numberOfPoints) % self.numberOfPoints and vertex != (self.lastSelectedVertex[-1]+1) % self.numberOfPoints]
        else:
            availableVertex = list(range(self.numberOfPoints))
        return availableVertex

    def animate(self):
        availableVertex = self.getAvailableVertex()
        selectedVertext = random.choice(availableVertex)
        self.lastSelectedVertex.append(selectedVertext)
        self.lastSelectedVertex = self.lastSelectedVertex[-self.chosenOnethresh:]
        newTracePoint = self.getThePoint(self.lastPoint, self.corners[selectedVertext])
        color = self.colors[selectedVertext % (len(self.colors))]
        self.drawPoint(newTracePoint, color)
        self.lastPoint = newTracePoint
        return []
