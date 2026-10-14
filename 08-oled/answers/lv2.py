# ---- Lv2 解答例:ボタンを押した回数を表示する ----
# 03 のタクトスイッチ(GP5・プルアップ)と組み合わせる
from machine import Pin, I2C
import ssd1306
import time

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # ★ GP5:ボタン(押すと 0)

count = 0
prev = 1                                # 前回のボタンの状態(1 = 押していない)

# ★ 関数:回数を画面に表示する
def show_count():
    oled.fill(0)
    oled.text("button:", 0, 0)
    oled.text(str(count) + " times", 0, 16)
    oled.show()

show_count()
while True:
    now = button.value()
    if prev == 1 and now == 0:          # ★ 押された瞬間だけ数える
        count = count + 1
        show_count()                    # ★ 変わったときだけ画面を書きかえる
        time.sleep_ms(50)               # チャタリング対策
    prev = now
    time.sleep_ms(10)
