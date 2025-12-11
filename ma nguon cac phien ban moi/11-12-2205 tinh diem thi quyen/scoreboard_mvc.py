import pygame
import time
from tkinter import *
from tkinter import messagebox
import numpy as np  # <<< ADDED: Required for generating sound data

# indices of predefined buttons
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

class Model:
    def __init__(self, match_duration):
        self.match_duration = match_duration
        self.red_score = 0
        self.blue_score = 0
        self.red_win = 0
        self.blue_win = 0
        self.round_current = 1
        self.scores = []  # List of [red, blue] per round
        self.pen_scores = [[0, 0]]  # Penalty scores per round
        self.red_winner = ""
        self.blue_winner = ""
        self.time_remaining = self.match_duration
        self.round_paused = True
        self.round_ended = False
        self.sound_played_for_end = False
        self.red_signal_arr = []
        self.blue_signal_arr = []
        self.joysticks = []
        self.joystick_instance_ids = []

    def reset_signals(self):
        self.red_signal_arr = [{1: 0, 2: 0, 3: 0, 4: 0} for _ in self.joysticks]
        self.blue_signal_arr = [{1: 0, 2: 0, 3: 0, 4: 0} for _ in self.joysticks]

    def update_scores(self, red_extra, blue_extra, red_pen, blue_pen):
        self.red_score += red_extra + blue_pen
        self.blue_score += blue_extra + red_pen
        if len(self.pen_scores) > 0:
            self.pen_scores[-1][RED_INDEX] += red_pen
            self.pen_scores[-1][BLUE_INDEX] += blue_pen

    def calculate_and_add_score(self):
        def calculate_score(signal_arr):
            score_arr = [1, 2, 3, 4]
            total = 0
            for score in score_arr:
                signals = [signal[score] for signal in signal_arr if signal[score] > 0]
                if len(signals) >= 2:
                    total += score
            return total

        self.red_score += calculate_score(self.red_signal_arr)
        self.blue_score += calculate_score(self.blue_signal_arr)

    def next_round(self):
        self.round_current += 1
        if self.red_score > self.blue_score:
            self.red_win += 1
        elif self.red_score < self.blue_score:
            self.blue_win += 1
        else:
            self.blue_win += 1
            self.red_win += 1
        self.scores.append([self.red_score, self.blue_score])
        self.red_score = 0
        self.blue_score = 0
        self.time_remaining = self.match_duration
        self.round_paused = True
        self.round_ended = False
        self.sound_played_for_end = False
        self.pen_scores.append([0, 0])

    def stop_match(self):
        self.next_round()  # Process current round
        self.blue_winner = "Winner"
        self.red_winner = "Winner"
        if self.red_win > self.blue_win:
            self.blue_winner = "Loser"
        elif self.red_win < self.blue_win:
            self.red_winner = "Loser"
        self.red_score = self.red_win
        self.blue_score = self.blue_win

    def reset_match(self):
        self.round_current = 1
        self.red_score = 0
        self.blue_score = 0
        self.red_win = 0
        self.blue_win = 0
        self.scores = []
        self.pen_scores = [[0, 0]]
        self.blue_winner = ""
        self.red_winner = ""
        self.time_remaining = self.match_duration
        self.round_paused = True
        self.round_ended = False
        self.sound_played_for_end = False

    def toggle_pause(self):
        self.round_paused = not self.round_paused

    def update_timer(self, dt):
        if not self.round_paused and not self.round_ended:
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.time_remaining = 0
                self.round_ended = True

    def should_play_sound(self, horn_sound):
        if self.round_ended and horn_sound and not self.sound_played_for_end:
            horn_sound.play()
            self.sound_played_for_end = True

    def update_joysticks(self):
        for i, joystick in enumerate(self.joysticks):
            name = joystick.get_name().lower()
            if "xbox" in name:
                zero, one, two, three = 3, 1, 0, 2
            elif 'twin' in name:
                zero, one, two, three = 4, 1, 0, 3
            else:
                zero, one, two, three = 0, 1, 2, 3

            if joystick.get_button(zero):
                self.red_signal_arr[i][1] += 1
            if joystick.get_button(one):
                self.red_signal_arr[i][2] += 1
            if joystick.get_button(two):
                self.red_signal_arr[i][3] += 1
            if joystick.get_button(three):
                self.red_signal_arr[i][4] += 1

            # Blue player
            if 'xbox' in name or 'twin' in name:
                hat_number = 0
                x, y = self.get_hat_position(joystick, hat_number)
                if (x, y) == (-1, 0):
                    self.blue_signal_arr[i][4] += 1
                if (x, y) == (1, 0):
                    self.blue_signal_arr[i][2] += 1
                if (x, y) == (0, -1):
                    self.blue_signal_arr[i][3] += 1
                if (x, y) == (0, 1):
                    self.blue_signal_arr[i][1] += 1
            else:
                horiz_move = joystick.get_axis(0)
                vert_move = joystick.get_axis(1)
                if horiz_move < -0.05:
                    self.blue_signal_arr[i][4] += 1
                if horiz_move > 0.05:
                    self.blue_signal_arr[i][2] += 1
                if vert_move > 0.05:
                    self.blue_signal_arr[i][3] += 1
                if vert_move < -0.05:
                    self.blue_signal_arr[i][1] += 1

    def get_hat_position(self, joystick, hat_number):
        try:
            return joystick.get_hat(hat_number)
        except (pygame.error, IndexError):
            return (0, 0)

    def add_joystick(self, joy):
        self.joysticks.append(joy)
        self.joystick_instance_ids.append(joy.get_instance_id())
        self.reset_signals()

    def remove_joystick(self, instance_id):
        for i, inst_id in enumerate(self.joystick_instance_ids):
            if inst_id == instance_id:
                del self.joysticks[i]
                del self.joystick_instance_ids[i]
                self.reset_signals()
                break

