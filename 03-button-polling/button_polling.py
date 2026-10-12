# ---- 必要な道具を読み込む ----
from machine import Pin
import time

# ---- ピンの設定 ----
red    = Pin(2, Pin.OUT)   # GP2:赤(出力)
yellow = Pin(3, Pin.OUT)   # GP3:黄(出力)
green  = Pin(4, Pin.OUT)   # GP4:緑(出力)

# GP5 をボタン用の「入力(IN)」にする
# PULL_UP:内部のプルアップ抵抗を使う
#   押していない → 1(HIGH)
#   押している   → 0(LOW) ← 押すと 0 になる点に注意!
button = Pin(5, Pin.IN, Pin.PULL_UP)

# ---- 関数:全部のLEDを消す ----
def all_off():
    for p in (red, yellow, green):
        p.value(0)

# ---- スタート時の状態 ----
all_off()
green.value(1)             # 車用の信号は緑で待つ
print("待機中(緑)")

# ---- メインの繰り返し ----
while True:
    # ボタンの状態を読む。0 なら押されている
    if button.value() == 0:
        time.sleep_ms(20)              # 20ミリ秒待つ(チャタリング対策)
        if button.value() == 0:        # 20ミリ秒後もまだ押されていたら「本当に押した」と判断
            print("ボタン押下")
            time.sleep(3)              # 押してからすぐには変わらず、3秒待つ

            # 緑 → 黄
            green.value(0)
            yellow.value(1)
            print("黄")
            time.sleep(2)              # 黄は2秒

            # 黄 → 赤
            yellow.value(0)
            red.value(1)
            print("赤(歩行者OK)")
            time.sleep(5)              # 赤は5秒(この間に歩行者がわたる)

            # 赤 → 緑(元に戻る)
            red.value(0)
            green.value(1)
            print("緑に復帰")

            # ボタンが押しっぱなしなら、離されるまでここで待つ
            # (待たないと、すぐに次のサイクルが始まってしまう)
            while button.value() == 0:
                time.sleep_ms(10)

    # 10ミリ秒ごとにボタンを見に行く(これがポーリング)
    time.sleep_ms(10)
