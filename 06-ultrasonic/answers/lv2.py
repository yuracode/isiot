# ---- Lv2 解答例:気温を変数にして音速を計算し直す ----
# 音速(m/秒)= 331.5 + 0.6 × 気温
# これを cm/μs に直して、距離 = 時間 × 音速 ÷ 2 で計算する
from machine import Pin, time_pulse_us
import time

TEMP = 25                 # ★ 今の気温(℃)。教室の温度計を見て変えよう

# ★ 音速を計算する
speed_m = 331.5 + 0.6 * TEMP           # m/秒  (25℃なら 346.5)
speed_cm_us = speed_m * 100 / 1000000  # cm/μs(m→cm で ×100、秒→μs で ÷100万)
print("気温", TEMP, "℃ → 音速", speed_m, "m/秒")

trig = Pin(10, Pin.OUT)   # GP10:Trig
echo = Pin(11, Pin.IN)    # GP11:Echo ※分圧回路経由

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    # ★ t / 58 のかわりに、計算した音速を使う(往復なので ÷2)
    return t * speed_cm_us / 2

while True:
    d = read_cm()
    if d is None:
        print("測定不可")
    else:
        print("{:.1f} cm".format(d))
    time.sleep_ms(200)