class View:
    def __init__(self, screen, font, winning_font, timer_font, round_font, red_bg, blue_bg, button_array):
        self.screen = screen
        self.font = font
        self.winning_font = winning_font
        self.timer_font = timer_font
        self.round_font = round_font
        self.red_bg = red_bg
        self.blue_bg = blue_bg
        self.button_array = button_array

    def update_background(self):
        self.screen.fill(pygame.Color("white"))
        pygame.draw.rect(self.screen, pygame.Color("red"), self.red_bg)
        pygame.draw.rect(self.screen, pygame.Color("blue"), self.blue_bg)

    def draw_score(self, text, color, centerX, centerY, font=None):
        if font is None:
            font = self.font
        image = font.render(text, True, color)
        size = font.size(text)
        self.screen.blit(image, (centerX - size[0] / 2, centerY - size[1] / 2))

    def draw_timer(self, text, color, centerX, centerY):
        self.draw_score(text, color, centerX, centerY, self.timer_font)

    def draw_buttons(self):
        for button_data in self.button_array:
            self.draw_button(button_data)

    def draw_button(self, button_data):
        button_text = button_data['button_text']
        button_rectangle = button_data['button_rectangle']
        BUTTON_HOVER_COLOR = button_data['BUTTON_HOVER_COLOR']
        BUTTON_COLOR = button_data['BUTTON_COLOR']
        BUTTON_TEXT_COLOR = button_data['BUTTON_TEXT_COLOR']
        button_font = button_data['button_font']

        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER_COLOR if button_rectangle.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(self.screen, color, button_rectangle)
        text_surface = button_font.render(button_text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rectangle.center)
        self.screen.blit(text_surface, text_rect)

    def render(self, model):
        self.update_background()

        # Draw current scores
        white = (255, 255, 255)
        self.draw_score(f'{model.red_score}', white, 1.2 * self.screen.get_width() / 6, self.screen.get_height() / 2)
        self.draw_score(f'{model.blue_score}', white, 4.8 * self.screen.get_width() / 6, self.screen.get_height() / 2)

        # Draw timer
        minutes = int(model.time_remaining / 60)
        seconds = int(model.time_remaining % 60)
        timer_text = f'{minutes:02}:{seconds:02}'
        self.draw_timer(timer_text, pygame.Color("yellow"), self.screen.get_width() / 2, 5.6 * self.screen.get_height() / 9)

        # Draw winning results
        yellow = (255, 255, 0)
        self.draw_score(f'{model.red_win}', yellow, 9 * self.screen.get_width() / 20, 1 * self.screen.get_height() / 10, self.winning_font)
        self.draw_score(f'{model.blue_win}', yellow, 11 * self.screen.get_width() / 20, 1 * self.screen.get_height() / 10, self.winning_font)

        # Draw round scores and penalties
        black = (0, 0, 0)
        position = 5
        for i in range(len(model.pen_scores)):
            if i < len(model.scores):
                item = model.scores[i]
                self.draw_score(f'{item[RED_INDEX]}', yellow, 9 * self.screen.get_width() / 20, position * self.screen.get_height() / 20, self.round_font)
                self.draw_score(f'{item[BLUE_INDEX]}', yellow, 11 * self.screen.get_width() / 20, position * self.screen.get_height() / 20, self.round_font)
            pen_item = model.pen_scores[i]
            if pen_item[RED_INDEX] > 0:
                self.draw_score(f'-{pen_item[RED_INDEX]}', black, 8 * self.screen.get_width() / 20, position * self.screen.get_height() / 20, self.round_font)
            if pen_item[BLUE_INDEX] > 0:
                self.draw_score(f'-{pen_item[BLUE_INDEX]}', black, 12 * self.screen.get_width() / 20, position * self.screen.get_height() / 20, self.round_font)
            position += 1.5

        # Draw winner messages
        self.draw_score(f'{model.red_winner}', yellow, self.screen.get_width() / 4, 1 * self.screen.get_height() / 10, self.round_font)
        self.draw_score(f'{model.blue_winner}', yellow, 3 * self.screen.get_width() / 4, 1 * self.screen.get_height() / 10, self.round_font)

        self.draw_buttons()

