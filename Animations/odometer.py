from Animations.lib import getNextTime, getFont, Colors
import time
import math

def getProgress(fSH,monitorN,currentTime):
    multiplier = 1000
    if monitorN>2:
        return 0
    currentTime*=multiplier
    divisiors = [3600,60,1]
    divisor = divisiors[monitorN]*multiplier
    prevTimeUnit = divisor*(math.floor(currentTime/divisor))
    timeElapsed =  currentTime - prevTimeUnit
    progress = (round(timeElapsed)/divisor)
    return progress*fSH

def animate(**kargs):
    selectedFont = 'helveticaneuecondensed'
    monitorNum = kargs["monitorNum"]
    currentTime = kargs["currentTime"]
    sw = kargs["screenWidth"]
    sh = kargs["screenHeight"]
    renderer = kargs["renderer"]
    currentDateTime = kargs["currentDateTime"]
    timeInMS = kargs["timeInMS"]
    nextTime = getNextTime(monitorNum, currentDateTime)
    renderer.draw_color = Colors.black
    fSH, text_texture = getFont(True,monitorNum,currentTime,sw,sh,selectedFont,renderer)
    totalHeight = (sh-(fSH//2))
    _,text_texture_next = getFont(False,monitorNum,nextTime,sw,sh,selectedFont,renderer)
    jitter_y = getProgress(totalHeight,monitorNum,timeInMS)
    posx,posy1 = (sw//2), (fSH//2)+jitter_y
    posy2 = posy1-totalHeight
    print(posy1, posy2)
    text_rect = text_texture.get_rect(centerx = posx, centery=posy1)
    text_rect_next = text_texture_next.get_rect(centerx=posx,centery=posy2)
    return [[text_texture,text_rect],[text_texture_next,text_rect_next]]


def applyArgs(**kargs):
    pass