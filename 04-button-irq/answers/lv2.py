# ---- Lv2 解答例:赤の間に押されたら「予約しました」と表示する ----
# 考え方:
#   赤の5秒を「50ミリ秒 × 100回」に分けて、そのたびに目印(pressed)を見る
#   目印が立っていたら「予約しました」と表示して reserved を True にする
#   最後に reserved が True なら、目印を残したままにして次のサイクルへ
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

pressed = False                        # フラグ(目印)

def on_press(pin):
    global pressed
    pressed = True                     # ハンドラは短く。目印を立てるだけ

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

        # ★ 赤の5秒を細かく分けて、そのたびに目印を確認する
        reserved = False               # 予約されたかどうか
        for i in range(100):           # 50ms × 100回 = 5000ms = 5秒
            if pressed and not reserved:
                print("予約しました")
                reserved = True
            time.sleep_ms(50)

        red.value(0)
        green.value(1)
        print("緑に復帰")

        if reserved:
            pressed = True             # ★ 予約あり → 目印を立てて次のサイクルへ
        else:
            pressed = False            # 予約なし → 黄の間の押下などは無視

    time.sleep_ms(50)
