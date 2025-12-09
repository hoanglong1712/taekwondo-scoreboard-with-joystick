import pygame
import time
from tkinter import *
from tkinter import messagebox
import numpy as np  # <<< ADDED: Required for generating sound data

# indices of predefined  buttons
NOTHING = 0
RED_DEC = 1
RED_INC = 2
BLE_DEC = 3
BLE_INC = 4
NEXT_ROUND = 5
RESET = 6
STOP = 7
START_PAUSE = 8
RED_PEN = 9
BLE_PEN = 10

# index in tuple in array of scores of rounds
BLUE_INDEX = 1
RED_INDEX = 0

# Match duration in seconds (dynamic, set by splash screen)
MATCH_DURATION_CHOICE = 60  # Default duration


# Function to generate horn sound
def generate_horn_sound(duration=4.5, frequency1=400, frequency2=550, volume=0.5):
    """
    Generates a simple two-tone horn sound using numpy and converts it to a
    pygame.mixer.Sound object.
    """

    # Configuration
    sample_rate = pygame.mixer.get_init()[0]
    n_samples = int(sample_rate * duration)

    # Generate time array
    time_array = np.linspace(0, duration, n_samples, False)

    # Generate two sine waves for a richer sound
    note1 = np.sin(frequency1 * 2 * np.pi * time_array)
    note2 = np.sin(frequency2 * 2 * np.pi * time_array)

    # Combine, apply volume, and convert to 16-bit integer format
    # The max value for a 16-bit sound is 32767
    combined_wave = (note1 * 0.7 + note2 * 0.5) / 1.2
    amplitude = int(32767 * volume)
    audio_data = (combined_wave * amplitude).astype(np.int16)

    # Create a 2-channel (stereo) array by duplicating the mono channel
    stereo_data = np.column_stack([audio_data, audio_data])

    # Convert NumPy array to Pygame Sound object
    sound = pygame.sndarray.make_sound(stereo_data)

    return sound


def draw_score(screen, font, text, color, centerX, centerY):
    '''
    draw score of red and blue
    :param screen: the screen
    :param font: font of the score
    :param text:
    :param color:
    :param centerX:
    :param centerY:
    :return:
    '''
    image = font.render(text, True, color)
    size = font.size(text)
    # draw from the top left corner of the text
    screen.blit(image, (centerX - size[0] / 2, centerY - size[1] / 2))
    pass


def draw_timer(screen, font, text, color, centerX, centerY):
    '''
    draw the countdown timer
    :param screen: the screen
    :param font: font of the timer
    :param text:
    :param color:
    :param centerX:
    :param centerY:
    :return:
    '''
    image = font.render(text, True, color)
    size = font.size(text)
    screen.blit(image, (centerX - size[0] / 2, centerY - size[1] / 2))
    pass


def update_background(screen, red_bg, blue_bg):
    '''
    clean the whole backgound with white color
    fill the whole screen with red
    fill half of screen with blue
    :param screen:
    :param red_bg:
    :param blue_bg:
    :return:
    '''
    # update background
    screen.fill(pygame.Color("white"))

    # draw player
    # player.topleft = (x, y)
    # pygame.draw.rect(screen, pygame.Color(col), player)

    # draw background of each score
    pygame.draw.rect(screen, pygame.Color("red"), red_bg)
    pygame.draw.rect(screen, pygame.Color("blue"), blue_bg)
    pass


def get_hat_position(joystick, hat_number):
    """
    Gets the current position of a joystick hat.

    Args:
        joystick (pygame.joystick.Joystick): The joystick object.
        hat_number (int): The index of the hat.

    Returns:
        tuple: A tuple containing the x and y coordinates of the hat position.
               (0, 0): Centered
               (1, 0): Right
               (-1, 0): Left
               (0, 1): Up
               (0, -1): Down
               (1, 1): Up-Right
               (-1, 1): Up-Left
               (1, -1): Down-Right
               (-1, -1): Down-Left
    """
    try:
        hat_position = joystick.get_hat(hat_number)
        return hat_position
    except (pygame.error, IndexError):
        return (0, 0)  # Return (0, 0) if hat is not found or an error occurs


