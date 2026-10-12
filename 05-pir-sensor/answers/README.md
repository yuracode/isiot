# 05. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**ウォームアップ時間を変える**

### 考え方

`time.sleep(30)` を変えれば OK。残り秒数を出すなら、1秒ずつ待つのを `for` でくり返そう。

### 解答コード

<!-- include: lv1.py -->
```python
# ---- Lv1 解答例:ウォームアップ時間を変える ----
# 元の pir_sensor.py から変えたのは ★ の行だけ
from machine import Pin
import time

pir = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー(何もないとき 0)
led = Pin("LED", Pin.OUT)                 # 本体LED("LED" と名前で指定)

WARMUP_SEC = 10                        # ★ ウォームアップの秒数(30 → 10)

print("ウォームアップ中...")
# ★ 残り秒数を1秒ごとに表示すると、待っている感じが分かりやすい
for i in range(WARMUP_SEC, 0, -1):     # 10, 9, 8, ... 1 と数を減らす
    print("あと", i, "秒")
    time.sleep(1)
print("開始")

prev = 0
while True:
    now = pir.value()
    if now != prev:                    # 変化したときだけ
        if now == 1:
            print("検知!")
        else:
            print("検知なし")
        led.value(now)
        prev = now
    time.sleep_ms(100)
```

### ポイント

- 秒数を `WARMUP_SEC` という変数にしたので、1か所変えるだけでいい。
- `range(10, 0, -1)` は「10 から始めて、0 の手前まで、1 ずつ減らす」→ 10, 9, …, 1。
- 時間を短くしすぎると、最初のうち誤検知することがあるよ。ためしてみよう。

## Lv2

**検知した回数を数える**

### 考え方

「検知している間ずっと」数えると、0.1秒ごとに増えてしまう。**0 → 1 に変わった瞬間だけ** 数えればいいね。

### 解答コード

<!-- include: lv2.py -->
```python
# ---- Lv2 解答例:検知した回数を数える ----
from machine import Pin
import time

pir = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー
led = Pin("LED", Pin.OUT)                 # 本体LED

print("ウォームアップ中...")
time.sleep(30)
print("開始")

prev = 0
count = 0                              # ★ 検知した回数(最初は0)

while True:
    now = pir.value()
    if now != prev:
        if now == 1:
            # ★ 0 → 1 に変わったときだけ数える
            #   (1 のあいだずっと数えると、1回の検知で何百回にもなってしまう)
            count = count + 1
            print("検知!", count, "回目")
        else:
            print("検知なし")
        led.value(now)
        prev = now
    time.sleep_ms(100)
```

### ポイント

- `if now != prev:` の中の `if now == 1:` が、ちょうど「0 → 1 に変わった瞬間」になるよ。
- 「変化したときだけ」の考え方は、ボタンの押下回数を数えるときにも使えるよ。

## Lv3

**検知したら信号機を赤にする**

### 考え方

05 のプログラムに、02 の信号機のピン設定と `all_off()` を足して、「LED を点ける」かわりに「信号の色を変える」ようにするよ。

### 解答コード

<!-- include: lv3.py -->
```python
# ---- Lv3 解答例:検知したら信号機を赤にする(02 と組み合わせ) ----
# 人がいる → 赤、人がいない → 緑
from machine import Pin
import time

# 人感センサー(05 のステップ)
pir = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15

# ★ 信号機(02 のステップ)
red    = Pin(2, Pin.OUT)               # GP2:赤
yellow = Pin(3, Pin.OUT)               # GP3:黄
green  = Pin(4, Pin.OUT)               # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

print("ウォームアップ中...")
all_off()
yellow.value(1)                        # ★ ウォームアップ中は黄で知らせる
time.sleep(30)
print("開始")

all_off()
green.value(1)                         # 最初は「人なし」= 緑
prev = 0

while True:
    now = pir.value()
    if now != prev:
        all_off()
        if now == 1:
            print("検知! → 赤")
            red.value(1)               # ★ 人がいる → 赤
        else:
            print("検知なし → 緑")
            green.value(1)             # ★ 人がいない → 緑
        prev = now
    time.sleep_ms(100)
```

### ポイント

- 2つのステップのプログラムを **組み合わせる** ときは、ピン設定と関数をコピーしてくるのが基本。
- ウォームアップ中は黄を点けて、「準備中」と分かるようにした。
- 変化したときに `all_off()` してから、点けたい色だけ点けているよ。

[← ステップ 05 に戻る](../README.md)
