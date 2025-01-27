import math
from Animations.lib import getFont, Colors

class AnimationArgs:
    def __init__(self):
        pass


class Odometer:
    def __init__(self, theDisplay):
        self.font = 'helveticaneuecondensed'
        self.display = theDisplay
        self.nextAnimationThresh = 0
        self.currentAnimationThresh = 0

    def getFontSize(self):
        r1 = 0.625
        r2 = 1.1111111111111112
        fontSize = int(min(self.display.width * r1, self.display.height * r2))//2
        theTime = self.whatToShow()
        fontSize = (2*fontSize)//(len(theTime.replace(" ","")) - theTime.count(":"))
        return fontSize

    def canBeAnimated(self):
        theTime = self.whatToShow()
        try:
            val = int(val)
            return True
        except:
            return False

    def whatToShow(self):
        val = self.display.whatToShow
        theTime = self.display.currentTime
        toShow = theTime.strftime(val)
        return toShow

    def shouldDisplayNext(self):
        theTime = self.whatToShow()
        try:
            val = int(val)
            return self.getProgress(1) >= self.nextAnimationThresh
        except:
            return False

    def shouldStartAnimation(self):
        theTime = self.whatToShow()
        try:
            val = int(val)
            return self.getProgress(1) >= self.currentAnimationThresh
        except:
            return False

    def getProgress(self, mul):
        multiplier = 1000
        currentTime = self.display.timeInMs * multiplier
        divisiors = {
            "%H": 3600,
            "%M": 60,
            "%S": 1
        }
        divisor = divisiors[self.display.whatToShow] * multiplier
        prevTimeUnit = divisor * (math.floor(currentTime / divisor))
        timeElapsed =  currentTime - prevTimeUnit - (divisor * (1 - mul))
        progress = (round(timeElapsed) / (divisor * mul))
        return progress

    def getNextTime(self):
        whatToShow = self.display.whatToShow
        theNextDict = {
            "%H": 3600,
            "%M": 60,
            "%S": 1
        }
        return (self.display.currentTime + timedelta(seconds = theNextDict[whatToShow])).strftime(whatToShow)
        

    def animate(self):
        shouldDisplayNext = self.shouldDisplayNext()
        self.display.renderer.draw_color = Colors.black

        
        if not self.canBeAnimated():
            fSH, text_texture = getFont(self.display.renderer, self.getFontSize()*2, Colors.red, self.whatToShow(), self.font)
            startPosX, startPosY = self.display.width // 2, (self.display.height // 2)
            posx, posy = startPosX, startPosY
            text_rect = text_texture.get_rect(centerx = posx, centery = posy)
            animatedBoards = [(text_texture,text_rect)]

        else:
            fSH, text_texture = getFont(self.display.renderer, self.getFontSize(), Colors.red, self.whatToShow(), self.font)
            totalHeight = (self.display.height - (fSH // 2))
            startPosX, startPosY = self.display.width // 2, (fSH // 2) 
            if self.shouldStartAnimation():
                jitter_y = self.getProgress(1-self.currentAnimationThresh)*totalHeight
            else:
                jitter_y = 0
            posx, posy = startPosX, startPosY + jitter_y
            text_rect = text_texture.get_rect(centerx = posx, centery = posy)
            animatedBoards = [(text_texture,text_rect)]


            if shouldDisplayNext:
                nextTime = self.getNextTime()
                fSHN, text_texture_next = getFont(self.display.renderer, self.getFontSize(), Colors.grey, self.getNextTime(), self.font)
                startPosNextX, startPosNextY = startPosX, -fSHN
                totalHeight =  startPosY - startPosNextY
                jitterYN = getProgress(1-self.nextAnimationThresh) * totalHeight
                posxN, posyN = startPosNextX, startPosNextY + jitterYN
                text_rect_next = text_texture_next.get_rect(centerx=posx,centery=posy2)
                animatedBoards.append(text_rect_next)
            
        return animatedBoards