def update_signal_arr(joysticks, red_signal_arr, blue_signal_arr):
    '''
    try to fill array of signals of red and blue

    each array contain a list of joystick signal
    normal match has 3 referees, the array has 3 joysticks
    each joystick signal is a dictionary
    {1: 0, 2: 0, 3: 0, 4: 0}
    key is score, value is nmber of signal per score

    :param joysticks:
    :param red_signal_arr:
    :param blue_signal_arr:
    :return:
    '''
    i = 0
    for joystick in joysticks:

        # red player uses right control
        # change player colour with buttons
        name = joystick.get_name().lower()
        # print(name)
        if "xbox" in name:
            # xbox case for red player
            zero = 3
            one = 1
            two = 0
            three = 2
            pass
        elif 'twin' in name:
            # twin usb joystick for red player
            zero = 4
            one = 1
            two = 0
            three = 3
            pass
        else:
            zero = 0
            one = 1
            two = 2
            three = 3
            pass
        if joystick.get_button(zero):
            # col = "royalblue"
            red_signal_arr[i][1] = red_signal_arr[i][1] + 1
            pass
        if joystick.get_button(one):
            # col = "crimson"
            red_signal_arr[i][2] = red_signal_arr[i][2] + 1
            pass
        if joystick.get_button(two):
            # col = "fuchsia"
            red_signal_arr[i][3] = red_signal_arr[i][3] + 1
            pass
        if joystick.get_button(three):
            # col = "forestgreen"
            red_signal_arr[i][4] = red_signal_arr[i][4] + 1
            pass
        '''
        if joystick.get_button(0):
            # col = "royalblue"
            red_signal_arr[i][1] = red_signal_arr[i][1] + 1
            pass
        if joystick.get_button(1):
            # col = "crimson"
            red_signal_arr[i][2] = red_signal_arr[i][2] + 1
            pass
        if joystick.get_button(2):
            # col = "fuchsia"
            red_signal_arr[i][3] = red_signal_arr[i][3] + 1
            pass
        if joystick.get_button(3):
            # col = "forestgreen"
            red_signal_arr[i][4] = red_signal_arr[i][4] + 1
            pass
        '''
        # blue player
        if 'xbox' in name or 'twin' in name:
            # xbox case for blue player
            # twin usb joystick for blue player
            hat_number = 0  # Assuming you want to get the position of the first hat
            x, y = get_hat_position(joystick, hat_number)
            '''
               (0, 0): Centered
               (1, 0): Right
               (-1, 0): Left
               (0, 1): Up
               (0, -1): Down
               (1, 1): Up-Right
               (-1, 1): Up-Left
               (1, -1): Down-Right
               (-1, -1): Down-Left
            '''
            if (x, y) == (-1, 0):
                blue_signal_arr[i][4] = blue_signal_arr[i][4] + 1
                pass
            if (x, y) == (1, 0):
                blue_signal_arr[i][2] = blue_signal_arr[i][2] + 1
                pass
            if (x, y) == (0, -1):
                blue_signal_arr[i][3] = blue_signal_arr[i][3] + 1
                pass
            if (x, y) == (0, 1):
                blue_signal_arr[i][1] = blue_signal_arr[i][1] + 1
                pass
            pass
        else:
            # player movement with analogue sticks
            # blue player uses left control
            horiz_move = joystick.get_axis(0)
            vert_move = joystick.get_axis(1)
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
            pass

        # each joystick goes along with a dictionary in blue or red array
        i += 1
        pass
    pass


def reset_signal_arr(joysticks):
    """
    reset all array after each -- 2 seconds --- and idled time which is 10 seconds for HUBT team
    :param joysticks:
    :return:
    """
    red_signal_arr = []
    blue_signal_arr = []
    for joystick in joysticks:
        # each joystick need 2 dictionary one for red and one for blue
        red_signal_arr.append({1: 0, 2: 0, 3: 0, 4: 0})
        blue_signal_arr.append({1: 0, 2: 0, 3: 0, 4: 0})
        pass
    return red_signal_arr, blue_signal_arr


