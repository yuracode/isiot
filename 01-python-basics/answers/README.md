# 01. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**点滅の速さを変える**

### 考え方

点滅の速さは「点けている時間」と「消している時間」で決まるよ。`blink()` の中の `time.sleep_ms(200)` を小さくすれば速く、大きくすれば遅くなる。

### 解答コード

<!-- include: lv1.py -->
```python
# ---- Lv1 解答例:点滅の速さを変える ----
# 元の basics.py から変えたのは blink() の中の待ち時間だけ
from machine import Pin   # Pin:Pico のピンを操作するための道具
import time               # time:待ち時間を作るための道具

# Pico 本体に付いているLEDを出力にする(番号ではなく "LED" と名前で指定する)
led = Pin("LED", Pin.OUT)

# ---- 関数:LEDを1回だけ点滅させる ----
def blink():
    led.value(1)           # 点灯
    time.sleep_ms(50)      # ★ 200 → 50 に変更(速い点滅になる)
    led.value(0)           # 消灯
    time.sleep_ms(50)      # ★ 200 → 50 に変更

print("スタート")

# 3回点滅
for i in range(3):
    print(i + 1, "回目")
    blink()

time.sleep(1)              # 1秒待つ

# ずっと点滅
count = 0
while True:
    blink()
    count = count + 1
    if count % 10 == 0:    # 10回ごとに表示
        print(count, "回点滅しました")
```

### ポイント

- 変えたのは `blink()` の中の2か所(★の行)だけ。
- 関数にまとめてあるので、**関数の中を1回変えるだけで全部の点滅が速くなる** よ。これが関数の便利なところ!

## Lv2

**点滅回数を関数の引数にする**

### 考え方

関数の `( )` の中に名前(引数)を書くと、呼び出すときに値を渡せるよ。受け取った回数だけ `for` でくり返せばいいね。

### 解答コード

<!-- include: lv2.py -->
```python
# ---- Lv2 解答例:点滅回数を関数の引数にする ----
# blink(回数) と呼ぶと、その回数だけ点滅する関数に作り変える
from machine import Pin
import time

led = Pin("LED", Pin.OUT)     # 本体LED("LED" と名前で指定)

# ---- 関数:times 回だけ点滅させる ----
# ★ ( ) の中に times を書くと、呼び出すときに数を渡せる(これを「引数」という)
def blink(times):
    for i in range(times):     # times 回くり返す
        led.value(1)           # 点灯
        time.sleep_ms(200)
        led.value(0)           # 消灯
        time.sleep_ms(200)

# ---- 呼び出してみる ----
print("3回点滅")
blink(3)                   # ★ 3 が times に入る
time.sleep(1)

print("5回点滅")
blink(5)                   # ★ 5 が times に入る
time.sleep(1)

# 1回、2回、3回…と回数を増やしながら点滅をくり返す
n = 1
while True:
    print(n, "回点滅")
    blink(n)
    time.sleep(1)          # 区切りが分かるように1秒休む
    n = n + 1
    if n > 5:              # 5回まで行ったら1回に戻す
        n = 1
```

### ポイント

- `def blink(times):` の `times` が **引数**。`blink(3)` と呼ぶと `times` に 3 が入る。
- 元の `for i in range(3):` が関数の **中に** 入ったよ。
- `while` の中で `n` を増やして、1回、2回…と回数を変えてみた。

## Lv3

**モールス信号で SOS を出す**

### 考え方

SOS は「短い光3回・長い光3回・短い光3回」。回数だけでなく **点灯の長さも引数** にすれば、1つの関数で両方作れるよ。

### 解答コード

<!-- include: lv3.py -->
```python
# ---- Lv3 解答例:モールス信号で SOS を出す ----
# 「点滅回数」だけでなく「点灯の長さ」も引数にして、
# 短い光(・)と長い光(-)を組み合わせる
from machine import Pin
import time

led = Pin("LED", Pin.OUT)     # 本体LED("LED" と名前で指定)

# ---- 関数:on_ms ミリ秒の点灯を times 回くり返す ----
# 引数を2つにすると、回数と長さの両方を変えられる
def blink(times, on_ms):
    for i in range(times):
        led.value(1)
        time.sleep_ms(on_ms)   # 点灯している長さ
        led.value(0)
        time.sleep_ms(200)     # 光と光の間のすき間

# ---- 関数:SOS を1回出す ----
# S = ・・・(短く3回)、O = ---(長く3回)
def sos():
    blink(3, 200)          # S:短い光を3回
    blink(3, 600)          # O:長い光を3回
    blink(3, 200)          # S:短い光を3回

while True:
    print("SOS")
    sos()
    time.sleep(2)          # 2秒あけてくり返す
```

### ポイント

- 引数は **2つ以上** にもできる:`blink(times, on_ms)`。
- `sos()` という関数の中から `blink()` を呼んでいる。**関数の中から別の関数を呼ぶ** と、大きな動きを小さな部品に分けて作れるよ。
- 自分の名前のイニシャルをモールス信号にしてみるのもおもしろいよ。

[← ステップ 01 に戻る](../README.md)
