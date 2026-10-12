# 04. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**赤の秒数を変える**

### 考え方

このプログラムはミリ秒で待っているよ。8秒 = 8 × 1000 = **8000ミリ秒**。

### 解答コード

<!-- include: lv1.py -->
```python
# ---- Lv1 解答例:赤の秒数を変える ----
# 元の button_irq.py から変えたのは ★ の1行だけ
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

pressed = False                        # フラグ(目印)

def on_press(pin):
    global pressed                     # 外の pressed を書き換える宣言
    pressed = True                     # 目印を立てるだけ

button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

while True:
    if pressed:
        pressed = False
        print("ボタン押下")
        time.sleep_ms(3000)

        green.value(0)
        yellow.value(1)
        print("黄")
        time.sleep_ms(2000)

        yellow.value(0)
        red.value(1)
        print("赤(歩行者OK)")
        time.sleep_ms(8000)            # ★ 赤:5000 → 8000(8秒)に変更

        red.value(0)
        green.value(1)
        print("緑に復帰")

        pressed = False                # 途中の押下は無視

    time.sleep_ms(50)
```

### ポイント

- 変えたのは ★ の1行だけ。
- `time.sleep(8)` と書いても同じ意味だよ。

## Lv2

**赤の間に押されたら「予約しました」と表示する**

### 考え方

1. 赤の5秒を「50ms × 100回」に分けて、そのたびに `pressed` を見る。
2. 押されていたら「予約しました」と表示し、`reserved = True` にする。
3. 緑に戻ったとき、予約があれば `pressed = True` のままにして次のサイクルへ。

### 解答コード

<!-- include: lv2.py -->
```python
# ---- Lv2 解答例:赤の間に押されたら「予約しました」と表示する ----
# 考え方:
#   赤の5秒を「50ミリ秒 × 100回」に分けて、そのたびに目印(pressed)を見る
#   目印が立っていたら「予約しました」と表示して reserved を True にする
#   最後に reserved が True なら、目印を残したままにして次のサイクルへ
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

pressed = False                        # フラグ(目印)

def on_press(pin):
    global pressed
    pressed = True                     # ハンドラは短く。目印を立てるだけ

button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

while True:
    if pressed:
        pressed = False
        print("ボタン押下")
        time.sleep_ms(3000)

        green.value(0)
        yellow.value(1)
        print("黄")
        time.sleep_ms(2000)

        yellow.value(0)
        red.value(1)
        print("赤(歩行者OK)")

        # ★ 赤の5秒を細かく分けて、そのたびに目印を確認する
        reserved = False               # 予約されたかどうか
        for i in range(100):           # 50ms × 100回 = 5000ms = 5秒
            if pressed and not reserved:
                print("予約しました")
                reserved = True
            time.sleep_ms(50)

        red.value(0)
        green.value(1)
        print("緑に復帰")

        if reserved:
            pressed = True             # ★ 予約あり → 目印を立てて次のサイクルへ
        else:
            pressed = False            # 予約なし → 黄の間の押下などは無視

    time.sleep_ms(50)
```

### ポイント

- ハンドラの中で `print` せず、**メインの処理で表示** しているよ(ハンドラは短く!)。
- `if pressed and not reserved:` の `not reserved` で、何回押しても「予約しました」は1回だけ表示される。
- 黄の間に押されたぶんは、最後に `pressed = False` で無視している。黄の間も予約にしたければ、どう変えればいいかな?

## Lv3

**前回の押下から200ms以内は無視する**

### 考え方

押されるたびに時刻を記録して、前回との差が 200ms より短ければ「チャタリング」とみなして無視するよ。

### 解答コード

<!-- include: lv3.py -->
```python
# ---- Lv3 解答例:前回の押下から200ms以内は無視する(チャタリング対策) ----
# 考え方:
#   time.ticks_ms() は「Pico が動き始めてからのミリ秒」を返す
#   押されるたびに時刻を記録し、前回との差が200ms未満なら
#   チャタリング(接点のバタつき)とみなして無視する
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0 になる

pressed = False                        # フラグ(目印)
last_ms = 0                            # ★ 前回、押下を受け付けた時刻(ミリ秒)

def on_press(pin):
    global pressed, last_ms            # ★ 外の変数を2つ書き換える
    now = time.ticks_ms()              # ★ 今の時刻
    # ticks_diff(新, 古) で「何ミリ秒たったか」を正しく計算できる
    if time.ticks_diff(now, last_ms) < 200:
        return                         # ★ 200ms以内 → チャタリングなので無視
    last_ms = now                      # 受け付けた時刻を覚えておく
    pressed = True                     # 目印を立てる

button.irq(trigger=Pin.IRQ_FALLING, handler=on_press)

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

while True:
    if pressed:
        pressed = False
        print("ボタン押下")
        time.sleep_ms(3000)

        green.value(0)
        yellow.value(1)
        print("黄")
        time.sleep_ms(2000)

        yellow.value(0)
        red.value(1)
        print("赤(歩行者OK)")
        time.sleep_ms(5000)

        red.value(0)
        green.value(1)
        print("緑に復帰")

        pressed = False

    time.sleep_ms(50)
```

### ポイント

- `global pressed, last_ms` のように、`global` はカンマで複数書ける。
- 時間の差は `now - last_ms` ではなく `time.ticks_diff(now, last_ms)` を使おう。`ticks_ms()` の値はとても大きくなると 0 に戻るので、`ticks_diff` が正しく計算してくれるんだ。
- `return` でハンドラを途中で終わらせて、フラグを立てないようにしている。

[← ステップ 04 に戻る](../README.md)
