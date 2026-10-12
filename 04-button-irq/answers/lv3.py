# ---- Lv3 解答例:前回の押下から200ms以内は無視する(チャタリング対策) ----
# 考え方:
#   time.ticks_ms() は「Pico が動き始めてからのミリ秒」を返す
#   押されるたびに時刻を記録し、前回との差が200ms未満なら
#   チャタリング(接点のバタつき)とみなして無視する
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

pressed = False                        # フラグ(目印)
last_ms = 0                            # ★ 前回、押下を受け付けた時刻(ミリ秒)

def on_press(pin):
    global pressed, last_ms            # ★ 外の変数を2つ書き換える
    now = time.ticks_ms()              # ★ 今の時刻
    # ticks_diff(新, 古) で「何ミリ秒たったか」を正しく計算できる
    if time.ticks_diff(now, last_ms) < 200:
        return                         # ★ 200ms以内 → チャタリングなので無視
    last_ms = now                      # 受け付けた時刻を覚えておく
    pressed = True                     # 目印を立てる

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
        time.sleep_ms(5000)

        red.value(0)
        green.value(1)
        print("緑に復帰")

        pressed = False

    time.sleep_ms(50)
