# ---- Lv1 解答例:各色の秒数を変える ----
# 元の traffic_light.py から変えたのは time.sleep() の数字だけ(★の行)
from machine import Pin   # Pin:Pico のピンを操作するための道具
import time               # time:待ち時間を作るための道具

red    = Pin(2, Pin.OUT)   # GP2 に赤のLED
yellow = Pin(3, Pin.OUT)   # GP3 に黄のLED
green  = Pin(4, Pin.OUT)   # GP4 に緑のLED

def all_off():
    for p in (red, yellow, green):
        p.value(0)         # 消灯

# 配線チェック:1個ずつ点灯
for name, p in (("赤", red), ("黄", yellow), ("緑", green)):
    all_off()
    print(name, "点灯")
    p.value(1)
    time.sleep(1)
all_off()

# 信号のサイクル
while True:
    green.value(1)
    time.sleep(3)          # ★ 緑:5秒 → 3秒
    green.value(0)

    yellow.value(1)
    time.sleep(1)          # ★ 黄:2秒 → 1秒
    yellow.value(0)

    red.value(1)
    time.sleep(3)          # ★ 赤:5秒 → 3秒
    red.value(0)
