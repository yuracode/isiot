# ---- 必要な道具(モジュール)を読み込む ----
from machine import Pin   # Pin:Pico のピンを操作するための道具
import time               # time:待ち時間を作るための道具

# ---- ピンの設定 ----
# Pico 本体に付いているLEDを出力にする(番号ではなく "LED" と名前で指定する)
led = Pin("LED", Pin.OUT)

# ---- 関数:LEDを1回だけ点滅させる ----
# def で「よく使う処理」に名前を付けておく
def blink():
    led.value(1)           # 1 = 電気を流す = 点灯
    time.sleep_ms(200)     # 200ミリ秒(0.2秒)待つ
    led.value(0)           # 0 = 電気を止める = 消灯
    time.sleep_ms(200)     # 200ミリ秒待つ

# ---- 順次:上から順に1行ずつ実行される ----
print("スタート")

# ---- for:決まった回数だけ繰り返す ----
# range(3) は 0, 1, 2 の3つ。i に順番に入る
for i in range(3):
    print(i + 1, "回目")   # 1回目、2回目、3回目 と表示
    blink()                # 関数を呼び出して1回点滅

time.sleep(1)              # 1秒待つ(この間、Pico は他のことができない)

# ---- while True:ずっと繰り返す(無限ループ) ----
# 止めるときは Thonny の停止ボタンを押す
count = 0                  # 何回点滅したかを数える変数
while True:
    blink()
    count = count + 1      # 1 増やす

    # ---- if:条件によって処理を分ける ----
    # 10回ごとに Shell に表示する
    if count % 10 == 0:    # % は「割った余り」。10で割り切れたら
        print(count, "回点滅しました")
