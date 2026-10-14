# ---- Lv3 解答例:超音波センサーの距離を数字とバーで表示する ----
# 06 の read_cm() をそのまま使う
from machine import Pin, I2C, time_pulse_us
import ssd1306
import time

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

trig = Pin(10, Pin.OUT)   # GP10:Trig
echo = Pin(11, Pin.IN)    # GP11:Echo ※分圧回路(1kΩ・2kΩ)経由

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    return t / 58

MAX_CM = 50               # ★ バーがいっぱいになる距離

while True:
    d = read_cm()
    oled.fill(0)
    oled.text("distance", 0, 0)
    if d is None:
        oled.text("---", 0, 16)
    else:
        oled.text("{:.1f} cm".format(d), 0, 16)
        # ★ 距離をバーの長さ(0〜128ドット)に変える
        w = int(d / MAX_CM * 128)
        if w > 128:
            w = 128                       # 画面からはみ出さないように
        oled.rect(0, 40, 128, 16, 1)      # 外の枠
        oled.fill_rect(0, 40, w, 16, 1)   # 中身(ぬりつぶし)
    oled.show()
    time.sleep_ms(200)
