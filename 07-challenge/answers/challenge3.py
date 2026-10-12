# ---- 課題3 解答例:ボタンを押したら距離を測り、距離に応じて信号の色を変える ----
# 使うステップ:02(信号機)+ 03(ボタン)+ 06(超音波)
#   10cm 未満 → 赤 / 30cm 未満 → 黄 / それ以上 → 緑
from machine import Pin, time_pulse_us
import time

red    = Pin(2, Pin.OUT)               # GP2:赤
yellow = Pin(3, Pin.OUT)               # GP3:黄
green  = Pin(4, Pin.OUT)               # GP4:緑
button = Pin(5, Pin.IN, Pin.PULL_UP)   # GP5:ボタン(押すと 0)
trig   = Pin(10, Pin.OUT)              # GP10:Trig
echo   = Pin(11, Pin.IN)               # GP11:Echo ※分圧回路経由

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

all_off()
print("ボタンを押すと距離を測るよ")

while True:
    if button.value() == 0:
        time.sleep_ms(20)              # チャタリング対策
        if button.value() == 0:
            d = read_cm()
            all_off()
            if d is None:
                print("測定不可")      # 何も点けない
            elif d < 10:               # elif =「そうでなくて、もし〜なら」
                red.value(1)
                print("{:.1f} cm → 赤".format(d))
            elif d < 30:
                yellow.value(1)
                print("{:.1f} cm → 黄".format(d))
            else:
                green.value(1)
                print("{:.1f} cm → 緑".format(d))

            while button.value() == 0: # 離されるまで待つ
                time.sleep_ms(10)

    time.sleep_ms(10)
