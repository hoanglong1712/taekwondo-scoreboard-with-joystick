import pygame
from pygame.locals import *
import time

pygame.init()

# initialise the joystick module
pygame.joystick.init()

info = pygame.display.Info()
# define screen size
SCREEN_WIDTH = info.current_w - 10
SCREEN_HEIGHT = info.current_h - 50

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Joysticks")

# define font
font_size = int(SCREEN_WIDTH / 2)
font = pygame.font.SysFont("Futura", font_size)

print(SCREEN_WIDTH, SCREEN_HEIGHT)

# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# create clock for setting game frame rate
clock = pygame.time.Clock()
FPS = 10

# create empty list to store joysticks
joysticks = []
joystick_instance_ids = []

# create player rectangle
x = 350
y = 200
player = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
red_bg = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
blue_bg = pygame.Rect(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH/ 2, SCREEN_HEIGHT)

# define player colour
col = "royalblue"

# game loop
run = True

# scores of red and blue
#red = {1: [], 2: [], 3: [], 4: []}
#blue = {1: [], 2: [], 3: [], 4: []}
red_signal_arr = []
blue_signal_arr = []

red_score = 0
blue_score = 0

while run:

    clock.tick(FPS)

    # update background
    screen.fill(pygame.Color("white"))

    # draw player
    #player.topleft = (x, y)
    #pygame.draw.rect(screen, pygame.Color(col), player)

    # draw background of each score
    pygame.draw.rect(screen, pygame.Color("red"), red_bg)
    pygame.draw.rect(screen, pygame.Color("blue"), blue_bg)

    # draw current scores
    red_image = font.render(f'{red_score}', True, (255, 255, 255))
    size = font.size(f'{red_score}')
    screen.blit(red_image,
                (SCREEN_WIDTH / 4 - size[0] / 2, SCREEN_HEIGHT / 2 - size[1] / 2))

    blue_image = font.render(f'{blue_score}', True, (255, 255, 255))
    size = font.size(f'{blue_score}')
    screen.blit(blue_image,
                (3 * SCREEN_WIDTH / 4 - size[0] / 2, SCREEN_HEIGHT / 2 - size[1]/2))




    # show number of connected joysticks
    #draw_text("Controllers: " + str(pygame.joystick.get_count()), font, pygame.Color("azure"), 10, 10)

    joystick_num = pygame.joystick.get_count()
    if joystick_num > 0:
        pass

    '''
    for joystick in joysticks:
        draw_text("Battery Level: " + str(joystick.get_power_level()), font, pygame.Color("azure"), 10, 35)
        draw_text("Controller Type: " + str(joystick.get_name()), font, pygame.Color("azure"), 10, 60)
        draw_text("Number of axes: " + str(joystick.get_numaxes()), font, pygame.Color("azure"), 10, 85)
    '''
    i = 0
    for joystick in joysticks:
        # change player colour with buttons
        if joystick.get_button(0):
            #col = "royalblue"
            red_signal_arr[i][1] = red_signal_arr[i][1] + 1
            pass
        if joystick.get_button(1):
            #col = "crimson"
            red_signal_arr[i][2] = red_signal_arr[i][2] + 1
            pass
        if joystick.get_button(2):
            #col = "fuchsia"
            red_signal_arr[i][3] = red_signal_arr[i][3] + 1
            pass
        if joystick.get_button(3):
            #col = "forestgreen"
            red_signal_arr[i][4] = red_signal_arr[i][4] + 1
            pass

        # player movement with joystick
        '''
        if joystick.get_button(14):
          x += 5
        if joystick.get_button(13):
          x -= 5
        if joystick.get_button(11):
          y -= 5
        if joystick.get_button(12):
          y += 5
        '''
        # player movement with analogue sticks
        horiz_move = joystick.get_axis(0)
        vert_move = joystick.get_axis(1)
        '''
        if abs(vert_move) > 0.05:
            y += vert_move * 5            
            pass
        if abs(horiz_move) > 0.05:
            x += horiz_move * 5
        '''
        if horiz_move < -0.05:
            blue_signal_arr[i][4] = blue_signal_arr[i][4] + 1
            pass
        if horiz_move > 0.05:
            blue_signal_arr[i][2] = blue_signal_arr[i][2] + 1
            pass
        if vert_move > 0.05:
            blue_signal_arr[i][3] = blue_signal_arr[i][3] + 1
            pass
        if vert_move < -0.05:
            blue_signal_arr[i][1] = blue_signal_arr[i][1] + 1
            pass
        i += 1
        pass

    joystick_changed = False
    # event handler
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
            joystick_instance_ids.append(joy.get_instance_id())
            joystick_changed = True
            pass
        if event.type == pygame.JOYDEVICEREMOVED:
            joystick_changed = True
            for i, instance_id in enumerate(joystick_instance_ids):
                if event.instance_id == instance_id:
                    del joysticks[i]
                    del joystick_instance_ids[i]
                    print(f'Joystick {i} removed')
                    break
                pass
            pass
        # quit program
        if event.type == pygame.QUIT:
            run = False

    if joystick_changed is True:
        red_signal_arr = []
        blue_signal_arr = []
        for joystick in joysticks:
            red_signal_arr.append({1: 0, 2: 0, 3: 0, 4: 0})
            blue_signal_arr.append({1: 0, 2: 0, 3: 0, 4: 0})
            pass
        print("updated ")
        pass
    #print(red_signal_arr, blue_signal_arr)


    # update display
    pygame.display.flip()
    pass

pygame.quit()
