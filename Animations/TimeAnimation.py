import math
from datetime import timedelta
class TimeAnimation:

    def __init__(self, display):
        self.display = display

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
            int(theTime)
            return True
        except:
            return False
    
    def whatToShow(self):
        val = self.display.whatToShow
        theTime = self.display.displayScreen.currentTime
        try:
            toShow = theTime.strftime(val)
        except:
            print(val)
            return None
        return toShow

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
