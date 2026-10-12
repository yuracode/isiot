# ---- Lv3 解答例:モールス信号で SOS を出す ----
# 「点滅回数」だけでなく「点灯の長さ」も引数にして、
# 短い光(・)と長い光(-)を組み合わせる
from machine import Pin
import time

led = Pin(25, Pin.OUT)     # 本体LED(GP25)。Pico W は Pin("LED", Pin.OUT)

# ---- 関数:on_ms ミリ秒の点灯を times 回くり返す ----
# 引数を2つにすると、回数と長さの両方を変えられる
def blink(times, on_ms):
    for i in range(times):
        led.value(1)
        time.sleep_ms(on_ms)   # 点灯している長さ
        led.value(0)
        time.sleep_ms(200)     # 光と光の間のすき間

# ---- 関数:SOS を1回出す ----
# S = ・・・(短く3回)、O = ---(長く3回)
def sos():
    blink(3, 200)          # S:短い光を3回
    blink(3, 600)          # O:長い光を3回
    blink(3, 200)          # S:短い光を3回

while True:
    print("SOS")
    sos()
    time.sleep(2)          # 2秒あけてくり返す
