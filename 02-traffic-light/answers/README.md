# 02. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**各色の秒数を変える**

### 考え方

色が点いている時間は、点けたあとの `time.sleep()` で決まるよ。その数字を変えればいいね。

### 解答コード

```python
# ---- Lv1 解答例:各色の秒数を変える ----
# 元の traffic_light.py から変えたのは time.sleep() の数字だけ(★の行)
from machine import Pin   # Pin:Pico のピンを操作するための道具
import time               # time:待ち時間を作るための道具

red    = Pin(2, Pin.OUT)   # GP2 に赤のLED
yellow = Pin(3, Pin.OUT)   # GP3 に黄のLED
green  = Pin(4, Pin.OUT)   # GP4 に緑のLED

def all_off():
    for p in (red, yellow, green):
        p.value(0)         # 消灯

# 配線チェック:1個ずつ点灯
for name, p in (("赤", red), ("黄", yellow), ("緑", green)):
    all_off()
    print(name, "点灯")
    p.value(1)
    time.sleep(1)
all_off()

# 信号のサイクル
while True:
    green.value(1)
    time.sleep(3)          # ★ 緑:5秒 → 3秒
    green.value(0)

    yellow.value(1)
    time.sleep(1)          # ★ 黄:2秒 → 1秒
    yellow.value(0)

    red.value(1)
    time.sleep(3)          # ★ 赤:5秒 → 3秒
    red.value(0)
```

### ポイント

- 変えたのは `while True:` の中の `time.sleep()` の3か所(★の行)。
- 本物の信号機は、交差点の交通量に合わせて秒数を変えているよ。

## Lv2

**赤の前に黄を3回点滅させる**

### 考え方

「点ける → 待つ → 消す → 待つ」を **3回くり返せば点滅** になるね。決まった回数のくり返しは `for` の出番だよ。

### 解答コード

```python
# ---- Lv2 解答例:赤の前に黄を3回点滅させる ----
# 黄の部分を「for で3回くり返す点滅」に作り変える
from machine import Pin
import time

red    = Pin(2, Pin.OUT)   # GP2:赤
yellow = Pin(3, Pin.OUT)   # GP3:黄
green  = Pin(4, Pin.OUT)   # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

# 配線チェック:1個ずつ点灯
for name, p in (("赤", red), ("黄", yellow), ("緑", green)):
    all_off()
    print(name, "点灯")
    p.value(1)
    time.sleep(1)
all_off()

while True:
    green.value(1)
    time.sleep(5)
    green.value(0)

    # ★ ここが変わった:黄を3回点滅
    for i in range(3):         # 3回くり返す
        yellow.value(1)        # 点ける
        time.sleep_ms(300)     # 0.3秒
        yellow.value(0)        # 消す
        time.sleep_ms(300)     # 0.3秒

    red.value(1)
    time.sleep(5)
    red.value(0)
```

### ポイント

- 元の「黄を2秒点ける」3行を、`for i in range(3):` のくり返しに置きかえた。
- 消したあとにも `sleep` を入れないと、すぐ次に点いてしまって点滅に見えないよ。

## Lv3

**秒数を変数にまとめる**

### 考え方

秒数がプログラムのあちこちに書いてあると、変えるときに探すのが大変。最初に **変数** としてまとめておけば、そこだけ変えれば OK になるよ。

### 解答コード

```python
# ---- Lv3 解答例:秒数を変数にまとめる ----
# 秒数をプログラムの最初にまとめて書いておくと、
# 「ここだけ変えれば全体が変わる」ので直すのが楽になる
from machine import Pin
import time

# ★ 秒数の設定(ここを変えるだけでOK)
GREEN_SEC  = 5             # 緑の秒数
YELLOW_SEC = 2             # 黄の秒数
RED_SEC    = 5             # 赤の秒数
CHECK_SEC  = 1             # 配線チェックで1色を点ける秒数

red    = Pin(2, Pin.OUT)   # GP2:赤
yellow = Pin(3, Pin.OUT)   # GP3:黄
green  = Pin(4, Pin.OUT)   # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

# ★ 関数:ピン p を sec 秒だけ点けて消す
#   同じ「点ける→待つ→消す」を3回書いていたのを1つにまとめた
def light(p, sec):
    p.value(1)
    time.sleep(sec)
    p.value(0)

# 配線チェック
for name, p in (("赤", red), ("黄", yellow), ("緑", green)):
    all_off()
    print(name, "点灯")
    light(p, CHECK_SEC)
all_off()

# 信号のサイクル:変数を使って秒数を決める
while True:
    light(green, GREEN_SEC)
    light(yellow, YELLOW_SEC)
    light(red, RED_SEC)
```

### ポイント

- `GREEN_SEC` のように **大文字の名前** は「あとで変えない設定値(定数)」という目印としてよく使われるよ。
- 「点ける → 待つ → 消す」を関数 `light(p, sec)` にまとめたので、`while` の中が3行になった。
- 配線チェックも `light()` を使えるので、同じ処理を何度も書かなくてすむね。

[← ステップ 02 に戻る](../README.md)
