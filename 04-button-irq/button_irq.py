# ---- 必要な道具を読み込む ----
from machine import Pin
import time

# ---- ピンの設定(ポーリング版と同じ) ----
red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

# ---- フラグ(目印)の変数 ----
# ボタンが押されたら True にする。最初は「押されていない」= False
pressed = False

# ---- 割り込みで呼ばれる関数(ハンドラ) ----
# ボタンが押された瞬間に、Pico が自動でこの関数を呼んでくれる
def on_press(pin):
    global pressed     # 関数の外にある pressed を書き換えるための宣言
    pressed = True     # 「押されたよ」と目印を立てるだけ(短く書くのが大事)

# ---- 割り込みの登録 ----
# IRQ_FALLING:1 → 0 に変わった瞬間(=押した瞬間)に on_press を呼ぶ
button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

# ---- 関数:全部のLEDを消す ----
def all_off():
    for p in (red, yellow, green):
        p.value(0)

# ---- スタート時の状態 ----
all_off()
green.value(1)
print("待機中(緑)")

# ---- メインの繰り返し ----
while True:
    # ボタンを直接見に行かず、目印(pressed)を確認する
    if pressed:
        pressed = False            # 目印を下ろしておく
        print("ボタン押下")
        time.sleep_ms(3000)        # 3秒待つ

        # 緑 → 黄
        green.value(0)
        yellow.value(1)
        print("黄")
        time.sleep_ms(2000)        # 黄は2秒

        # 黄 → 赤
        yellow.value(0)
        red.value(1)
        print("赤(歩行者OK)")
        time.sleep_ms(5000)        # 赤は5秒

        # 赤 → 緑
        red.value(0)
        green.value(1)
        print("緑に復帰")

        # 黄・赤の間に押されていても、割り込みで目印が立っている
        # ここで False に戻すと「その押下は無視」
        # この行を消すと「予約」として次のサイクルが始まる
        pressed = False

    time.sleep_ms(50)              # 0.05秒ごとに目印を確認
