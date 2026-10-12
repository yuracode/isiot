# ---- Lv3 解答例:検知したら信号機を赤にする(02 と組み合わせ) ----
# 人がいる → 赤、人がいない → 緑
from machine import Pin
import time

# 人感センサー(05 のステップ)
pir = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15

# ★ 信号機(02 のステップ)
red    = Pin(2, Pin.OUT)               # GP2:赤
yellow = Pin(3, Pin.OUT)               # GP3:黄
green  = Pin(4, Pin.OUT)               # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

print("ウォームアップ中...")
all_off()
yellow.value(1)                        # ★ ウォームアップ中は黄で知らせる
time.sleep(30)
print("開始")

all_off()
green.value(1)                         # 最初は「人なし」= 緑
prev = 0

while True:
    now = pir.value()
    if now != prev:
        all_off()
        if now == 1:
            print("検知! → 赤")
            red.value(1)               # ★ 人がいる → 赤
        else:
            print("検知なし → 緑")
            green.value(1)             # ★ 人がいない → 緑
        prev = now
    time.sleep_ms(100)
