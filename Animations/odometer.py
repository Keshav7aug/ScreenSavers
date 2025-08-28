from Animations.lib import getFont, Colors, drawDots
from Animations.TimeAnimation import TimeAnimation

class AnimationArgs:
    def __init__(self, text_rect):
        self.text_rect = text_rect

class Odometer(TimeAnimation):
    def __init__(self, display):
        super().__init__(display)
        self.font = 'helveticaneuecondensed'
        self.currentTimeColor = Colors.blue_red
        animationThresh = {
            "%H": 0.99,
            "%M": 0.98,
            "%S": 0.90
        }
        val = display.whatToShow
        self.nextAnimationThresh = animationThresh[val] if val in animationThresh else 1
        self.currentAnimationThresh = self.nextAnimationThresh        

    def shouldDisplayNext(self):
        return self.getProgress(1) >= self.nextAnimationThresh

    def shouldStartAnimation(self):
        return self.getProgress(1) >= self.currentAnimationThresh
    
    def animate(self):
        shouldDisplayNext = False
        if not self.canBeAnimated():
            startPosX, startPosY = self.display.x + (self.display.width // 2), (self.display.height // 2)
            posx, posy = startPosX, startPosY

            textToShow = self.whatToShow()
            _, text_texture = getFont(self.display.displayScreen.renderer, self.getFontSize(), self.currentTimeColor, textToShow, self.font)

        else:
            shouldDisplayNext = self.shouldDisplayNext()
            theFont, text_texture = getFont(self.display.displayScreen.renderer, self.getFontSize(), self.currentTimeColor, self.whatToShow(), self.font)
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
