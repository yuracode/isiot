# 06. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**測る間隔を変える**

### 考え方

最後の `time.sleep_ms(200)` が測る間隔。1秒 = **1000ミリ秒** だね。

### 解答コード

```python
# ---- Lv1 解答例:測る間隔を変える ----
# 元の ultrasonic.py から変えたのは ★ の行だけ
from machine import Pin, time_pulse_us
import time

trig = Pin(10, Pin.OUT)   # GP10:Trig(出力)
echo = Pin(11, Pin.IN)    # GP11:Echo(入力)※分圧回路(1kΩ・2kΩ)経由

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)              # 10μs だけ 1 → 超音波を出す
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)   # 往復の時間(μs)
    if t < 0:
        return None            # 測れなかった
    return t / 58              # 時間 ÷ 58 = 距離(cm)

while True:
    d = read_cm()
    if d is None:
        print("測定不可")
    else:
        print("{:.1f} cm".format(d))
    time.sleep_ms(1000)        # ★ 200 → 1000(1秒ごと)に変更
```

### ポイント

- 変えたのは ★ の1行だけ。
- 間隔を短くしすぎる(例:10ms)と、前の音の反射が残っていて、おかしな値になることがあるよ。

## Lv2

**気温を変数にして音速を計算し直す**

### 考え方

1. 音速(m/秒)= 331.5 + 0.6 × 気温
2. cm/μs に直す:× 100(m → cm)÷ 1000000(秒 → μs)
3. 距離 = 時間 × 音速 ÷ 2(往復なので)

例:25℃ なら 331.5 + 0.6 × 25 = **346.5m/秒** = 0.03465cm/μs。

### 解答コード

```python
# ---- Lv2 解答例:気温を変数にして音速を計算し直す ----
# 音速(m/秒)= 331.5 + 0.6 × 気温
# これを cm/μs に直して、距離 = 時間 × 音速 ÷ 2 で計算する
from machine import Pin, time_pulse_us
import time

TEMP = 25                 # ★ 今の気温(℃)。教室の温度計を見て変えよう

# ★ 音速を計算する
speed_m = 331.5 + 0.6 * TEMP           # m/秒  (25℃なら 346.5)
speed_cm_us = speed_m * 100 / 1000000  # cm/μs(m→cm で ×100、秒→μs で ÷100万)
print("気温", TEMP, "℃ → 音速", speed_m, "m/秒")

trig = Pin(10, Pin.OUT)   # GP10:Trig
echo = Pin(11, Pin.IN)    # GP11:Echo ※分圧回路経由

def read_cm():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    t = time_pulse_us(echo, 1, 30000)
    if t < 0:
        return None
    # ★ t / 58 のかわりに、計算した音速を使う(往復なので ÷2)
    return t * speed_cm_us / 2

while True:
    d = read_cm()
    if d is None:
        print("測定不可")
    else:
        print("{:.1f} cm".format(d))
    time.sleep_ms(200)
```

### ポイント

- 音速の計算は **ループの外で1回だけ** やっている。気温は測っている間に変わらないからね。
- `t / 58` は「15℃くらい(340m/秒)」のときの近似。気温を入れると、より正確になるよ。
- 温度センサーを使えば、気温も自動で測れるようになるよ(発展)。

## Lv3

**5回測った平均を表示して、値のブレを減らす**

### 考え方

1回ずつの値はブレることがあるので、**何回か測って平均** をとるよ。測定不可(`None`)は足せないので、うまく測れたときだけ足して、その回数で割る。

### 解答コード

```python
# ---- Lv3 解答例:5回測った平均を表示して、値のブレを減らす ----
from machine import Pin, time_pulse_us
import time

trig = Pin(10, Pin.OUT)   # GP10:Trig
echo = Pin(11, Pin.IN)    # GP11:Echo ※分圧回路経由

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

# ★ 関数:n 回測って平均を返す
def read_avg(n):
    total = 0              # 合計
    ok = 0                 # うまく測れた回数
    for i in range(n):
        d = read_cm()
        if d is not None:  # 測れたときだけ足す(None は足せない)
            total = total + d
            ok = ok + 1
        time.sleep_ms(30)  # 前の音の反射が消えるまで少し待つ
    if ok == 0:
        return None        # 1回も測れなかった
    return total / ok      # 平均 = 合計 ÷ 回数

while True:
    d = read_avg(5)        # ★ 5回の平均
    if d is None:
        print("測定不可")
    else:
        print("{:.1f} cm(5回平均)".format(d))
    time.sleep_ms(200)
```

### ポイント

- 関数 `read_avg(n)` の中で、別の関数 `read_cm()` を呼んでいるよ。
- `ok == 0`(1回も測れなかった)のときに割り算すると **0 で割るエラー** になるので、先に `None` を返している。
- 平均のかわりに「真ん中の値(中央値)」を使う方法もあるよ。とびぬけた値に強くなるんだ。

[← ステップ 06 に戻る](../README.md)
