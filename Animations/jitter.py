from Animations.lib import getNextTime, getFont, Colors
import time
import math

jitter_intensity = 50
def getProgress(val, currentTime, monitorN):
    nextMinute = 60*(math.ceil(currentTime/60))
    secleft = nextMinute - currentTime
    threshHold = 5
    if(secleft<threshHold):
        return val*((threshHold-secleft)/threshHold)
    return 0


def animate(**kargs):
    selectedFont = 'helveticaneuecondensed'
    monitorNum = kargs["monitorNum"]
    currentTime = kargs["currentTime"]
    sw = kargs["screenWidth"]
    sh = kargs["screenHeight"]
    renderer = kargs["renderer"]
    val = kargs["val"]
    timeInMS = kargs["timeInMS"]
    jitterPerc = getProgress(val,timeInMS,monitorNum)
    if jitterPerc!=0:
        selectedFont = "chiller"
    fSH, text_texture = getFont(True,monitorNum,currentTime,sw,sh,selectedFont,renderer)
    jitter_x = jitter_intensity*jitterPerc
    jitter_y = jitter_intensity*jitterPerc
    posx,posy = (sw//2)+jitter_x, (sh//2)+jitter_y
    text_rect = text_texture.get_rect(centerx = posx, centery=posy)

    return [[text_texture,text_rect]]