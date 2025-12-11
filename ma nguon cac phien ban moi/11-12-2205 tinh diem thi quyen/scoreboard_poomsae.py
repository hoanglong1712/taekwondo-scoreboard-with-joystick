import pygame

ACCURACY_INDEX = 0
PRESENTATION_INDEX = 1

INIT_ACCURACY_SCORE = 4.0
INIT_PRESENTATION_SCORE = 6.0

DEFAULT_ACCURACY_BG_COLOR = '#2a2b2a'
DEFAULT_PRESENTATION_BG_COLOR = '#575657'
IGNORED_ACCURACY_BG_COLOR = '#d3801a'
IGNORED_PRESENTATION_BG_COLOR = '#dbcb38'
BLUE_REF_BG_COLOR = '#0052cb'

NORMAL_COLOR = '#ffffff'
IGNORED_COLOR = '#000000'

MAIN_BG_COLOR = "#00173e"

ACC_MINOR_ERROR = 0.1
ACC_MAJOR_ERROR = 0.3
PRE_DEFAULT_ERROR = 0.2

# indices of predefined  buttons
RESET = 6


def update_joysticks(joysticks: {}, scores: {}, button_array: []):
    run = True
    # event handler
    for event in pygame.event.get():
        # a new device is added
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            # store the new joystick
            joysticks[joy.get_instance_id()] = joy
            print(f'Joystick {joy.get_instance_id()} added')
            scores[joy.get_instance_id()] = [INIT_ACCURACY_SCORE, INIT_PRESENTATION_SCORE]
            pass
        # a device is removed
        elif event.type == pygame.JOYDEVICEREMOVED:
            if event.instance_id in joysticks.keys():
                joysticks.pop(event.instance_id)
                scores.pop(event.instance_id)
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
                    if code == RESET:
                        for key, item in scores.items():
                            item[ACCURACY_INDEX] = INIT_ACCURACY_SCORE
                            item[PRESENTATION_INDEX] = INIT_PRESENTATION_SCORE
                            pass
                        pass
                pass
            pass
            # quit program
        elif event.type == pygame.QUIT:
            run = False
            pass
        pass
    return run


def draw_box(screen, box_data: {}):
    text = box_data['text']
    color = box_data['color']
    bg_color = box_data['bg_color']
    rectangle = box_data['rectangle']
    font = box_data['font']
    # draw the text and its box
    pygame.draw.rect(screen, bg_color, rectangle)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rectangle.center)
    screen.blit(text_surface, text_rect)
    pass


def draw_ref_id(screen, ref_id):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    box_data = {
        'text': f'J{ref_id}',
        'color': NORMAL_COLOR,
        'bg_color': BLUE_REF_BG_COLOR,
        'rectangle': pygame.Rect(0.1 * SCREEN_WIDTH / 20,
                                 1.1 * ref_id * SCREEN_HEIGHT / 12, 150, 50),
        'font': pygame.font.Font(None, 50)}
    draw_box(screen, box_data)
    pass


def draw_acc_score(screen, ref_id, accuracy, acc_removed):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    box_data = {
        'text': f'{accuracy:.1f}',
        'color': IGNORED_COLOR if acc_removed else NORMAL_COLOR,
        'bg_color': IGNORED_ACCURACY_BG_COLOR if acc_removed else DEFAULT_ACCURACY_BG_COLOR,
        'rectangle': pygame.Rect(0.1 * SCREEN_WIDTH / 20 + SCREEN_WIDTH / 10,
                                 1.1 * ref_id * SCREEN_HEIGHT / 12, 150, 50),
        'font': pygame.font.Font(None, 50)}
    draw_box(screen, box_data)
    pass


def draw_pre_score(screen, ref_id, accuracy, acc_removed):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    box_data = {
        'text': f'{accuracy:.1f}',
        'color': IGNORED_COLOR if acc_removed else NORMAL_COLOR,
        'bg_color': IGNORED_PRESENTATION_BG_COLOR if acc_removed else DEFAULT_PRESENTATION_BG_COLOR,
        'rectangle': pygame.Rect(0.1 * SCREEN_WIDTH / 20 + 2.2 * SCREEN_WIDTH / 10,
                                 1.1 * ref_id * SCREEN_HEIGHT / 12, 150, 50),
        'font': pygame.font.Font(None, 50)}
    draw_box(screen, box_data)
    pass


