# ---- Lv1 解答例:点滅の速さを変える ----
# 元の basics.py から変えたのは blink() の中の待ち時間だけ
from machine import Pin   # Pin:Pico のピンを操作するための道具
import time               # time:待ち時間を作るための道具

# Pico 本体に付いているLED(GP25)を出力にする
# ※ Pico W の場合は Pin("LED", Pin.OUT) と書く
led = Pin(25, Pin.OUT)

# ---- 関数:LEDを1回だけ点滅させる ----
def blink():
    led.value(1)           # 点灯
    time.sleep_ms(50)      # ★ 200 → 50 に変更(速い点滅になる)
    led.value(0)           # 消灯
    time.sleep_ms(50)      # ★ 200 → 50 に変更

print("スタート")

# 3回点滅
for i in range(3):
    print(i + 1, "回目")
    blink()

time.sleep(1)              # 1秒待つ

# ずっと点滅
count = 0
while True:
    blink()
    count = count + 1
    if count % 10 == 0:    # 10回ごとに表示
        print(count, "回点滅しました")
