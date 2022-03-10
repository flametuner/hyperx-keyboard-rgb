import hid
from time import sleep

class KspHid():
    def __init__(self, path: bytes):
        self.path = path
        self.hid = hid.device()

        self.hid.open_path(self.path)
        self.hid.set_nonblocking(1)

    def execute_packet_buffer(self, packet_buffer):
        self.hid.write(packet_buffer)


class KspHidHelper():
    @staticmethod
    def get_interface_path_for_pidvid(vid, pid, interface_number):
        for d in hid.enumerate():
            if d['vendor_id'] == vid and d['product_id'] == pid and d['interface_number'] == interface_number:
                return d['path']
        return None