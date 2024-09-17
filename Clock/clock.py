import pygame
import sys
import random
import argparse
import datetime
import time
import math

class Colors:
    black = (0,0,0)
    white = (255,255,255)
    grey = (127,127,127)
    red = (200,0,0)
    blue = (0,0,255)
    CARD_COLOR = (30, 30, 30)
    yellow = (255,255,0)

def getCurrentTime():
    now = datetime.datetime.now().strftime("%H:%M")
    return now.split(":")

def getFlipProgress(val):
    currentTime = time.time()
    nextMinute = 60*(math.ceil(currentTime/60))
    secleft = nextMinute - currentTime
    threshHold = 5
    if(secleft<threshHold):
        return val*((threshHold-secleft)/threshHold)
    return 0

def apply_sizzling_effect(surface):
    # Create a new surface with the same dimensions as the text
    sizzling_surface = surface.copy()
    
    # Flicker effect (random alpha change)
    for y in range(0, surface.get_height(), 10):
        for x in range(0, surface.get_width(), 10):
            if random.random() < 0.3:  # 30% chance of flickering at any point
                flicker_alpha = random.randint(alpha_min, alpha_max)
                sizzling_surface.set_at((x, y), sizzling_surface.get_at((x, y)).lerp(Colors.grey, 0.5))
    
    return sizzling_surface

def apply_glow_effect(surface):
    glow_surface = pygame.Surface((surface.get_width() + glow_intensity * 2, surface.get_height() + glow_intensity * 2), pygame.SRCALPHA)
    
    for i in range(glow_intensity):
        glow_color = (255, 255, 0, 10 * (glow_intensity - i))  # Yellowish glow with decreasing alpha
        glow_rect = glow_surface.get_rect(center=surface.get_rect(center=(screen_width // 2, screen_height // 2)).center)
        pygame.draw.rect(glow_surface, glow_color, glow_rect.inflate(i * 2, i * 2), border_radius=10)

    glow_surface.blit(surface, (glow_intensity, glow_intensity))
    return glow_surface


pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))

r1 = 0.4231770833333333
r2 = 0.7523148148148148
fontSize = int(min(screen_width*r1, screen_height*r2))
font = pygame.font.SysFont('helveticaneuecondensed', fontSize)  # Customize the font and size

text1,text2 = getCurrentTime()
text_surface1 = font.render(text1, True, Colors.grey)
text_surface2 = font.render(text2, True, Colors.grey)


text_width1, text_height1 = text_surface1.get_size()
text_width2, text_height2 = text_surface2.get_size()

padding_x = 50
padding_y = 30

card_width = max(text_width1, text_width2) + padding_x * 2
card_height = max(text_height1, text_height2) + padding_y * 2

spacing_between_cards = 50  # Space between the two rectangles
total_width = (2 * card_width) + spacing_between_cards
card_pos1 = [(screen_width - total_width) // 2, (screen_height - card_height) // 2]
card_pos2 = [card_pos1[0] + card_width + spacing_between_cards, card_pos1[1]]

jitter_intensity = 50  # Max number of pixels for jitter (shaking effect)
alpha_min, alpha_max = 150, 255  # Range for alpha (transparency) flickering
glow_intensity = 0  # Glow effect radius # Todo: to be done later

clock = pygame.time.Clock()



def gettextColour():
    textColour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    return textColour


def run_screensaver(t=-1):
    # print(pygame.font.get_fonts())
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    cT=0
    val=1
    jitterPerc = 0
    haltEvents = [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.QUIT]
    textColour = gettextColour()
    while cT!=t:
        for event in pygame.event.get():
            if event.type in haltEvents:
                pygame.quit()
                sys.exit()
        # Todo: To be redisigned later
        if abs(jitterPerc)>0.9:
            screen.fill(Colors.black)
            CARD_COLOR = Colors.CARD_COLOR
        else:
            screen.fill(Colors.black)
            CARD_COLOR = Colors.CARD_COLOR
        text1,text2 = getCurrentTime()
        jitterPerc = getFlipProgress(val)
        if jitterPerc==0:
            font = pygame.font.SysFont('helveticaneuecondensed', fontSize)
        else:
            font = pygame.font.SysFont('chiller', fontSize)
        text_surface1 = font.render(text1, True, Colors.grey)
        text_surface2 = font.render(text2, True, Colors.grey)
        # Todo
        # sizzled_surface1 = apply_sizzling_effect(text_surface1)
        # sizzled_surface2 = apply_sizzling_effect(text_surface2)
        # glowing_surface1 = apply_glow_effect(sizzled_surface1)
        # glowing_surface2 = apply_glow_effect(sizzled_surface2)

        jitter_x = jitter_intensity*jitterPerc
        jitter_y = jitter_intensity*jitterPerc
        # jitter_x = random.randint(-jitter_intensity, jitter_intensity)
        # jitter_y = random.randint(-jitter_intensity, jitter_intensity)

        pygame.draw.rect(screen, CARD_COLOR, (card_pos1[0], card_pos1[1], card_width, card_height), border_radius=20)
        pygame.draw.rect(screen, CARD_COLOR, (card_pos2[0], card_pos2[1], card_width, card_height), border_radius=20)

        screen.blit(text_surface1, (card_pos1[0] + padding_x + jitter_x - glow_intensity, card_pos1[1] + padding_y + jitter_y - glow_intensity))
        screen.blit(text_surface2, (card_pos2[0] + padding_x + jitter_x - glow_intensity, card_pos2[1] + padding_y + jitter_y - glow_intensity))

        pygame.display.flip()

        clock.tick(60)
        cT+=1
        val*=-1


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