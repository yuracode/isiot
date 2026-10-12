# ---- Lv2 解答例:赤の前に黄を3回点滅させる ----
# 黄の部分を「for で3回くり返す点滅」に作り変える
from machine import Pin
import time

red    = Pin(2, Pin.OUT)   # GP2:赤
yellow = Pin(3, Pin.OUT)   # GP3:黄
green  = Pin(4, Pin.OUT)   # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

# 配線チェック:1個ずつ点灯
for name, p in (("赤", red), ("黄", yellow), ("緑", green)):
    all_off()
    print(name, "点灯")
    p.value(1)
    time.sleep(1)
all_off()

while True:
    green.value(1)
    time.sleep(5)
    green.value(0)

    # ★ ここが変わった:黄を3回点滅
    for i in range(3):         # 3回くり返す
        yellow.value(1)        # 点ける
        time.sleep_ms(300)     # 0.3秒
        yellow.value(0)        # 消す
        time.sleep_ms(300)     # 0.3秒

    red.value(1)
    time.sleep(5)
    red.value(0)
