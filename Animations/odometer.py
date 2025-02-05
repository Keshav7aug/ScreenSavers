import math
from Animations.lib import getFont, Colors, drawDots
from datetime import timedelta

class AnimationArgs:
    def __init__(self, text_rect):
        self.text_rect = text_rect


class Odometer:
    def __init__(self, display):
        self.font = 'helveticaneuecondensed'
        animationThresh = {
            "%H": 0.99,
            "%M": 0.98,
            "%S": 0.90
        }
        self.display = display
        val = display.whatToShow
        self.nextAnimationThresh = animationThresh[val] if val in animationThresh else 1
        self.currentAnimationThresh = self.nextAnimationThresh

    def getFontSize(self):
        r1 = 0.625
        r2 = 1.1111111111111112
        fontSize = int(min(self.display.width * r1, self.display.height * r2))
        theTime = self.whatToShow()
        fontSize = (2*fontSize)//(len(theTime.replace(" ","")) - theTime.count(":"))
        return fontSize

    def canBeAnimated(self):
        theTime = self.whatToShow()
        try:
            val = int(theTime)
            return True
        except:
            return False

    def whatToShow(self):
        val = self.display.whatToShow
        theTime = self.display.displayScreen.currentTime
        try:
            toShow = theTime.strftime(val)
        except:
            return val
        return toShow

    def shouldDisplayNext(self):
        return self.getProgress(1) >= self.nextAnimationThresh

    def shouldStartAnimation(self):
        return self.getProgress(1) >= self.currentAnimationThresh

    def getProgress(self, mul):
        multiplier = 1000
        currentTime = self.display.displayScreen.timeInMs * multiplier
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
        return (self.display.displayScreen.currentTime + timedelta(seconds = theNextDict[whatToShow])).strftime(whatToShow)
        

    def animate(self):

        shouldDisplayNext = False
        if not self.canBeAnimated():
            startPosX, startPosY = self.display.x + (self.display.width // 2), (self.display.height // 2)
            posx, posy = startPosX, startPosY

            textToShow = self.whatToShow()
            _, text_texture = getFont(self.display.displayScreen.renderer, self.getFontSize(), Colors.red, textToShow, self.font)

        else:
            shouldDisplayNext = self.shouldDisplayNext()
            theFont, text_texture = getFont(self.display.displayScreen.renderer, self.getFontSize(), Colors.red, self.whatToShow(), self.font)
            fSH = theFont.get_ascent()
            totalHeight = (self.display.height - (self.display.height // 2))
            startPosX, startPosY = self.display.x + (self.display.width // 2), (self.display.height // 2) 
            if self.shouldStartAnimation():
                jitter_y = self.getProgress(1-self.currentAnimationThresh)*totalHeight
            else:
                jitter_y = 0
            posx, posy = startPosX, startPosY + jitter_y
        
        text_rect = text_texture.get_rect(centerx = posx, centery = posy)
        animatedBoards = [(text_texture,text_rect)]


        if shouldDisplayNext:
            nextTime = self.getNextTime()
            theFont, text_texture_next = getFont(self.display.displayScreen.renderer, self.getFontSize(), Colors.grey, self.getNextTime(), self.font)
            fSHN = theFont.get_ascent()
            startPosNextX, startPosNextY = startPosX, -fSHN
            totalHeight =  startPosY - startPosNextY
            jitterYN = self.getProgress(1-self.nextAnimationThresh) * totalHeight
            posxN, posyN = startPosNextX, startPosNextY + jitterYN
            text_rect_next = text_texture_next.get_rect(centerx = posxN,centery = posyN)
            animatedBoards.append((text_texture_next, text_rect_next))
            
        return animatedBoards
