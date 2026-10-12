# ---- Lv2 解答例:検知した回数を数える ----
from machine import Pin
import time

pir = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー
led = Pin(25, Pin.OUT)                 # 本体LED

print("ウォームアップ中...")
time.sleep(30)
print("開始")

prev = 0
count = 0                              # ★ 検知した回数(最初は0)

while True:
    now = pir.value()
    if now != prev:
        if now == 1:
            # ★ 0 → 1 に変わったときだけ数える
            #   (1 のあいだずっと数えると、1回の検知で何百回にもなってしまう)
            count = count + 1
            print("検知!", count, "回目")
        else:
            print("検知なし")
        led.value(now)
        prev = now
    time.sleep_ms(100)
