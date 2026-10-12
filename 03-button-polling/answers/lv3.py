# ---- Lv3 解答例:長押し(1秒以上)で全色点滅モード ----
# 考え方:押されたら「離されるまで何ミリ秒押されていたか」を数える
#   1000ミリ秒以上 → 長押し → 全色点滅モード
#   それより短い   → ふつうの押しボタン信号
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0

def all_off():
    for p in (red, yellow, green):
        p.value(0)

# ★ 関数:全色をそろって点滅させる。もう一度ボタンを押すと終わる
def blink_mode():
    print("全色点滅モード(ボタンで終了)")
    while True:
        for v in (1, 0):               # 1(点灯)→ 0(消灯)の順に
            for p in (red, yellow, green):
                p.value(v)
            # 0.3秒待つあいだも、10ミリ秒ごとにボタンを見る
            for i in range(30):
                if button.value() == 0:
                    all_off()
                    while button.value() == 0:   # 離されるまで待つ
                        time.sleep_ms(10)
                    return                       # 関数を終わって元に戻る
                time.sleep_ms(10)

# ★ 関数:ふつうの押しボタン信号のサイクル
def normal_cycle():
    print("ボタン押下")
    time.sleep(3)
    green.value(0)
    yellow.value(1)
    print("黄")
    time.sleep(2)
    yellow.value(0)
    red.value(1)
    print("赤(歩行者OK)")
    time.sleep(5)
    red.value(0)

all_off()
green.value(1)
print("待機中(緑)")

while True:
    if button.value() == 0:
        time.sleep_ms(20)              # チャタリング対策
        if button.value() == 0:
            # ★ 押されている時間を数える
            held = 0                   # 押している時間(ミリ秒)
            while button.value() == 0:
                time.sleep_ms(10)
                held = held + 10       # 10ミリ秒ずつ足していく

            if held >= 1000:           # ★ 1秒以上なら長押し
                all_off()
                blink_mode()
            else:                      # 短い押しなら今まで通り
                normal_cycle()

            all_off()
            green.value(1)
            print("緑に復帰")

    time.sleep_ms(10)
