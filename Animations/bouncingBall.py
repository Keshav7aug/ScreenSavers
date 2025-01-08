import pygame
from pygame._sdl2 import Renderer, Window, Texture
from Animations.lib import Colors


def isColision(h,k,r,x,y):
    if ((x-h)**2)+((y-k)**2) >= r**2:
        return True
    return False

def solveQuad(h,k,r,x,y,ox,oy,vx,vy):
    if x==ox:
        return (ox, r+k, (oy/vy)-(r/vy)) 
    m = (y-oy)/(x-ox)
    C1 = oy-(m*ox)-k
    C = -1*((r**2)-(h**2)-(C1**2))
    A = (1+(m**2))
    B = ((2*m*C1)-2*h)
    D = ((B*B)-(4*A*C))
    print(f"Determinant {A} {B} {C} {D}")
    D=D**0.5
    x1 = (-B+D)/(2*A)
    x2 = (-B-D)/(2*A)
    t1 = (x1-x)/vx
    t2 = (x2-x)/vx
    if t1>t2:
        x1=x2
        t1=t2
    y1 = ox+(m*(x1-ox))
    
    return (x1,y1,t1)
    
def moveIt(h,k,r,oldX,oldY,speed,oldTime,currentTime):
    timeElapsed = currentTime-oldTime
    vx,vy = speed
    x = oldX+(vx*timeElapsed)
    y = oldY+(vy*timeElapsed)
    print("HERE", x,y,timeElapsed)
    if isColision(h,k,r,x,y):
        xc,yc,t1 = solveQuad(h,k,r,x,y,oldX,oldY,vx,vy)
        currentTime-=t1
        vxn = vx - (2*(((vx*(xc-h))+(vy*(yc-k)))/((xc-h)**2+(yc-k)**2))*(xc-h))
        vyn = vy - (2*(((vx*(xc-h))+(vy*(yc-k)))/((xc-h)**2+(yc-k)**2))*(yc-k))
        speed = (vxn,vyn)
        print(speed)
        x,y = xc,yc
        print("Collison")
    print("Data",x,y,r,timeElapsed,speed)
    return {"x":x, "y":y, "speed":speed, "time": currentTime}


def animate(**kargs):
    sw = kargs["screenWidth"]
    sh = kargs["screenHeight"]
    renderer = kargs["renderer"]
    timeInMS = kargs["timeInMS"]
    try:
        oldX = kargs["bouncingball"]["x"]
        oldY = kargs["bouncingball"]["y"]
        speed = kargs["bouncingball"]["speed"]
        oldTime = kargs["bouncingball"]["time"]
    except:
        oldX, oldY, speed, oldTime = sw//2, sh//2, (0, 500), timeInMS
    radius = min(sw//2,sh//2)
    center = (sw//2,sh//2)
    circle_surface = pygame.Surface((sw, sh), pygame.SRCALPHA)
    pygame.draw.circle(
    surface=circle_surface, color=Colors.grey, center=center, radius=radius,width=5)
    vals = moveIt(*center, radius, oldX, oldY, speed, oldTime, timeInMS)
    pygame.draw.circle(
    surface=circle_surface, color=Colors.blue, center=(vals["x"], vals["y"]), radius=20)
    circle_texture = Texture.from_surface(renderer, circle_surface)
    circle_rect = circle_texture.get_rect()
    return {"data": [(circle_texture,circle_rect)], "args": vals}