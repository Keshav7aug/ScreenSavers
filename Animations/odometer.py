from Animations.lib import getNextTime, getFont, Colors
import time
import math

class AnimationArgs:

    def __init__(self):
        pass


class Odometer:


    def __init__(self, theDisplay, font):
        self.font = 'helveticaneuecondensed'
        self.display = theDisplay

    def whatToShow(self):
        val = self.display.whatToShow
        theTime = self.display.currentTime
        toShow = theTime.strftime(val)
        return toShow

    def getProgress(self, mul):
        multiplier = 1000
        currentTime*=multiplier
        divisiors = [3600,60,1]
        divisor = divisiors[monitorN]*multiplier
        prevTimeUnit = divisor*(math.floor(currentTime/divisor))
        timeElapsed =  currentTime - prevTimeUnit - (divisor*(1-mul))
        progress = (round(timeElapsed)/(divisor*mul))
        return progress

    def getNextTime(self):
        whatToShow = self.display.whatToShow
        theNextDict = {
            "%H": 3600,
            "%M": 60,
            "%S": 1
        }
        return (self.display.currentTime + timedelta(seconds = theNextDict[whatToShow])).strftime(whatToShow)
        

    def shouldDisplayNext(self):
        theTime = self.whatToShow()
        try:
            val = int(val)
            return True
        except:
            return False

    def animate(self, theDisplay):
        shouldDisplayNext = self.shouldDisplayNext()
        if shouldDisplayNext:
            nextTime = self.getNextTime()
        self.theDisplay.renderer.draw_color = Colors.black
        fSH, text_texture = getFont(True,monitorNum,currentTime,sw,sh,selectedFont,renderer,whatToShow,shouldDisplayNext)
        totalHeight = (sh-(fSH//2))
        if shouldDisplayNext:
            _,text_texture_next = getFont(False,monitorNum,nextTime,sw,sh,selectedFont,renderer)
        if shouldDisplayNext:
            thresh = 0.9
            progress = getProgress(whatToShow-1,timeInMS)
            if progress>thresh:
                progress = getProgress(whatToShow-1,timeInMS,1-thresh)
                jitter_y = progress*totalHeight
                # shouldDisplayNext = progress>thresh
                jitter_y1 = 0
                if shouldDisplayNext:
                    jitter_y1 = getProgress(whatToShow-1, timeInMS, 1-thresh)*totalHeight
            else:
                jitter_y = 0
                jitter_y1 = 0

        else:
            jitter_y = (sh//2)-(fSH//2)
        posx,posy1 = (sw//2), (fSH//2)+jitter_y
        posy2 = posy1-totalHeight
        text_rect = text_texture.get_rect(centerx = posx, centery = posy1)
        if shouldDisplayNext:
            text_rect_next = text_texture_next.get_rect(centerx=posx,centery=posy2)
            return [(text_texture,text_rect),(text_texture_next,text_rect_next)]
        return [(text_texture,text_rect)]
