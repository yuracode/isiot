# ---- Lv1 解答例:表示する文字と位置を変える ----
# 元の oled.py のあいさつ部分を、★ のように変えた例
from machine import Pin, I2C
import ssd1306

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)   # SDA=GP18、SCL=GP19
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text("My name is", 0, 0)     # ★ 文字を変更
oled.text("PICO TARO", 28, 28)    # ★ x=28, y=28 で、まん中あたりに表示
oled.rect(16, 20, 96, 24, 1)      # ★ 名前を囲む枠
oled.show()
