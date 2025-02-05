from datetime import timedelta
import pygame
from pygame._sdl2 import Renderer, Window, Texture
class Colors:
    black = (0,0,0,255)
    white = (255,255,255,255)
    grey = (127,127,127,255)
    red = (200,0,0,255)
    blue = (0,0,255,255)
    CARD_COLOR = (30, 30, 30,255)
    yellow = (255,255,0,255)

def drawDots(renderer, center=0, radius=0):
    theCircle = pygame.draw.circle(renderer, Colors.red, center=center, radius=radius)
    return radius, theCircle

def getFont(renderer, fontSize, text_color, text, textFont):
    fontSize = int(fontSize)
    font = pygame.font.SysFont(textFont, fontSize)
    text_surface = font.render(text, True, text_color)
    text_texture = Texture.from_surface(renderer, text_surface)
    return font,text_texture