def update_joysticks(joysticks, joystick_instance_ids,
                     red_signal_arr, blue_signal_arr, run, button_array):
    """
    take action when there is a click on the screen or a press on the joystick
    :param joysticks:
    :param joystick_instance_ids:
    :param red_signal_arr:
    :param blue_signal_arr:
    :param run:
    :param button_array:
    :return:
    """
    joystick_changed = False

    # onscreen buttons
    red_extra = 0
    blue_extra = 0
    red_pen = 0
    blue_pen = 0

    control_button = NOTHING
    # event handler
    for event in pygame.event.get():
        # a new device is added
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            # store the new joystick
            joysticks.append(joy)
            # store its id
            joystick_instance_ids.append(joy.get_instance_id())
            joystick_changed = True
            pass
        # a device is removed
        elif event.type == pygame.JOYDEVICEREMOVED:
            joystick_changed = True
            # find the store joystick by its id
            for i, instance_id in enumerate(joystick_instance_ids):
                if event.instance_id == instance_id:
                    # removed
                    del joysticks[i]
                    del joystick_instance_ids[i]
                    print(f'Joystick {i} removed')
                    break
                pass
            pass
        # a click on screen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # for each predefined button
            for button_data in button_array:
                # get it rectangle on the screen
                button_rect = button_data['button_rectangle']
                # if the mouse click on the area of the button
                if button_rect.collidepoint(event.pos):
                    # get code of the button
                    code = button_data['code']
                    # change score if it is needed
                    if code == RED_DEC:
                        red_extra -= 1
                        pass
                    elif code == RED_INC:
                        red_extra += 1
                        pass
                    elif code == BLE_INC:
                        blue_extra += 1
                        pass
                    elif code == BLE_DEC:
                        blue_extra -= 1
                        pass
                    elif code == RED_PEN:
                        red_pen += 1
                        pass
                    elif code == BLE_PEN:
                        blue_pen += 1
                        pass
                    # move to next round
                    elif code == NEXT_ROUND:
                        control_button = NEXT_ROUND
                        pass
                    elif code == RESET:
                        control_button = RESET
                        pass
                    elif code == STOP:
                        control_button = STOP
                        pass
                    elif code == START_PAUSE:
                        control_button = START_PAUSE
                        pass
                    pass
                pass
            pass
        # quit program
        elif event.type == pygame.QUIT:
            run = False
    if run is True:
        # reset array of signal when joystick is plugged in or removed
        if joystick_changed is True:
            red_signal_arr, blue_signal_arr = reset_signal_arr(joysticks)
            pass
        pass
    return (red_signal_arr, blue_signal_arr, run,
            red_extra, blue_extra, red_pen, blue_pen, control_button)


def calculate_score(signal_arr):
    """
    calculate score based on joystick clicks
    :param signal_arr: an array of dictionaries
    :return:
    """
    score_arr = [1, 2, 3, 4]
    total = 0
    # from 1 to 4
    for score in score_arr:
        signals = []
        # iterate over array of joysticks
        for signal in signal_arr:
            # if there is a click from a joystick
            if signal[score] > 0:
                # mark its number of click
                signals.append(signal[score])
                pass
            pass
        # update final score when there are at least 2 click on the same button
        if len(signals) >= 2:
            # assume that the athlete cannot kick more than 1 same kick in 2 seconds
            #
            # idled time, waiting time before checking the score
            # 1 seconds is better than 2 seconds in case of HUBT team
            # it is set at final lines of "running" function
            total += score  # score * min(signals)
            pass
        pass
    return total


def update_score(red_signal_arr, blue_signal_arr, red_score, blue_score):
    """
    update score of each player
    :param red_signal_arr:
    :param blue_signal_arr:
    :param red_score:
    :param blue_score:
    :return:
    """
    red_score += calculate_score(red_signal_arr)
    blue_score += calculate_score(blue_signal_arr)
    return red_score, blue_score


def draw_button(screen, button_data: {}):
    """
    draw button on screen
    :param screen: the main screen
    :param button_data: dictionary
    :return:
    """
    button_text = button_data['button_text']
    button_rectangle = button_data['button_rectangle']
    BUTTON_HOVER_COLOR = button_data['BUTTON_HOVER_COLOR']
    BUTTON_COLOR = button_data['BUTTON_COLOR']
    BUTTON_TEXT_COLOR = button_data['BUTTON_TEXT_COLOR']
    button_font = button_data['button_font']

    # try to highly the button when the mouse is hovering above
    mouse_pos = pygame.mouse.get_pos()
    if button_rectangle.collidepoint(mouse_pos):
        color = BUTTON_HOVER_COLOR
        pass
    else:
        color = BUTTON_COLOR
        pass
    # draw the text and its box
    pygame.draw.rect(screen, color, button_rectangle)
    text_surface = button_font.render(button_text, True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rectangle.center)
    screen.blit(text_surface, text_rect)
    pass


