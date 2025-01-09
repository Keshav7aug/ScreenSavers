from Animations.lib import getNextTime, getFont, Colors
import time
import math

def getProgress(monitorN,currentTime, mul=1):
    multiplier = 1000
    currentTime*=multiplier
    divisiors = [3600,60,1]
    divisor = divisiors[monitorN]*multiplier
    prevTimeUnit = divisor*(math.floor(currentTime/divisor))
    timeElapsed =  currentTime - prevTimeUnit - (divisor*(1-mul))
    progress = (round(timeElapsed)/(divisor*mul))
    return progress

def animate(**kargs):
    selectedFont = 'helveticaneuecondensed'
    monitorNum = kargs["monitorNum"]
    currentTime = kargs["currentTime"]
    sw = kargs["screenWidth"]
    sh = kargs["screenHeight"]
    renderer = kargs["renderer"]
    currentDateTime = kargs["currentDateTime"]
    timeInMS = kargs["timeInMS"]
    numberOfMonitors = kargs["numberOfMonitors"]
    whatToShow = kargs["whatToShow"]
    shouldDisplayNext = whatToShow>0 and whatToShow<4
    if shouldDisplayNext:
        nextTime = getNextTime(whatToShow-1, currentDateTime)
    renderer.draw_color = Colors.black
    fSH, text_texture = getFont(True,monitorNum,currentTime,sw,sh,selectedFont,renderer,whatToShow,shouldDisplayNext)
    totalHeight = (sh-(fSH//2))
    if shouldDisplayNext:
        _,text_texture_next = getFont(False,monitorNum,nextTime,sw,sh,selectedFont,renderer)
    if shouldDisplayNext:
        progress = getProgress(whatToShow-1,timeInMS)
        jitter_y = progress*totalHeight
        thresh = 0.75
        shouldDisplayNext = progress>thresh
        jitter_y1 = 0
        if shouldDisplayNext:
            jitter_y1 = getProgress(whatToShow-1, timeInMS, 1-thresh)*totalHeight
    else:
        jitter_y = (sh//2)-(fSH//2)
    posx,posy1 = (sw//2), (fSH//2)+jitter_y
    posy2 = posy1-totalHeight
    text_rect = text_texture.get_rect(centerx = posx, centery = posy1)
    if shouldDisplayNext:
        text_rect_next = text_texture_next.get_rect(centerx=posx,centery=posy2)
        return {"data": [(text_texture,text_rect),(text_texture_next,text_rect_next)], "args": {}}
    return {"data": [(text_texture,text_rect)], "args": {}}


def applyArgs(**kargs):
    pass