def draw_ref_score(screen, ref_id, accuracy, presentation, acc_removed, pre_removed):
    draw_ref_id(screen, ref_id)
    draw_acc_score(screen, ref_id, accuracy, acc_removed)
    draw_pre_score(screen, ref_id, presentation, pre_removed)
    pass


def get_ref_score(scores: {}):
    ref_scores = []
    sorted_items = dict(sorted(scores.items()))

    values = sorted_items.values()
    min_acc = INIT_ACCURACY_SCORE
    min_pre = INIT_PRESENTATION_SCORE
    max_acc = 0
    max_pre = 0
    for value in sorted_items.values():
        acc = value[ACCURACY_INDEX]
        if acc > max_acc:
            max_acc = acc
            pass
        if acc < min_acc:
            min_acc = acc
            pass
        pre = value[PRESENTATION_INDEX]
        if pre > max_pre:
            max_pre = pre
            pass
        if pre < min_pre:
            min_pre = pre
            pass
        pass
    i = 0
    max_acc_used = False
    min_acc_used = False
    max_pre_used = False
    min_pre_used = False

    acc_sum = 0.0
    acc_num = 0
    pre_sum = 0.0
    pre_num = 0
    for key, value in sorted_items.items():
        acc = value[ACCURACY_INDEX]
        pre = value[PRESENTATION_INDEX]
        acc_removed = False
        pre_removed = False
        if len(sorted_items) > 2:
            if acc == max_acc and max_acc_used == False:
                acc_removed = True
                max_acc_used = True
                pass
            if acc == min_acc and min_acc_used == False:
                acc_removed = True
                min_acc_used = True
                pass

            if pre == max_pre and max_pre_used == False:
                pre_removed = True
                max_pre_used = True
                pass
            if pre == min_pre and min_pre_used == False:
                pre_removed = True
                min_pre_used = True
                pass
            if not acc_removed:
                acc_sum += acc
                acc_num += 1
                pass
            if not pre_removed:
                pre_sum += pre
                pre_num += 1
                pass
            pass
        else:
            acc_sum += acc
            acc_num += 1
            pre_sum += pre
            pre_num += 1
            pass
        ref_scores.append((i + 1, acc, pre, acc_removed, pre_removed))
        i += 1
        pass

    return (ref_scores,
            acc_sum / acc_num if acc_num > 0 else 0,
            pre_sum / pre_num if pre_num > 0 else 0)

def draw_acc_avg(screen, font, text, color, next_ref_id):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    box_data = {
        'text': f'{text}',
        'color': color,
        'bg_color': MAIN_BG_COLOR,
        'rectangle': pygame.Rect(0.1 * SCREEN_WIDTH / 20 + SCREEN_WIDTH / 10,
                                 1.1 * next_ref_id * SCREEN_HEIGHT / 12, 150, 50),
        'font': font}
    draw_box(screen, box_data)
    pass

def draw_pre_avg(screen, font, text, color, next_ref_id):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    box_data = {
        'text': f'{text}',
        'color': color,
        'bg_color': MAIN_BG_COLOR,
        'rectangle': pygame.Rect(0.1 * SCREEN_WIDTH / 20 + 2.2 * SCREEN_WIDTH / 10,
                                 1.1 * next_ref_id * SCREEN_HEIGHT / 12, 150, 50),
        'font': font}
    draw_box(screen, box_data)
    pass

def draw_final_score(screen, font, text, color):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    box_data = {
        'text': f'{text}',
        'color': color,
        'bg_color': MAIN_BG_COLOR,
        'rectangle': pygame.Rect( 1.3 * SCREEN_WIDTH / 2,
                                 SCREEN_HEIGHT / 2, 150, 50),
        'font': font}
    draw_box(screen, box_data)
    pass

def draw_scores(screen, scores: {}):
    ref_scores, acc_avg, pre_avg = get_ref_score(scores)
    for item in ref_scores:
        ref_id, accuracy, presentation, acc_removed, pre_removed = item
        draw_ref_score(screen, ref_id, accuracy, presentation, acc_removed, pre_removed)
        pass
    text_font = pygame.font.Font(None, 80)
    yellow = (255, 255, 0)
    draw_acc_avg(screen, text_font, f'{acc_avg:.2f}',
              yellow, len(ref_scores) + 1)
    draw_pre_avg(screen, text_font, f'{pre_avg:.2f}',
                 yellow, len(ref_scores) + 1)
    final_score_font = pygame.font.Font(None, int( screen.get_width() / 4))

    draw_final_score(screen, final_score_font, f'{ (pre_avg + acc_avg):.2f}',
                 yellow)
    pass

