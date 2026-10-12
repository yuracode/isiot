# ---- Lv1 解答例:赤の秒数を変える ----
# 元の button_irq.py から変えたのは ★ の1行だけ
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

pressed = False                        # フラグ(目印)

def on_press(pin):
    global pressed                     # 外の pressed を書き換える宣言
    pressed = True                     # 目印を立てるだけ

button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

while True:
    if pressed:
        pressed = False
        print("ボタン押下")
        time.sleep_ms(3000)

        green.value(0)
        yellow.value(1)
        print("黄")
        time.sleep_ms(2000)

        yellow.value(0)
        red.value(1)
        print("赤(歩行者OK)")
        time.sleep_ms(8000)            # ★ 赤:5000 → 8000(8秒)に変更

        red.value(0)
        green.value(1)
        print("緑に復帰")

        pressed = False                # 途中の押下は無視

    time.sleep_ms(50)