class Controller:
    def __init__(self, model, view, horn_sound):
        self.model = model
        self.view = view
        self.horn_sound = horn_sound
        self.clock = pygame.time.Clock()
        self.FPS = 20
        self.start_time = pygame.time.get_ticks()
        self.IDLED_TIME = 10  # In tenths of seconds
        pygame.joystick.init()
        self.run = True

    def handle_events(self):
        red_extra = 0
        blue_extra = 0
        red_pen = 0
        blue_pen = 0
        control_button = NOTHING
        joystick_changed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                self.model.add_joystick(joy)
                joystick_changed = True
            elif event.type == pygame.JOYDEVICEREMOVED:
                self.model.remove_joystick(event.instance_id)
                joystick_changed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_data in self.view.button_array:
                    if button_data['button_rectangle'].collidepoint(event.pos):
                        code = button_data['code']
                        if code == RED_DEC:
                            red_extra -= 1
                        elif code == RED_INC:
                            red_extra += 1
                        elif code == BLE_INC:
                            blue_extra += 1
                        elif code == BLE_DEC:
                            blue_extra -= 1
                        elif code == RED_PEN:
                            red_pen += 1
                        elif code == BLE_PEN:
                            blue_pen += 1
                        elif code == NEXT_ROUND:
                            control_button = NEXT_ROUND
                        elif code == RESET:
                            control_button = RESET
                        elif code == STOP:
                            control_button = STOP
                        elif code == START_PAUSE:
                            control_button = START_PAUSE

        if joystick_changed:
            self.model.reset_signals()

        return red_extra, blue_extra, red_pen, blue_pen, control_button

    def reset_start_pause_button(self, new_round=True):
        for item in self.view.button_array:
            if item['code'] == START_PAUSE:
                if new_round:
                    item['button_text'] = 'Start'
                else:
                    item['button_text'] = 'Pause' if item['button_text'] == 'Start' else 'Start'
                break

    def main_loop(self):
        while self.run:
            dt = self.clock.tick(self.FPS) / 1000.0

            self.model.update_timer(dt)
            self.model.should_play_sound(self.horn_sound)
            self.model.update_joysticks()

            red_extra, blue_extra, red_pen, blue_pen, control_button = self.handle_events()

            self.model.update_scores(red_extra, blue_extra, red_pen, blue_pen)

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.start_time) / 100

            if control_button == START_PAUSE:
                self.model.toggle_pause()
                self.reset_start_pause_button(new_round=False)
            elif control_button == NEXT_ROUND:
                self.model.next_round()
                self.reset_start_pause_button()
            elif control_button == STOP:
                self.model.stop_match()
                self.reset_start_pause_button()
            elif control_button == RESET:
                self.model.reset_match()
                self.reset_start_pause_button()
            else:
                if elapsed_time >= self.IDLED_TIME:
                    if not self.model.sound_played_for_end and not self.model.round_paused:
                        self.model.calculate_and_add_score()
                    self.model.reset_signals()
                    self.start_time = current_time

            self.view.render(self.model)
            pygame.display.flip()

# Helper functions remain the same
def generate_horn_sound(duration=4.5, frequency1=400, frequency2=550, volume=0.5):
    sample_rate = pygame.mixer.get_init()[0]
    n_samples = int(sample_rate * duration)
    time_array = np.linspace(0, duration, n_samples, False)
    note1 = np.sin(frequency1 * 2 * np.pi * time_array)
    note2 = np.sin(frequency2 * 2 * np.pi * time_array)
    combined_wave = (note1 * 0.7 + note2 * 0.5) / 1.2
    amplitude = int(32767 * volume)
    audio_data = (combined_wave * amplitude).astype(np.int16)
    stereo_data = np.column_stack([audio_data, audio_data])
    sound = pygame.sndarray.make_sound(stereo_data)
    return sound

