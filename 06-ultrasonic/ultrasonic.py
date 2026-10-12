# ---- 必要な道具を読み込む ----
# time_pulse_us:ピンが HIGH になっている時間を μs(100万分の1秒)単位で測る道具
from machine import Pin, time_pulse_us
import time

# ---- ピンの設定 ----
trig = Pin(10, Pin.OUT)   # GP10:Trig(音を出す合図を送る → 出力)
echo = Pin(11, Pin.IN)    # GP11:Echo(返ってきた時間を受け取る → 入力)
                          # ※ Echo は分圧回路(1kΩ・2kΩ)を通してつなぐ

# ---- 関数:距離を測って cm で返す ----
def read_cm():
    # 合図の前に、いったん 0 にして落ち着かせる
    trig.value(0)
    time.sleep_us(2)

    # 10μs だけ 1 にする → センサーが超音波を出す
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Echo が 1 になっている時間(音が往復した時間)を測る
    # 30000μs(=30ミリ秒)待っても返ってこなければあきらめる
    t = time_pulse_us(echo, 1, 30000)

    # 測れなかったとき、t はマイナスの値になる
    if t < 0:
        return None        # None =「値なし」を返す

    # 時間(μs)を距離(cm)に変える
    # 音速 0.034cm/μs × 時間 ÷ 2(往復なので)≒ 時間 ÷ 58
    return t / 58

# ---- メインの繰り返し ----
while True:
    d = read_cm()          # 距離を測る

    if d is None:
        print("測定不可")
    else:
        # {:.1f} は「小数第1位まで表示する」という意味
        print("{:.1f} cm".format(d))

    time.sleep_ms(200)     # 0.2秒ごとに測る