def update_signal(joysticks: {}, scores: {}):
    for key, joy in joysticks.items():
        zero = 0
        one = 1
        two = 2
        three = 3
        name = joy.get_name().lower()
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
        score_item = scores[key]
        if joy.get_button(zero):
            score_item[ACCURACY_INDEX] -= ACC_MINOR_ERROR
            pass
        elif joy.get_button(one):
            score_item[ACCURACY_INDEX] -= ACC_MAJOR_ERROR
            pass
        elif joy.get_button(two):
            score_item[PRESENTATION_INDEX] -= PRE_DEFAULT_ERROR
            pass
        if score_item[ACCURACY_INDEX] < 0.0:
            score_item[ACCURACY_INDEX] = 0.0
            pass
        if score_item[PRESENTATION_INDEX] < 0.0:
            score_item[PRESENTATION_INDEX] = 0.0
            pass
        pass
    pass

def creat_list_of_button(screen):
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    # array of button
    button_array = []
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

def running():
    info = pygame.display.Info()
    # define screen size
    SCREEN_WIDTH = info.current_w - 10
    SCREEN_HEIGHT = info.current_h - 50

    # create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(
        "Tác giả: Lê Hoàng Long - Email: hoanglong1712@gmail.com - Thạc sĩ khoa học ngành Khoa học Dữ liệu & Trí tuệ nhân tạo")

    # game loop
    run = True
    # create clock for setting game frame rate
    clock = pygame.time.Clock()
    FPS = 20

    # create an empty dictionary to store joysticks
    joysticks = {}
    # a dictionary of scores, each item belongs to one joystick
    # marked by joystick ID
    scores = {}

    button_array = creat_list_of_button(screen)

    start_time = pygame.time.get_ticks()
    while run:
        clock.tick(FPS)

        run = update_joysticks(joysticks, scores, button_array)
        current_time = pygame.time.get_ticks()
        # convert from milliseconds to one tenth of seconds
        elapsed_time = (current_time - start_time) / 100

        # idled time, waiting time before checking the score
        # 1 seconds is good for poomsae
        IDLED_TIME = 2
        if elapsed_time >= IDLED_TIME:  # 20:
            update_signal(joysticks, scores)
            start_time = current_time
            pass
        pass


        # fill screen with black color
        screen.fill(pygame.Color(MAIN_BG_COLOR))

        draw_scores(screen, scores)

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
    - Điểm được tính độc lập
    - Số lượng tay cầm tính điểm không hạn chế, 
        tối thiểu là 1 tay cầm và tối đa có thể lên đến 8 tay cầm,
        tùy thuộc vào sức mạnh của máy tính trung tâm
    - Phần điều khiển bên phải 
        dùng để tính điểm cho vận động viên 
    - Phầm mềm có 4 mức điểm cơ sở
        Nút bấm trên cùng: trừ 0.1 điểm cho mỗi lỗi kỹ thuật nhỏ
        Nút bấm bên phải: trừ 0.3 điểm cho mỗi lỗi kỹ thuật lớn
        Nút bấm dưới cùng: trừ 0.2 điểm cho mỗi lỗi trình diễn        
    - Nhấn nút Reset để bắt đầu chấm điểm
    - Những điểm bị đổi màu là những điểm không được tính vào tổng điểm cuối cùng
    - Nếu có dưới 2 trọng tài thì không áp dụng cơ chế đổi màu và 
    không thực hiện ngăn chặn tính vào tổng điểm cuối cùng     
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
    welcome_label = Label(text="Phần mềm tính điểm thi đấu quyền", bg="#2F6C60",
                          font=("Arial", 25, "bold"), fg="white")
    welcome_label.place(x=width / 7, y=height / 6)

    author_text = "Tác giả: Lê Hoàng Long"
    email_text = "Email: hoanglong1712@gmail.com, Điện thoại: 0359568862"
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

    help_button = Button(root, text="Hướng dẫn", command=help_message,
                         font=("Arial", 15, "bold"), width=10)
    help_button.place(x=width * 3 / 5, y=height * 4 / 5)

    def close():
        root.destroy()
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
