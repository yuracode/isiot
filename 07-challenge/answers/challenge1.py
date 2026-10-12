# ---- 課題1 解答例:超音波で10cm以内に近づいたら信号機を赤にする ----
# 使うステップ:02(信号機)+ 06(超音波)
from machine import Pin, time_pulse_us
import time

# 信号機
red    = Pin(2, Pin.OUT)   # GP2:赤
yellow = Pin(3, Pin.OUT)   # GP3:黄
green  = Pin(4, Pin.OUT)   # GP4:緑

# 超音波センサー
trig = Pin(10, Pin.OUT)    # GP10:Trig
echo = Pin(11, Pin.IN)     # GP11:Echo ※分圧回路(1kΩ・2kΩ)経由

def all_off():
    for p in (red, yellow, green):
        p.value(0)

# 06 の read_cm() をそのまま使う
def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    return t / 58

while True:
    d = read_cm()
    all_off()
    if d is not None and d < 10:   # 測れていて、しかも10cm未満なら
        red.value(1)               # 近い → 赤
        print("{:.1f} cm 近い!→ 赤".format(d))
    else:
        green.value(1)             # 遠い(または測定不可)→ 緑
        print("遠い → 緑")
    time.sleep_ms(200)
