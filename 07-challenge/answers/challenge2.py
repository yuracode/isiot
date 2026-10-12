# ---- 課題2 解答例:人感センサーが反応したら黄を点滅させる ----
# 使うステップ:02(信号機)+ 05(人感センサー)
from machine import Pin
import time

pir    = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー
red    = Pin(2, Pin.OUT)                  # GP2:赤
yellow = Pin(3, Pin.OUT)                  # GP3:黄
green  = Pin(4, Pin.OUT)                  # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
print("ウォームアップ中...")
time.sleep(30)
print("開始")

while True:
    if pir.value() == 1:       # 検知している間は
        yellow.value(1)        # 黄を点けて
        time.sleep_ms(300)
        yellow.value(0)        # 消して
        time.sleep_ms(300)     # → これをくり返すので点滅になる
    else:
        yellow.value(0)        # 検知していないときは消しておく
        time.sleep_ms(100)
