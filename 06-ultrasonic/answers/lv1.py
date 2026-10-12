# ---- Lv1 解答例:測る間隔を変える ----
# 元の ultrasonic.py から変えたのは ★ の行だけ
from machine import Pin, time_pulse_us
import time

trig = Pin(10, Pin.OUT)   # GP10:Trig(出力)
echo = Pin(11, Pin.IN)    # GP11:Echo(入力)※分圧回路(1kΩ・2kΩ)経由

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)              # 10μs だけ 1 → 超音波を出す
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)   # 往復の時間(μs)
    if t < 0:
        return None            # 測れなかった
    return t / 58              # 時間 ÷ 58 = 距離(cm)

while True:
    d = read_cm()
    if d is None:
        print("測定不可")
    else:
        print("{:.1f} cm".format(d))
    time.sleep_ms(1000)        # ★ 200 → 1000(1秒ごと)に変更
