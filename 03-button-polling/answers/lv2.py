# ---- Lv2 解答例:ボタンを押した回数を数えて Shell に表示する ----
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

count = 0                              # ★ 押した回数を数える変数(最初は0)

while True:
    if button.value() == 0:
        time.sleep_ms(20)              # チャタリング対策
        if button.value() == 0:
            count = count + 1          # ★ 1 増やす
            print("ボタン押下", count, "回目")   # ★ 回数も表示
            time.sleep(3)

            green.value(0)
            yellow.value(1)
            print("黄")
            time.sleep(2)

            yellow.value(0)
            red.value(1)
            print("赤(歩行者OK)")
            time.sleep(5)

            red.value(0)
            green.value(1)
            print("緑に復帰")

            while button.value() == 0:
                time.sleep_ms(10)

    time.sleep_ms(10)
