# ---- Lv3 解答例:5回測った平均を表示して、値のブレを減らす ----
from machine import Pin, time_pulse_us
import time

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
    return t / 58

# ★ 関数:n 回測って平均を返す
def read_avg(n):
    total = 0              # 合計
    ok = 0                 # うまく測れた回数
    for i in range(n):
        d = read_cm()
        if d is not None:  # 測れたときだけ足す(None は足せない)
            total = total + d
            ok = ok + 1
        time.sleep_ms(30)  # 前の音の反射が消えるまで少し待つ
    if ok == 0:
        return None        # 1回も測れなかった
    return total / ok      # 平均 = 合計 ÷ 回数

while True:
    d = read_avg(5)        # ★ 5回の平均
    if d is None:
        print("測定不可")
    else:
        print("{:.1f} cm(5回平均)".format(d))
    time.sleep_ms(200)
