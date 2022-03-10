


from time import sleep
from hyperx import HyperXKeyboard
from rgbcolor import RGBColor
from keyboard import on_press_key


def main():
    on_press_key('q', lambda e: print('Q'))
    on_press_key('w', lambda e: print('W'))
    on_press_key('e', lambda e: print('E'))
    on_press_key('r', lambda e: print('R'))


    hyperx = HyperXKeyboard()

    # keyboard.set_key_color('ESC', RGBColor(255, 0, 0))

    # keyboard.set_key_color('Q', RGBColor(0, 0, 255))
    # keyboard.set_key_color('W', RGBColor(0, 0, 255))
    # keyboard.set_key_color('E', RGBColor(0, 0, 255))
    # keyboard.set_key_color('R', RGBColor(0, 0, 255))
    # keyboard.set_key_color('F', RGBColor(255, 255, 0))
    # keyboard.set_key_color('D', RGBColor(0, 255, 0))

    # keyboard.set_key_color('F1', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F2', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F3', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F4', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F5', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F6', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F7', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F8', RGBColor(0, 255, 0))
    
    # keyboard.set_key_color('F9', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F10', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F11', RGBColor(0, 255, 0))
    # keyboard.set_key_color('F12', RGBColor(0, 255, 0))
    
    # keyboard.set_key_color('SPACE', RGBColor(0, 255, 0))

    
    hyperx.start()
    print("after")
    sleep(10)
    hyperx.stop()

    hyperx.wait()
    print("end")


if __name__ == "__main__":
    main()