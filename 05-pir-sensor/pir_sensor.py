# ---- 必要な道具を読み込む ----
from machine import Pin
import time

# ---- ピンの設定 ----
# GP15 を人感センサーの入力にする
# PULL_DOWN:何もつながっていないときは 0(LOW)に固定する
pir = Pin(15, Pin.IN, Pin.PULL_DOWN)

# Pico 本体に付いているLED(GP25)を出力にする
# ※ Pico W の場合は Pin("LED", Pin.OUT) と書く
led = Pin(25, Pin.OUT)

# ---- ウォームアップ ----
# 電源を入れてすぐはセンサーが不安定なので30秒待つ
print("ウォームアップ中...")
time.sleep(30)
print("開始")

# ---- 前回の値を覚えておく変数 ----
prev = 0   # 最初は「検知なし」として始める

# ---- メインの繰り返し ----
while True:
    now = pir.value()          # 今のセンサーの値(1:検知、0:検知なし)

    # 前回と値が変わったときだけ表示する
    # (毎回表示すると Shell が文字だらけになるため)
    if now != prev:
        if now == 1:
            print("検知!")
        else:
            print("検知なし")
        led.value(now)         # 検知中は本体LEDを点ける
        prev = now             # 今の値を「前回の値」として覚える

    time.sleep_ms(100)         # 0.1秒ごとに確認