def draw_all_buttons(screens, button_data_arr: []):
    for data in button_data_arr:
        draw_button(screens, data)
        pass
    pass


def creat_list_of_button(SCREEN_WIDTH, SCREEN_HEIGHT):
    '''
    define all buttons
    :param SCREEN_WIDTH:
    :param SCREEN_HEIGHT:
    :return:
    '''
    # array of button
    button_array = []

    # decreasing button of red
    btn_red_dec = {
        'code': RED_DEC,
        'button_text': '-',
        'button_rectangle': pygame.Rect(3 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9,
                                        80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (0, 0, 255),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_red_dec)
    # increasing button of red
    btn_red_inc = {
        'code': RED_INC,
        'button_text': '+',
        'button_rectangle': pygame.Rect(4.9 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9,
                                        80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (0, 0, 255),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_red_inc)
    # penalty button of red
    btn_red_pen = {
        'code': RED_PEN,
        'button_text': 'P',
        'button_rectangle': pygame.Rect(1.1 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9,
                                        80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (0, 0, 255),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_red_pen)

    # Increasing button of blue
    btn_blue_inc = {
        'code': BLE_INC,
        'button_text': '+',
        'button_rectangle': pygame.Rect(14 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9,
                                        80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 0, 0),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_blue_inc)
    # decreasing button of blue
    btn_blue_dec = {
        'code': BLE_DEC,
        'button_text': '-',
        'button_rectangle': pygame.Rect(12 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9,
                                        80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 0, 0),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_blue_dec)

    # decreasing button of blue
    btn_blue_pen = {
        'code': BLE_PEN,
        'button_text': 'P',
        'button_rectangle': pygame.Rect(16 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9,
                                        80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 0, 0),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_blue_pen)

    # start and pause button
    btn_start_pause = {
        'code': START_PAUSE,
        'button_text': 'Start',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 6.5 * SCREEN_HEIGHT / 9,
                                        150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_start_pause)

    # next round button
    btn_next_round = {
        'code': NEXT_ROUND,
        'button_text': 'Next Round',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 7 * SCREEN_HEIGHT / 9,
                                        150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_next_round)

    btn_stop_match = {
        'code': STOP,
        'button_text': 'Stop',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 7.5 * SCREEN_HEIGHT / 9,
                                        150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_stop_match)

    btn_reset_match = {
        'code': RESET,
        'button_text': 'Reset',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 8 * SCREEN_HEIGHT / 9,
                                        150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_reset_match)
    return button_array


def reset_start_pause_button(button_array, new_round=True):
    for item in button_array:
        if item['code'] == START_PAUSE:
            if new_round == True:
                item['button_text'] = 'Start'
                pass
            else:
                if item['button_text'] == 'Start':
                    item['button_text'] = 'Pause'
                    pass
                else:
                    item['button_text'] = 'Start'
                    pass
                pass
            break
        pass
    pass


def running():
    """
    run the game
    :return:
    """
    global MATCH_DURATION_CHOICE
    info = pygame.display.Info()
    # define screen size
    SCREEN_WIDTH = info.current_w - 10
    SCREEN_HEIGHT = info.current_h - 50

    # create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(
        "Tác giả: Lê Hoàng Long - Email: hoanglong1712@gmail.com - Thạc sĩ khoa học ngành Khoa học Dữ liệu & Trí tuệ nhân tạo")

    # define font of scores
    font_size = int(SCREEN_WIDTH / 2)
    font = pygame.font.SysFont("Futura", font_size)

    # define font of winning result
    winning_font_size = int(SCREEN_WIDTH / 8)
    winning_font = pygame.font.SysFont("Futura", winning_font_size)

    # define font for timer
    timer_font_size = int(SCREEN_WIDTH / 10)
    timer_font = pygame.font.SysFont("Futura", timer_font_size)

    # define font of round result
    round_font_size = int(SCREEN_WIDTH / 20)
    round_font = pygame.font.SysFont("Futura", round_font_size)

    # create clock for setting game frame rate
    clock = pygame.time.Clock()
    FPS = 20

    # create empty list to store joysticks
    joysticks = []
    # list of id of working joystick
    joystick_instance_ids = []

    # create background for each scores
    red_bg = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    blue_bg = pygame.Rect(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

    # game loop
    run = True

    # scores of red and blue
    # red = {1: [], 2: [], 3: [], 4: []}
    # blue = {1: [], 2: [], 3: [], 4: []}
    # scores from references
    red_signal_arr = []
    blue_signal_arr = []

    # current scores
    red_score = 0
    blue_score = 0

    # array of score
    scores = []
    # array of penalty score
    pen_scores = [[0, 0]]

    # current winning result
    red_win = 0
    blue_win = 0

    # winner message
    blue_winner = ""
    red_winner = ""

    # current round
    round_current = 1

    # Timer variables
    match_start_time = time.time()
    time_remaining = MATCH_DURATION_CHOICE  # Use the chosen duration
    round_paused = True
    round_ended = False  # New state for when timer hits zero

    # Load/Generate horn sound
    horn_sound = None
    try:
        # Load the generated sound data
        horn_sound = generate_horn_sound(duration=1.5, frequency1=400, frequency2=550)
    except Exception as e:
        print(f"Warning: Could not generate horn sound. Pygame or numpy error: {e}")

    sound_played_for_end = False  # Flag to ensure the horn only plays once per round end

    button_array = creat_list_of_button(SCREEN_WIDTH, SCREEN_HEIGHT)

    start_time = pygame.time.get_ticks()
    while run:
        # clock.tick(FPS)
        # Calculate time difference from last frame
        dt = clock.tick(FPS) / 1000.0  # Time in seconds since last tick

        # update background
        update_background(screen, red_bg, blue_bg)

        # Update timer
        if not round_paused and not round_ended:
            time_remaining -= dt
            if time_remaining <= 0:
                time_remaining = 0
                round_ended = True  # Round ends when timer hits zero
                pass
            pass
        # Sound Trigger Logic: Play horn only once when time is over
        if round_ended and horn_sound and not sound_played_for_end:
            horn_sound.play()
            sound_played_for_end = True

        # Display timer
        minutes = int(time_remaining / 60)
        seconds = int(time_remaining % 60)
        timer_text = f'{minutes:02}:{seconds:02}'
        draw_timer(screen, timer_font, timer_text, pygame.Color("yellow"),
                   SCREEN_WIDTH / 2, 5.6 * SCREEN_HEIGHT / 9)

        # joystick_num = pygame.joystick.get_count()

        update_signal_arr(joysticks, red_signal_arr, blue_signal_arr)

        # draw current scores
        white = (255, 255, 255)
        draw_score(screen, font, f'{red_score}', white,
                   1.2 * SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)
        draw_score(screen, font, f'{blue_score}', white,
                   4.8 * SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2)

        # draw current result of the match
        yellow = (255, 255, 0)
        draw_score(screen, winning_font, f'{red_win}', yellow,
                   9 * SCREEN_WIDTH / 20, 1 * SCREEN_HEIGHT / 10)
        draw_score(screen, winning_font, f'{blue_win}', yellow,
                   11 * SCREEN_WIDTH / 20, 1 * SCREEN_HEIGHT / 10)

        black = (0, 0, 0)
        # draw score of each round
        position = 5
        for i in range(len(pen_scores)):
            if i < len(scores):
                item = scores[i]
                draw_score(screen, round_font, f'{item[RED_INDEX]}', yellow,
                           9 * SCREEN_WIDTH / 20, position * SCREEN_HEIGHT / 20)
                draw_score(screen, round_font, f'{item[BLUE_INDEX]}', yellow,
                           11 * SCREEN_WIDTH / 20, position * SCREEN_HEIGHT / 20)
                pass
            pen_item = pen_scores[i]
            if pen_item[RED_INDEX] > 0:
                draw_score(screen, round_font, f'-{pen_item[RED_INDEX]}', black,
                           8 * SCREEN_WIDTH / 20, position * SCREEN_HEIGHT / 20)
                pass
            if pen_item[BLUE_INDEX] > 0:
                draw_score(screen, round_font, f'-{pen_item[BLUE_INDEX]}', black,
                           12 * SCREEN_WIDTH / 20, position * SCREEN_HEIGHT / 20)
                pass
            position += 1.5
            pass

        # draw winner message
        draw_score(screen, round_font, f'{red_winner}', yellow,
                   SCREEN_WIDTH / 4, 1 * SCREEN_HEIGHT / 10)
        draw_score(screen, round_font, f'{blue_winner}', yellow,
                   3 * SCREEN_WIDTH / 4, 1 * SCREEN_HEIGHT / 10)

        # draw current round number
        '''
        draw_score(screen, round_font, f'{round_current}', yellow,
                   10 * SCREEN_WIDTH / 20, 2 * SCREEN_HEIGHT / 10)
        '''

        red_signal_arr, blue_signal_arr, run, red_extra, blue_extra, \
            red_pen, blue_pen, control_button \
            = update_joysticks(joysticks, joystick_instance_ids,
                               red_signal_arr, blue_signal_arr, run,
                               button_array)

        # update score
        red_score += red_extra
        blue_score += blue_extra

        # update penalty can be done while pausing or at the end of the round
        pen_scores[-1][RED_INDEX] += red_pen
        pen_scores[-1][BLUE_INDEX] += blue_pen

        red_score += blue_pen
        blue_score += red_pen


        current_time = pygame.time.get_ticks()
        # convert from milliseconds to one tenth of seconds
        elapsed_time = (current_time - start_time) / 100

        if control_button == START_PAUSE:
            # control the timer
            if round_paused == True:
                round_paused = False
                pass
            else:
                round_paused = True
                pass
            reset_start_pause_button(button_array, new_round=False)
            pass
        elif control_button == NEXT_ROUND or control_button == STOP:
            round_current += 1
            # winner gets 1 mark
            # both players get 1 mark when the round ties
            if red_score > blue_score:
                red_win += 1
                pass
            elif red_score < blue_score:
                blue_win += 1
                pass
            else:
                blue_win += 1
                red_win += 1
                pass
            # add score to list of scores so that it could be showed on screen
            scores.append([red_score, blue_score])
            # reset current score of the round
            red_score = 0
            blue_score = 0

            # Reset timer and unpause for the new round
            time_remaining = MATCH_DURATION_CHOICE
            round_paused = True
            round_ended = False
            sound_played_for_end = False
            reset_start_pause_button(button_array)
            pen_scores.append([0, 0])

            # stop button is clicked
            if control_button == STOP:
                # update the final message
                blue_winner = "Winner"
                red_winner = "Winner"
                if red_win > blue_win:
                    blue_winner = "Loser"
                    pass
                elif red_win < blue_win:
                    red_winner = "Loser"
                    pass
                # show final score
                red_score = red_win
                blue_score = blue_win
                pass
            pass
        elif control_button == RESET:
            round_current = 1
            red_score = 0
            blue_score = 0
            red_win = 0
            blue_win = 0

            scores = []
            pen_scores.clear()
            pen_scores.append([0, 0])

            blue_winner = ""
            red_winner = ""

            # Reset timer and unpause for the new round
            time_remaining = MATCH_DURATION_CHOICE
            round_paused = True
            round_ended = False
            sound_played_for_end = False
            reset_start_pause_button(button_array)
            pass
        else:
            # idled time, waiting time before checking teh score
            # 1 seconds is better than 2 seconds in case of HUBT team
            IDLED_TIME = 10
            if elapsed_time >= IDLED_TIME:  # 20:
                # reference cannot update score after the horn has been blown
                # or when the round is paused
                if not sound_played_for_end and round_paused == False:
                    red_score, blue_score = update_score(
                        red_signal_arr, blue_signal_arr, red_score, blue_score)
                    pass
                red_signal_arr, blue_signal_arr = reset_signal_arr(joysticks)
                start_time = current_time
                pass
            pass

        draw_all_buttons(screen, button_array)
        # update display
        pygame.display.flip()
        pass
    pass


from tkinter import *
from tkinter import messagebox


def help_message():
    infor_text = '''
    Hướng dẫn sử dụng
    - Phần mềm tương thích với các loại tay cầm chơi game 
        như PS2, PS3 và PS4 cũng như Xbox
    - Điểm được tính khi có 2 tay cầm cùng cho điểm 1 lúc
    - Số lượng tay cầm tính điểm không hạn chế, 
        tối thiểu là 2 tay cầm và tối đa có thể lên đến 8 tay cầm,
        tùy thuộc vào sức mạnh của máy tính trung tâm 
    - Phần điều khiển lên xuống ở bên trái 
        dùng để tính điểm cho vận động viên màu xanh
    - Phần điều khiển bên phải 
        dùng để tính điểm cho vận động viên màu đỏ
    - Phầm mềm có 4 mức điểm cơ sở
        1 điểm là nút bấm trên cùng
        2 điểm là nút bấm bên phải
        3 điểm là nút bấm dưới cùng
        4 điểm là nút bấm bên trái
        ngoài ra có thể bấm tổ hợp nút để tính các mức điểm 5 hoặc 6
    - Nhấn nút Start để bắt đầu hiệp đấu, nút Pause để tạm dừng hiệp đấu
    - Thời gian trận đấu được cài đặt trước khi bắt đầu.
    - Khi hết giờ, còi sẽ báo hiệu, tất cả trọng tài sẽ bị chặn thao tác thay đổi điểm số
    '''
    messagebox.showinfo(title="Hướng dẫn", message=infor_text)
    pass


def splash_screen():
    root = Tk()
    width = 800
    height = 430
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    # root.overrideredirect(True)
    root.title("Phần mềm tính điểm thi đấu")
    root.config(background="#2F6C60")
    welcome_label = Label(text="Phần mềm tính điểm thi đấu đối kháng", bg="#2F6C60",
                          font=("Arial", 25, "bold"), fg="white")
    welcome_label.place(x=width / 7, y=height / 6)

    author_text = "Tác giả: Lê Hoàng Long"
    email_text = "Email: hoanglong1712@gmail.com"
    education_text = "Học vị: Thạc sĩ khoa học ngành Khoa học Dữ liệu & Trí tuệ nhân tạo"
    work_text = '''Cung cấp dịch vụ:
    - Phát triển các phần mềm tự động hóa, plugin phục vụ yêu cầu riêng lẻ và đặc thù
    - Giảng dạy, hỗ trợ học tập các ngành Công nghệ thông tin, Khoa học Máy tính 
      Khoa học Dữ liệu & Trí tuệ nhân tạo
    '''

    infor_label = Label(text=f'{author_text}\n{email_text}\n{education_text}\n{work_text}',
                        font=("Arial", 12, "bold"), bg="#2F6C60", fg="white",
                        anchor="w", justify="left")
    infor_label.place(x=width / 12, y=height / 3)

    # Add duration input
    duration_y = height * 3.5 / 5
    duration_label = Label(root, text="Thời gian trận đấu (giây):", bg="#2F6C60",
                           font=("Arial", 12, "bold"), fg="white")
    duration_label.place(x=width / 12, y=duration_y)

    time_choice_var = StringVar(root, value=str(MATCH_DURATION_CHOICE))
    duration_entry = Entry(root, textvariable=time_choice_var, width=10,
                           font=("Arial", 12))
    duration_entry.place(x=width / 12 + 250, y=duration_y)

    help_button = Button(root, text="Hướng dẫn", command=help_message,
                         font=("Arial", 15, "bold"), width=10)
    help_button.place(x=width * 3 / 5, y=height * 4 / 5)

    def close():
        # root.destroy()
        try:
            chosen_time = int(time_choice_var.get())
            if chosen_time > 0:
                global MATCH_DURATION_CHOICE
                MATCH_DURATION_CHOICE = chosen_time
                root.destroy()
            else:
                messagebox.showerror(title="Lỗi", message="Thời gian phải là số nguyên dương.")
        except ValueError:
            messagebox.showerror(title="Lỗi", message="Vui lòng nhập số nguyên hợp lệ cho thời gian.")
        pass

    exit_button = Button(root, text="Bắt đầu", command=close,
                         font=("Arial", 15, "bold"), width=10)
    exit_button.place(x=width * 1.3 / 5, y=height * 4 / 5)
    root.mainloop()
    pass


if __name__ == '__main__':
    splash_screen()
    pygame.init()

    # initialise the joystick module
    pygame.joystick.init()

    running()
    pygame.quit()
    pass
