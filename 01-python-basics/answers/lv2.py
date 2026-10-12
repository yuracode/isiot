# ---- Lv2 解答例:点滅回数を関数の引数にする ----
# blink(回数) と呼ぶと、その回数だけ点滅する関数に作り変える
from machine import Pin
import time

led = Pin(25, Pin.OUT)     # 本体LED(GP25)。Pico W は Pin("LED", Pin.OUT)

# ---- 関数:times 回だけ点滅させる ----
# ★ ( ) の中に times を書くと、呼び出すときに数を渡せる(これを「引数」という)
def blink(times):
    for i in range(times):     # times 回くり返す
        led.value(1)           # 点灯
        time.sleep_ms(200)
        led.value(0)           # 消灯
        time.sleep_ms(200)

# ---- 呼び出してみる ----
print("3回点滅")
blink(3)                   # ★ 3 が times に入る
time.sleep(1)

print("5回点滅")
blink(5)                   # ★ 5 が times に入る
time.sleep(1)

# 1回、2回、3回…と回数を増やしながら点滅をくり返す
n = 1
while True:
    print(n, "回点滅")
    blink(n)
    time.sleep(1)          # 区切りが分かるように1秒休む
    n = n + 1
    if n > 5:              # 5回まで行ったら1回に戻す
        n = 1
