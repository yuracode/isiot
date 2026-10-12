# ---- 必要な道具(モジュール)を読み込む ----
from machine import Pin   # Pin:Pico のピンを操作するための道具
import time               # time:待ち時間を作るための道具

# ---- ピンの設定 ----
# Pin(番号, Pin.OUT) で「このピンは電気を出す(出力)」と決める
red    = Pin(2, Pin.OUT)   # GP2 に赤のLED
yellow = Pin(3, Pin.OUT)   # GP3 に黄のLED
green  = Pin(4, Pin.OUT)   # GP4 に緑のLED

# ---- 関数:全部のLEDを消す ----
def all_off():
    # 赤・黄・緑を1つずつ取り出して p に入れ、順番に消す
    for p in (red, yellow, green):
        p.value(0)         # 0 = 電気を止める = 消灯

# ---- 配線チェック:1個ずつ点灯 ----
# (名前, ピン) の組を順番に取り出して処理する
for name, p in (("赤", red), ("黄", yellow), ("緑", green)):
    all_off()              # いったん全部消す
    print(name, "点灯")    # Shell に今どの色かを表示
    p.value(1)             # 1 = 電気を流す = 点灯
    time.sleep(1)          # 1秒待つ
all_off()                  # チェックが終わったら全部消す

# ---- 信号のサイクル(ずっと繰り返す) ----
while True:                # True なので終わらない(無限ループ)
    green.value(1)         # 緑を点ける
    time.sleep(5)          # 5秒待つ
    green.value(0)         # 緑を消す

    yellow.value(1)        # 黄を点ける
    time.sleep(2)          # 2秒待つ
    yellow.value(0)        # 黄を消す

    red.value(1)           # 赤を点ける
    time.sleep(5)          # 5秒待つ
    red.value(0)           # 赤を消す → また緑に戻る
