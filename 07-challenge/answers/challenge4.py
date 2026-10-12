# ---- 課題4(+α)解答例:人がいるときだけ、距離に応じて信号の色を変え続ける ----
# 使うステップ:02(信号機)+ 05(人感センサー)+ 06(超音波)
#   人がいない → 全部消灯(省エネ)
#   人がいる   → 10cm 未満:赤 / 30cm 未満:黄 / それ以上:緑
from machine import Pin, time_pulse_us
import time

pir    = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー
red    = Pin(2, Pin.OUT)                  # GP2:赤
yellow = Pin(3, Pin.OUT)                  # GP3:黄
green  = Pin(4, Pin.OUT)                  # GP4:緑
trig   = Pin(10, Pin.OUT)                 # GP10:Trig
echo   = Pin(11, Pin.IN)                  # GP11:Echo ※分圧回路経由

def all_off():
    for p in (red, yellow, green):
        p.value(0)

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

# ★ 関数:距離から点けるLEDを決めて返す
def color_for(d):
    if d < 10:
        return red
    elif d < 30:
        return yellow
    else:
        return green

all_off()
print("ウォームアップ中...")
time.sleep(30)
print("開始")

while True:
    all_off()
    if pir.value() == 1:               # 人がいるときだけ測る
        d = read_cm()
        if d is not None:
            color_for(d).value(1)      # 関数が返したLEDを点ける
            print("{:.1f} cm".format(d))
    time.sleep_ms(200)
