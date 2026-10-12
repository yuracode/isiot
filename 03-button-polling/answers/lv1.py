# ---- Lv1 解答例:押してから黄になるまでの時間を変える ----
# 元の button_polling.py から変えたのは ★ の1行だけ
from machine import Pin
import time

red    = Pin(2, Pin.OUT)   # GP2:赤(出力)
yellow = Pin(3, Pin.OUT)   # GP3:黄(出力)
green  = Pin(4, Pin.OUT)   # GP4:緑(出力)

# GP5 をボタン用の入力にする(押すと 0)
button = Pin(5, Pin.IN, Pin.PULL_UP)

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

while True:
    if button.value() == 0:
        time.sleep_ms(20)              # チャタリング対策
        if button.value() == 0:
            print("ボタン押下")
            time.sleep(1)              # ★ 3秒 → 1秒 に変更(すぐ黄になる)

            green.value(0)
            yellow.value(1)
            print("黄")
            time.sleep(2)

            yellow.value(0)
            red.value(1)
            print("赤(歩行者OK)")
            time.sleep(5)

            red.value(0)
            green.value(1)
            print("緑に復帰")

            while button.value() == 0: # 離されるまで待つ
                time.sleep_ms(10)

    time.sleep_ms(10)                  # ポーリング
