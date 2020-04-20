from keyboards.hyperx_alloy_origins import Keyboard, Keys
from models.Color import Color



k = Keyboard()
k.set_key_color(Keys.ESC, Color(255,0,0))
k.commit_colors_to_keyboard()
