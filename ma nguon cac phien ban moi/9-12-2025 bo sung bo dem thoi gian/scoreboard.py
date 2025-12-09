import pygame

# indices of predefined  buttons
RED_DEC = 1
RED_INC = 2
BLE_DEC = 3
BLE_INC = 4


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

        # each joystick goes along with a dictionary in blue or red array
        i += 1
        pass
    pass


def reset_signal_arr(joysticks):
    '''
    reset all array after each 2 seconds
    :param joysticks:
    :return:
    '''
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
    '''
    take action when there is a click on the screen or a press on the joystick
    :param joysticks:
    :param joystick_instance_ids:
    :param red_signal_arr:
    :param blue_signal_arr:
    :param run:
    :param button_array:
    :return:
    '''
    joystick_changed = False

    # onscreen buttons
    red_extra = 0
    blue_extra = 0

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
    return red_signal_arr, blue_signal_arr, run, red_extra, blue_extra


def calculate_score(signal_arr):
    '''
    calculate score based on joystick clicks
    :param signal_arr: an array of dictionaries
    :return:
    '''
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
            total += score  # score * min(signals)
            pass
        pass
    return total


def update_score(red_signal_arr, blue_signal_arr, red_score, blue_score):
    '''
    update score of each player
    :param red_signal_arr:
    :param blue_signal_arr:
    :param red_score:
    :param blue_score:
    :return:
    '''
    red_score += calculate_score(red_signal_arr)
    blue_score += calculate_score(blue_signal_arr)
    return red_score, blue_score


def draw_button(screen, button_data: {}):
    '''
    draw button on screen
    :param screen: the main screen
    :param button_data: dictionary
    :return:
    '''
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

    return button_array


def running():
    '''
    run the game
    :return:
    '''
    info = pygame.display.Info()
    # define screen size
    SCREEN_WIDTH = info.current_w - 10
    SCREEN_HEIGHT = info.current_h - 50

    # create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Joysticks")

    # define font of scores
    font_size = int(SCREEN_WIDTH / 2)
    font = pygame.font.SysFont("Futura", font_size)

    # create clock for setting game frame rate
    clock = pygame.time.Clock()
    FPS = 20

    # create empty list to store joysticks
    joysticks = []
    # list of id of working joystick
    joystick_instance_ids = []

    # create background cor each scores
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

    button_array = creat_list_of_button(SCREEN_WIDTH, SCREEN_HEIGHT)

    start_time = pygame.time.get_ticks()
    while run:
        clock.tick(FPS)

        # update background
        update_background(screen, red_bg, blue_bg)

        # joystick_num = pygame.joystick.get_count()

        update_signal_arr(joysticks, red_signal_arr, blue_signal_arr)

        # draw current scores
        white = (255, 255, 255)
        draw_score(screen, font, f'{red_score}', white,
                   SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)
        draw_score(screen, font, f'{blue_score}', white,
                   3 * SCREEN_WIDTH / 4, SCREEN_HEIGHT / 2)

        red_signal_arr, blue_signal_arr, run, red_extra, blue_extra \
            = update_joysticks(joysticks, joystick_instance_ids,
                               red_signal_arr, blue_signal_arr, run,
                               button_array)

        red_score += red_extra
        blue_score += blue_extra

        current_time = pygame.time.get_ticks()
        # convert from milliseconds to one tenth of seconds
        elapsed_time = (current_time - start_time) / 100

        if elapsed_time >= 20:
            red_score, blue_score = update_score(
                red_signal_arr, blue_signal_arr, red_score, blue_score)
            red_signal_arr, blue_signal_arr = reset_signal_arr(joysticks)
            start_time = current_time
            pass
        draw_all_buttons(screen, button_array)
        # update display
        pygame.display.flip()
        pass
    pass


if __name__ == '__main__':
    pygame.init()

    # initialise the joystick module
    pygame.joystick.init()

    running()
    pygame.quit()
    pass
