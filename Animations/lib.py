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
def getNextTime(monitorN, currentTime):
    if monitorN == 0:
        val = (currentTime+timedelta(hours=1)).hour
    elif monitorN == 1:
        val = (currentTime+timedelta(minutes=1)).minute
    elif monitorN == 2:
        val = (currentTime+timedelta(seconds=1)).second
    if val<10:
        return f"0{val}"
    return f"{val}"

def getFont(isCurrentTime,i,timeText,sw,sh,selectedFont,renderer):
    r1 = 0.625
    r2 = 1.1111111111111112
    fontSize = int(min(sw*r1, sh*r2))//2
    if isCurrentTime == False:
        text = f"{timeText}"
        text_color = Colors.grey
    else:
        text = timeText[i]
        text_color = Colors.red
    fontSize = (2*fontSize)//(len(text.replace(" ","")) - text.count(":"))
    font = pygame.font.SysFont(selectedFont, fontSize)
    text_surface = font.render(text, True, text_color)
    # sdl2_surface = pygame._sdl2.surface.Surface.from_surface(text_surface)
    text_texture = Texture.from_surface(renderer, text_surface)
    return font.size(text)[1],text_texture