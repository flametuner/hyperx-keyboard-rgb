from KspHid import KspHidHelper, KspHid
from models.Buffer import Buffer as b
from models.Color import Color
from enum import Enum

class Keys(Enum):
     ESC = 0
     TILDE = 4
     TAB = 8
     CAPS = 12
     SHIFT = 16
     CTRL = 20
     ONE = 28
     Q = 32
     A = 36
     Z =40
     L_WIN = 44
     F1 = 48
     TWO = 52
     W = 56
     S = 60
     X = 64
     L_ALT = 68
     F2 =72
     THREE = 76
     E = 80
     D = 84
     C =88
     F3 =96
     FOUR = 100
     R = 104
     F = 108
     V = 112
     F4 = 120
     FIVE = 124
     T = 128
     G = 132
     B = 136
     SPACE = 140
     F5 = 144
     SIX = 148
     Y = 152
     H =156
     N =160
     F6 = 168
     SEVEN = 172
     U = 176
     J = 180
     M = 184
     F7 =192
     EIGHT = 196
     I = 200
     K = 204
     COMMA = 208
     R_ALT = 212
     F8 = 216
     NINE = 220
     O =224
     L =228
     POINT =232
     F9 =240
     ZERO = 244
     P =248
     SEMICOLON =252
     SLASH =256
     FN =260
     F10 =264
     MIN =268
     L_BRACKET =272
     N_SLASH_0 =276
     F11 = 288
     IS =292
     R_BRACKET =296
     OPTIONS =308
     F12 =312
     BACKSPACE = 316
     BACKSLASH = 320
     L_ENTER = 324
     R_SHIFT =328
     R_CTRL = 332
     PRINT_SCREEN =336
     INS = 340
     DEL = 344
     L_ARROW =356
     SCROLL_LOCK =360
     HOME = 364
     END = 368
     U_ARROW = 376
     D_ARROW = 380
     PAUSE_BREAK = 384
     PGUP = 388
     PGDN = 392
     R_ARROW =404
     NUMLK = 412
     N_7 = 416
     N_4 = 420
     N_1 = 424
     N_0 = 428
     N_SLASH = 436
     N_8 = 440
     N_5 = 444
     N_2 = 448
     N_STAR = 460
     N_9 = 464
     N_6 = 468
     N_3 = 472
     N_DOT = 476
     N_MIN = 484
     N_PLUS = 488
     N_ENTER = 500

class Keyboard():
    def __init__(self):
        self.vid = 0x0
        self.pid = 0x0
        self.interface = 0
        self.buffer_length = 64


        self.path = KspHidHelper.get_interface_path_for_pidvid(self.vid, self.pid, self.interface)
        if self.path is None:
            raise ValueError(f"Keyboard pid={self.pid}, vid={self.vid}, i={self.interface} not found!")
        self.device = KspHid(self.path)

        self.keyboard_color_buffer = self.__init_keyboard_color_buffer()

    def set_key_color(self, key: Keys, color: Color):
        self.keyboard_color_buffer.replace_at_offset(
            self.__get_key_color_instruction(color[0], color[1], color[2]),
            key.value
        )
    
    def reset_colors(self):
        self.keyboard_color_buffer = self.__init_keyboard_color_buffer()
    
    def commit_colors_to_keyboard(self):
        START_COLOR_PACKET = self.__get_keyboard_color_start_packet()

        TO_SEND = [START_COLOR_PACKET] + self.keyboard_color_buffer.split_into_buffers(self.buffer_length)
        for packet in TO_SEND:
            self.device.execute_packet_buffer(packet.get(), True)
    
    
    def __init_keyboard_color_buffer(self):
        BUFFER_LEN = self.buffer_length * 9
        BUFFER = b(self.buffer_length)
        for i in range(0, BUFFER_LEN, 64):
            BUFFER.replace_at_offset(self.__get_keyboard_color_packet().get_raw(), i)
        return BUFFER
    
    def __get_keyboard_color_packet(self):
        _packet_buffer = b(self.buffer_length)
        for i in range(0, self.buffer_length, len(self.__get_key_color_instruction())):
            _packet_buffer.replace_at_offset(self.__get_key_color_instruction(), i)
        return _packet_buffer
    
    def __get_keyboard_color_start_packet(self):
        _packet_buffer = b(self.buffer_length)
        _packet_buffer.replace_at_offset([0x04, 0xf2], 0)
        return _packet_buffer
    
    def __get_key_color_instruction(self, r=0, g=0, b=0):
        return [0x81,r,g,b]
