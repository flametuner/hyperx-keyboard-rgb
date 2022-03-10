
from dataclasses import dataclass
from threading import Thread
from time import sleep
from KspHid import KspHid, KspHidHelper
from rgbcolor import BLACK
from models.PacketBuffer import PacketBuffer as pb

SKIP_COLORS = [6, 7, 14, 15, 22, 23, 30, 31, 38, 39, 44, 46, 47, 54, 55, 58, 60, 61,
               62, 63, 70, 71, 78, 79, 86, 87, 94, 95, 101, 102, 103, 109, 110, 111, 118, 119]

NA = 0xFFFFFFF

MATRIX = [
    [0,  NA,  1,  2,  3,  4,  5,  8,   9,  64,  NA,  65,  66,  67,  68, NA,  69,  72,  73],
    [10, NA, 11, 12, 13, 16, 17, 18, 19,  20,  74,  75,  76,  77,   80, NA,  81,  82,  73],
    [21, NA, 24, 25, 26, 27, 28, 29,  32,  84,  85,  88,  89,  90,  NA, NA,  92,  93,  96],
    [33, NA, 34, 35, 36, 37, 40, 41,  42,  97,  98,  99, 100, 101, 104, NA,  NA,  NA,  NA],
    [43, 44, 45, 48, 49, 50, 51, 52, 105, 106, 107, 108, 109,  NA, 112, NA,  NA, 113,  NA],
    [53, 56, 57, NA, NA, NA, 59, NA,  NA,  NA,  NA, 114, 115, 116, 117, NA, 120, 121, 122]
]
KEYS = {
    'CTRL_L': 53,
    'WIN': 56,
    'ALT_L': 57,
    'SPACE': 59,
    'ALT_R': 114,
    'FN': 115,
    'OPTION': 116,
    'CTRL_R': 117,
    'LEFT_ARROW': 120,
    'DOWN_ARROW': 121,
    'RIGHT_ARROW': 122,

    'SHIFT_L': 43,
    '\\': 44,
    'Z': 45,
    'X': 48,
    'C': 49,
    'V': 50,
    'B': 51,
    'N': 52,
    'M': 105,
    ',': 106,
    '.': 107,
    ';': 108,
    '/': 109,
    'SHIFT_R': 112,
    'UP_ARROW': 113,

    'CAPS': 33,
    'A': 34,
    'S': 35,
    'D': 36,
    'F': 37,
    'G': 40,
    'H': 41,
    'J': 42,
    'K': 97,
    'L': 98,
    'Ç': 99,
    '~': 100,
    ']': 101,
    'ENTER': 104,

    'TAB': 21,
    'Q': 24,
    'W': 25,
    'E': 26,
    'R': 27,
    'T': 28,
    'Y': 29,
    'U': 32,
    'I': 84,
    'O': 85,
    'P': 88,
    '´': 89,
    '[': 90,
    'DEL': 92,
    'END': 93,
    'PG_DOWN': 96,

    '\'': 10,
    '1': 11,
    '2': 12,
    '3': 13,
    '4': 16,
    '5': 17,
    '6': 18,
    '7': 19,
    '8': 20,
    '9': 74,
    '0': 75,
    '-': 76,
    '=': 77,
    'BKSPC': 80,
    'INS': 81,
    'HOME': 82,
    'PG_UP': 83,
    'ESC': 0,
    'F1': 1,
    'F2': 2,
    'F3': 3,
    'F4': 4,
    'F5': 5,
    'F6': 8,
    'F7': 9,
    'F8': 64,
    'F9': 65,
    'F10': 66,
    'F11': 67,
    'F12': 68,
    'PRT_SCR': 69,
    'SCRL_LK': 72,
    'PAUSE_BREAK': 73
}
BUFFER_LEN = 380
PACKET_SIZE = 48
PAYLOAD_SIZE = 60
TOTAL_COLORS = 123


@dataclass
class HyperXKeyboard:

    def __init__(self):
        usb_path = KspHidHelper.get_interface_path_for_pidvid(
            0x0951, 0x16e6, 2)
        self.socket = KspHid(usb_path)
        self.current_colors = [BLACK for _ in range(0, TOTAL_COLORS)]

    def set_key_color(self, char, color):
        key_id = KEYS[char]
        self.current_colors[key_id] = color

    def start(self):
        self.running = True
        self.thread = Thread(target = self.run)
        self.thread.start()

    def stop(self):
        self.running = False


    def wait(self):
        self.thread.join()

    def run(self):
        while self.running:
            self._send_color_packet()
            sleep(0.01)

    def _send_color_packet(self):
        keyboardBuffer = pb(BUFFER_LEN)

        offset = 0
        row_pos = 0

        for color_idx, color in enumerate(self.current_colors):
            if color_idx > 0 and color_idx % 16 == 0:
                offset += PACKET_SIZE
                row_pos = 0
            keyboardBuffer.replace_at_offset([color.g], row_pos + offset)
            keyboardBuffer.replace_at_offset([color.r], row_pos + offset + 16)
            keyboardBuffer.replace_at_offset([color.b], row_pos + offset + 32)

            row_pos += 1

        sentBytes = 0
        bytesToSend = len(keyboardBuffer)
        payloadSize = PAYLOAD_SIZE
        seq = 0
        while sentBytes < bytesToSend:
            if bytesToSend - sentBytes < payloadSize:
                payloadSize = bytesToSend - sentBytes
            packet = pb(64)
            packet.replace_at_offset([0xA2, seq, 0, payloadSize], 0)
            payload = keyboardBuffer.get_slice(sentBytes, payloadSize)
            packet.replace_at_offset(payload.get_raw(), 4)
            seq += 1
            self.socket.execute_packet_buffer(packet.get())
            sentBytes += payloadSize