def creat_list_of_button(SCREEN_WIDTH, SCREEN_HEIGHT):
    button_array = []
    # ... (same as original, no changes)
    btn_red_dec = {
        'code': RED_DEC,
        'button_text': '-',
        'button_rectangle': pygame.Rect(3 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9, 80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (0, 0, 255),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_red_dec)
    btn_red_inc = {
        'code': RED_INC,
        'button_text': '+',
        'button_rectangle': pygame.Rect(4.9 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9, 80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (0, 0, 255),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_red_inc)
    btn_red_pen = {
        'code': RED_PEN,
        'button_text': 'P',
        'button_rectangle': pygame.Rect(1.1 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9, 80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (0, 0, 255),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_red_pen)
    btn_blue_inc = {
        'code': BLE_INC,
        'button_text': '+',
        'button_rectangle': pygame.Rect(14 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9, 80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 0, 0),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_blue_inc)
    btn_blue_dec = {
        'code': BLE_DEC,
        'button_text': '-',
        'button_rectangle': pygame.Rect(12 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9, 80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 0, 0),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_blue_dec)
    btn_blue_pen = {
        'code': BLE_PEN,
        'button_text': 'P',
        'button_rectangle': pygame.Rect(16 * SCREEN_WIDTH / 18, 7 * SCREEN_HEIGHT / 9, 80, 80),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 0, 0),
        'BUTTON_TEXT_COLOR': (255, 255, 255),
        'button_font': pygame.font.Font(None, 100)
    }
    button_array.append(btn_blue_pen)
    btn_start_pause = {
        'code': START_PAUSE,
        'button_text': 'Start',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 6.5 * SCREEN_HEIGHT / 9, 150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_start_pause)
    btn_next_round = {
        'code': NEXT_ROUND,
        'button_text': 'Next Round',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 7 * SCREEN_HEIGHT / 9, 150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_next_round)
    btn_stop_match = {
        'code': STOP,
        'button_text': 'Stop',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 7.5 * SCREEN_HEIGHT / 9, 150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_stop_match)
    btn_reset_match = {
        'code': RESET,
        'button_text': 'Reset',
        'button_rectangle': pygame.Rect(8.7 * SCREEN_WIDTH / 20, 8 * SCREEN_HEIGHT / 9, 150, 35),
        'BUTTON_HOVER_COLOR': (70, 200, 70),
        'BUTTON_COLOR': (255, 255, 255),
        'BUTTON_TEXT_COLOR': (0, 0, 0),
        'button_font': pygame.font.Font(None, 30)
    }
    button_array.append(btn_reset_match)
    return button_array

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

def splash_screen():
    global MATCH_DURATION_CHOICE
    root = Tk()
    width = 800
    height = 430
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
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

    exit_button = Button(root, text="Bắt đầu", command=close,
                         font=("Arial", 15, "bold"), width=10)
    exit_button.place(x=width * 1.3 / 5, y=height * 4 / 5)
    root.mainloop()
    return MATCH_DURATION_CHOICE

if __name__ == '__main__':
    splash_screen()
    pygame.init()

    info = pygame.display.Info()
    SCREEN_WIDTH = info.current_w - 10
    SCREEN_HEIGHT = info.current_h - 50

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tác giả: Lê Hoàng Long - Email: hoanglong1712@gmail.com - Thạc sĩ khoa học ngành Khoa học Dữ liệu & Trí tuệ nhân tạo")

    font_size = int(SCREEN_WIDTH / 2)
    font = pygame.font.SysFont("Futura", font_size)

    winning_font_size = int(SCREEN_WIDTH / 8)
    winning_font = pygame.font.SysFont("Futura", winning_font_size)

    timer_font_size = int(SCREEN_WIDTH / 10)
    timer_font = pygame.font.SysFont("Futura", timer_font_size)

    round_font_size = int(SCREEN_WIDTH / 20)
    round_font = pygame.font.SysFont("Futura", round_font_size)

    red_bg = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    blue_bg = pygame.Rect(SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)

    button_array = creat_list_of_button(SCREEN_WIDTH, SCREEN_HEIGHT)

    horn_sound = None
    try:
        horn_sound = generate_horn_sound(duration=1.5, frequency1=400, frequency2=550)
    except Exception as e:
        print(f"Warning: Could not generate horn sound. Pygame or numpy error: {e}")

    model = Model(MATCH_DURATION_CHOICE)
    view = View(screen, font, winning_font, timer_font, round_font, red_bg, blue_bg, button_array)
    controller = Controller(model, view, horn_sound)
    controller.main_loop()

    pygame.quit()