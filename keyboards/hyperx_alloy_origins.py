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
KeyRows = [
    [Keys.ESC, Keys.TILDE, Keys.TAB, Keys.CAPS, Keys.SHIFT, Keys.CTRL],
    [Keys.ONE, Keys.Q, Keys.A, Keys.Z, Keys.L_WIN],
    [Keys.F1, Keys.TWO, Keys.W, Keys.S, Keys.X, Keys.L_ALT],
    [Keys.F2, Keys.THREE, Keys.E, Keys.D, Keys.C],
    [Keys.F3, Keys.FOUR, Keys.R, Keys.F, Keys.V],
    [Keys.F4, Keys.FIVE, Keys.T, Keys.G, Keys.B, Keys.SPACE],
    [Keys.F5, Keys.SIX, Keys.Y, Keys.H, Keys.N],
    [Keys.F6, Keys.SEVEN, Keys.U, Keys.J, Keys.M],
    [Keys.F7, Keys.EIGHT, Keys.I, Keys.K, Keys.COMMA],
    [Keys.F8, Keys.NINE, Keys.O, Keys.L, Keys.POINT],
    [Keys.F9, Keys.ZERO, Keys.P, Keys.SEMICOLON, Keys.SLASH, Keys.FN]
]

class Keyboard():
    def __init__(self):
        self.vid = 0x0951
        self.pid = 0x16e5
        self.interface = 3
        self.buffer_length = 64


        self.path = KspHidHelper.get_interface_path_for_pidvid(self.vid, self.pid, self.interface)
        if self.path is None:
            raise ValueError(f"Keyboard pid={self.pid}, vid={self.vid}, i={self.interface} not found!")
        self.device = KspHid(self.path)

        self.keyboard_color_buffer = self.__init_keyboard_color_buffer()

    def set_key_color(self, key: Keys, color: Color):
        self.keyboard_color_buffer.replace_at_offset(
            self.__get_key_color_instruction(color.get()[0], color.get()[1], color.get()[2]),
            key.value
        )

    def reset_colors(self):
        self.keyboard_color_buffer = self.__init_keyboard_color_buffer()
    
    def commit_colors_to_keyboard(self):
        START_COLOR_PACKET = self.__get_keyboard_color_start_packet()

        TO_SEND = [START_COLOR_PACKET] + self.keyboard_color_buffer.split_into_buffers(self.buffer_length)
        for packet in TO_SEND:
            self.device.execute_packet_buffer(packet.get(), True)
    
    def set_game_mode(self, new_state):
        PACKETS = [None]*17

        b0 = b(self.buffer_length)
        b0.replace_at_offset([0x04, 0x57], 0)

        b1 = b(self.buffer_length)
        b1.replace_at_offset([new_state],4)
        b1.replace_at_offset([0xff], 12)

        b2 = b(self.buffer_length)
        b2.replace_at_offset([0x04, 0x02], 0)

        b3 = b(self.buffer_length)
        b3.replace_at_offset([0x04, 0x19], 0)

        b4 = b(self.buffer_length)
        b4.replace_at_offset([0x04, 0x21], 0)

        b5 = b(self.buffer_length)
        b6 = b5
        b7 = b5
        b8 = b5
        b9 = b5
        b10 = b5
        b11 = b5
        b12 = b5
        b13 = b5

        b14 = b(self.buffer_length)
        b14.replace_at_offset([0xaa, 0x55], 62)

        b15 = b2

        b16 = b(self.buffer_length)
        b16.replace_at_offset([0x04, 0x18], 0)

        PACKETS = [b0, b1, b2, b3, b4, b5, b6, b7, b8,b9, b10, b11,b12,b13,b14,b15,b16]

        for packet in PACKETS:
            self.device.execute_packet_buffer(packet.get(), True)

        


    def save_current_to_profile(self, profile_id):
        PACKETS = [None]*10
        PACKETS[0] = self.__get_function_start_packet()
        PACKETS[1] = self.__get_save_profile_2nd_packet(profile_id)
        
        packet_2_buffer = b(self.buffer_length)
        packet_2_buffer.replace_at_offset([0x08], 0)
        packet_2_buffer.replace_at_offset([0x22, 0x00, 0x01, 0xaa, 0x55], 59)
        PACKETS[2] = packet_2_buffer

        packet_3_buffer = b(self.buffer_length)
        packet_3_buffer.replace_at_offset([0x01, 0x01, 0x00, 0x10, 0x00, 0x00, 0xaa, 0x55], 56)
        PACKETS[3] = packet_3_buffer


        PACKETS[4] = self.__get_function_start_packet()

        PROFILE = [0x27, 0x37, 0x47]
        packet_5_buffer = b(self.buffer_length)
        packet_5_buffer.replace_at_offset([0x04, PROFILE[profile_id], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01],0)
        PACKETS[5] = packet_5_buffer

        packet_6_buffer = b(self.buffer_length)
        packet_6_buffer.replace_at_offset([profile_id, 0,0,0,0,0,0,0,0,0,0,0,0xff], 0)
        PACKETS[6] = packet_6_buffer

        packet_7_buffer = b(self.buffer_length)
        packet_7_buffer.replace_at_offset([0x04, 0x02], 0)
        PACKETS[7] = packet_7_buffer

        packet_8_buffer = b(self.buffer_length)
        packet_8_buffer.replace_at_offset([0x04, 0x19],0)
        PACKETS[8] = packet_8_buffer

        PROFILE = [0X31, 0X41, 0X51]
        packet_9_buffer = b(self.buffer_length)
        packet_9_buffer.replace_at_offset([0x04, PROFILE[profile_id], 0, 0, 0, 0, 0, 0, 0x0a], 0)
        PACKETS[9] = packet_9_buffer

        for packet in PACKETS:
            self.device.execute_packet_buffer(packet.get(), True)
    


    def __get_save_profile_2nd_packet(self, profile_id):
        PROFILE = [0x23, 0x33, 0x43]
        _packet_buffer = b(self.buffer_length)
        _packet_buffer.replace_at_offset([0x04, PROFILE[profile_id], 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02],0)
        return _packet_buffer

    def __get_function_start_packet(self):
        _packet_buffer = b(self.buffer_length)
        _packet_buffer.replace_at_offset([0x04, 0x02], 0)
        return _packet_buffer
    
    def __init_keyboard_color_buffer(self):
        BUFFER_LEN = self.buffer_length * 9
        BUFFER = b(BUFFER_LEN)
        for i in range(0, BUFFER_LEN, self.buffer_length):
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
