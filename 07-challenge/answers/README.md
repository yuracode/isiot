# 07. チャレンジ課題 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## 課題1

**超音波で10cm以内に近づいたら信号機を赤にする**

### 考え方

02 の信号機のピン設定と `all_off()`、06 の `read_cm()` を1つのプログラムにまとめる。測った距離が 10cm 未満なら赤、それ以外は緑。

### 解答コード

```python
# ---- 課題1 解答例:超音波で10cm以内に近づいたら信号機を赤にする ----
# 使うステップ:02(信号機)+ 06(超音波)
from machine import Pin, time_pulse_us
import time

# 信号機
red    = Pin(2, Pin.OUT)   # GP2:赤
yellow = Pin(3, Pin.OUT)   # GP3:黄
green  = Pin(4, Pin.OUT)   # GP4:緑

# 超音波センサー
trig = Pin(10, Pin.OUT)    # GP10:Trig
echo = Pin(11, Pin.IN)     # GP11:Echo ※分圧回路(1kΩ・2kΩ)経由

def all_off():
    for p in (red, yellow, green):
        p.value(0)

# 06 の read_cm() をそのまま使う
def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    return t / 58

while True:
    d = read_cm()
    all_off()
    if d is not None and d < 10:   # 測れていて、しかも10cm未満なら
        red.value(1)               # 近い → 赤
        print("{:.1f} cm 近い!→ 赤".format(d))
    else:
        green.value(1)             # 遠い(または測定不可)→ 緑
        print("遠い → 緑")
    time.sleep_ms(200)
```

### ポイント

- `d is not None and d < 10`:`None` と数字は大きさをくらべられないので、**先に None でないことを確かめる** のが大事。`and` は左から調べて、左が False なら右は調べないよ。
- 毎回 `all_off()` してから点けたい色だけ点けているので、色が混ざらない。

## 課題2

**人感センサーが反応したら黄を点滅させる**

### 考え方

検知している間(`pir.value() == 1`)、点ける → 待つ → 消す → 待つ をくり返せば点滅になるよ。

### 解答コード

```python
# ---- 課題2 解答例:人感センサーが反応したら黄を点滅させる ----
# 使うステップ:02(信号機)+ 05(人感センサー)
from machine import Pin
import time

pir    = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー
red    = Pin(2, Pin.OUT)                  # GP2:赤
yellow = Pin(3, Pin.OUT)                  # GP3:黄
green  = Pin(4, Pin.OUT)                  # GP4:緑

def all_off():
    for p in (red, yellow, green):
        p.value(0)

all_off()
print("ウォームアップ中...")
time.sleep(30)
print("開始")

while True:
    if pir.value() == 1:       # 検知している間は
        yellow.value(1)        # 黄を点けて
        time.sleep_ms(300)
        yellow.value(0)        # 消して
        time.sleep_ms(300)     # → これをくり返すので点滅になる
    else:
        yellow.value(0)        # 検知していないときは消しておく
        time.sleep_ms(100)
```

### ポイント

- `while True` 自体がくり返しなので、1回分の点滅を書くだけで点滅が続くよ。
- 検知していないときも `sleep_ms(100)` を入れて、Pico を休ませている。

## 課題3

**ボタンを押したら超音波で距離を測り、距離に応じて信号の色を変える**

### 考え方

03 のボタンの読み方で「本当に押した」を判断したら、06 の `read_cm()` で距離を測って、`if` / `elif` / `else` で色を選ぶ。

### 解答コード

```python
# ---- 課題3 解答例:ボタンを押したら距離を測り、距離に応じて信号の色を変える ----
# 使うステップ:02(信号機)+ 03(ボタン)+ 06(超音波)
#   10cm 未満 → 赤 / 30cm 未満 → 黄 / それ以上 → 緑
from machine import Pin, time_pulse_us
import time

red    = Pin(2, Pin.OUT)               # GP2:赤
yellow = Pin(3, Pin.OUT)               # GP3:黄
green  = Pin(4, Pin.OUT)               # GP4:緑
button = Pin(5, Pin.IN, Pin.PULL_UP)   # GP5:ボタン(押すと 0)
trig   = Pin(10, Pin.OUT)              # GP10:Trig
echo   = Pin(11, Pin.IN)               # GP11:Echo ※分圧回路経由

def all_off():
    for p in (red, yellow, green):
        p.value(0)

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    return t / 58

all_off()
print("ボタンを押すと距離を測るよ")

while True:
    if button.value() == 0:
        time.sleep_ms(20)              # チャタリング対策
        if button.value() == 0:
            d = read_cm()
            all_off()
            if d is None:
                print("測定不可")      # 何も点けない
            elif d < 10:               # elif =「そうでなくて、もし〜なら」
                red.value(1)
                print("{:.1f} cm → 赤".format(d))
            elif d < 30:
                yellow.value(1)
                print("{:.1f} cm → 黄".format(d))
            else:
                green.value(1)
                print("{:.1f} cm → 緑".format(d))

            while button.value() == 0: # 離されるまで待つ
                time.sleep_ms(10)

    time.sleep_ms(10)
```

### ポイント

- `if` → `elif` → `else` は **上から順に調べて、最初に当てはまった1つだけ** 実行するよ。だから小さい距離(10cm)から順に書いている。
- 離されるまで待つ部分(03 で学んだ)がないと、押している間ずっと測り続けてしまうよ。

## 課題4(+α)

**人がいるときだけ、距離に応じて信号の色を変え続ける**

### 考え方

05 の人感センサーで「人がいるか」を調べ、いるときだけ 06 の超音波で測る。距離から色を決める部分は関数 `color_for(d)` にまとめた。

### 解答コード

```python
# ---- 課題4(+α)解答例:人がいるときだけ、距離に応じて信号の色を変え続ける ----
# 使うステップ:02(信号機)+ 05(人感センサー)+ 06(超音波)
#   人がいない → 全部消灯(省エネ)
#   人がいる   → 10cm 未満:赤 / 30cm 未満:黄 / それ以上:緑
from machine import Pin, time_pulse_us
import time

pir    = Pin(15, Pin.IN, Pin.PULL_DOWN)   # GP15:人感センサー
red    = Pin(2, Pin.OUT)                  # GP2:赤
yellow = Pin(3, Pin.OUT)                  # GP3:黄
green  = Pin(4, Pin.OUT)                  # GP4:緑
trig   = Pin(10, Pin.OUT)                 # GP10:Trig
echo   = Pin(11, Pin.IN)                  # GP11:Echo ※分圧回路経由

def all_off():
    for p in (red, yellow, green):
        p.value(0)

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    return t / 58

# ★ 関数:距離から点けるLEDを決めて返す
def color_for(d):
    if d < 10:
        return red
    elif d < 30:
        return yellow
    else:
        return green

all_off()
print("ウォームアップ中...")
time.sleep(30)
print("開始")

while True:
    all_off()
    if pir.value() == 1:               # 人がいるときだけ測る
        d = read_cm()
        if d is not None:
            color_for(d).value(1)      # 関数が返したLEDを点ける
            print("{:.1f} cm".format(d))
    time.sleep_ms(200)
```

### ポイント

- `color_for(d)` は **LED のピンそのものを return** している。返ってきたピンに `.value(1)` すれば点くよ。関数は数字だけでなく、いろいろなものを返せるんだ。
- 3種類のセンサー・部品を組み合わせても、1つ1つは今までのステップで学んだことの組み合わせだね。

[← 07 チャレンジ課題に戻る](../README.md)
