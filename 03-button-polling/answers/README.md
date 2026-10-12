# 03. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**押してから黄になるまでの時間を変える**

### 考え方

「本当に押した」と判断したあとの `time.sleep(3)` が、黄になるまでの待ち時間だよ。

### 解答コード

<!-- include: lv1.py -->
```python
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
```

### ポイント

- 変えたのは ★ の1行だけ。
- 本物の押しボタン信号も、押してすぐではなく少し待ってから変わるよね。車が急に止まらなくてすむようにしているんだ。

## Lv2

**ボタンを押した回数を数えて Shell に表示する**

### 考え方

数を数えるには、**ループの外** で変数を 0 にしておき、押されるたびに 1 足すよ。

### 解答コード

<!-- include: lv2.py -->
```python
# ---- Lv2 解答例:ボタンを押した回数を数えて Shell に表示する ----
from machine import Pin
import time

red    = Pin(2, Pin.OUT)
yellow = Pin(3, Pin.OUT)
green  = Pin(4, Pin.OUT)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # 押すと 0

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
green.value(1)
print("待機中(緑)")

count = 0                              # ★ 押した回数を数える変数(最初は0)

while True:
    if button.value() == 0:
        time.sleep_ms(20)              # チャタリング対策
        if button.value() == 0:
            count = count + 1          # ★ 1 増やす
            print("ボタン押下", count, "回目")   # ★ 回数も表示
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
            green.value(1)
            print("緑に復帰")

            while button.value() == 0:
                time.sleep_ms(10)

    time.sleep_ms(10)
```

### ポイント

- `count = 0` を `while True:` の **中** に書くと、毎回 0 に戻ってしまうよ。だから **外** に書く。
- チャタリング対策の **あと** で数えているので、1回押して2回以上数えることはないよ。

## Lv3

**長押し(1秒以上)で全色点滅モード**

### 考え方

1. 押されたら、離されるまでの時間を 10ms ずつ足して測る。
2. 1000ms 以上なら長押し → 点滅モード。短ければ今まで通り。
3. 点滅モードの中でもボタンを見て、押されたら終わる。

### 解答コード

<!-- include: lv3.py -->
```python
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
```

### ポイント

- 処理を `blink_mode()` と `normal_cycle()` の **関数に分けた** ので、メインの `while` が読みやすくなったね。
- 点滅モードの「0.3秒待つ」を **10ms × 30回** に分けて、その間もボタンを見ているよ。こうすると `sleep` 中でもボタンに気づける(ポーリングの工夫)。
- `return` で関数を途中で終わらせて、元の場所に戻っているよ。

[← ステップ 03 に戻る](../README.md)
