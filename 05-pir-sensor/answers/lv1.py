# ---- Lv1 解答例:ウォームアップ時間を変える ----
# 元の pir_sensor.py から変えたのは ★ の行だけ
from machine import Pin
import time

pir = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー(何もないとき 0)
led = Pin("LED", Pin.OUT)                 # 本体LED("LED" と名前で指定)

WARMUP_SEC = 10                        # ★ ウォームアップの秒数(30 → 10)

print("ウォームアップ中...")
# ★ 残り秒数を1秒ごとに表示すると、待っている感じが分かりやすい
for i in range(WARMUP_SEC, 0, -1):     # 10, 9, 8, ... 1 と数を減らす
    print("あと", i, "秒")
    time.sleep(1)
print("開始")

prev = 0
while True:
    now = pir.value()
    if now != prev:                    # 変化したときだけ
        if now == 1:
            print("検知!")
        else:
            print("検知なし")
        led.value(now)
        prev = now
    time.sleep_ms(100)
