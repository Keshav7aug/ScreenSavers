import pygame
import sys
import random
import argparse
pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

class Colors:
    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    blue = (0,0,255)

def getBallColour():
    ballColour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    return ballColour
ball_radius = 20
ball_pos = [random.randint(ball_radius, screen_width-ball_radius),
random.randint(ball_radius, screen_height-ball_radius)]
ball_vel = [random.choice([-5,5]), random.choice([-10,10])]

clock = pygame.time.Clock()

def run_screensaver(t=-1):
    cT=0
    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN]
    ballColour = getBallColour()
    while cT!=t:
        for event in pygame.event.get():
            if event.type in haltEvents:
                pygame.quit()
                sys.exit()
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        if ball_pos[0] <= ball_radius or ball_pos[0] >= screen_width-ball_radius:
            ball_vel[0] = -ball_vel[0]
            ballColour = getBallColour() 
        if ball_pos[1] <= ball_radius or ball_pos[1] >= screen_height-ball_radius:
            ball_vel[1] = -ball_vel[1]
            ballColour = getBallColour()
        screen.fill(Colors.black)
        pygame.draw.circle(screen, ballColour, ball_pos, ball_radius)
        pygame.display.flip()
        clock.tick(60)
        cT+=1


def show_config():
    pass

def handle_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('/s', action='store_true', help="Run the screensaver")
    parser.add_argument('/c', action='store_true', help="Configure the screensaver")
    parser.add_argument('/p', action='store_true', help="Preview the screensaver")

    args = ""
    if len(sys.argv)>1:
        args = sys.argv[1].lower()

    if args == "/s":  # Start screensaver
        run_screensaver()
    elif args == "/c":  # Configuration (if needed)
        show_config()
    elif args == "/p":  # Preview
        run_screensaver(100)  # You can make a mini preview here
    else:
        run_screensaver()

handle_arguments()