

from dataclasses import dataclass

@dataclass
class RGBColor():
    r: int
    g: int
    b: int

    def __str__(self):
        return f"{self.r}, {self.g}, {self.b}"

# create a enum

WHITE = RGBColor(255, 255, 255)
RED = RGBColor(255, 0, 0)
GREEN = RGBColor(0, 255, 0)
BLUE = RGBColor(255, 255, 255)
YELLOW = RGBColor(255, 255, 0)
MAGENTA = RGBColor(255, 0, 255)
CYAN = RGBColor(0, 255, 255)
BLACK = RGBColor(0, 0, 0)