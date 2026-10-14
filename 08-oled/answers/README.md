# 08. 解答例と解説

> 別の書き方もOK。動けば正解!ここにあるのは1つの例だよ。自分なりに改良してみよう。

## Lv1

**表示する文字と位置を変える**

### 考え方

`oled.text("文字", x, y)` の x・y が、文字の左上の位置。"PICO TARO" は 9文字 = 72 ドットなので、(128 − 72)÷ 2 = **28** から書くとまん中になるよ。

### 解答コード

<!-- include: lv1.py -->
```python
# ---- Lv1 解答例:表示する文字と位置を変える ----
# 元の oled.py のあいさつ部分を、★ のように変えた例
from machine import Pin, I2C
import ssd1306

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)   # SDA=GP18、SCL=GP19
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.text("My name is", 0, 0)     # ★ 文字を変更
oled.text("PICO TARO", 28, 28)    # ★ x=28, y=28 で、まん中あたりに表示
oled.rect(16, 20, 96, 24, 1)      # ★ 名前を囲む枠
oled.show()
```

### ポイント

- 名前を枠で囲むと見やすいね。枠の大きさも数字を変えて調整してみよう。
- ループがないので、表示したら終わり。画面はそのまま残るよ。

## Lv2

**ボタンを押した回数を表示する**

### 考え方

1. 03 のボタン(GP5・プルアップ)をつなぐ
2. 05 の `prev` と `now` のように、「前は 1、今は 0」=**押された瞬間** だけ数える
3. 回数が変わったときだけ、画面を書きかえる

### 解答コード

<!-- include: lv2.py -->
```python
# ---- Lv2 解答例:ボタンを押した回数を表示する ----
# 03 のタクトスイッチ(GP5・プルアップ)と組み合わせる
from machine import Pin, I2C
import ssd1306
import time

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
button = Pin(5, Pin.IN, Pin.PULL_UP)   # ★ GP5:ボタン(押すと 0)

count = 0
prev = 1                                # 前回のボタンの状態(1 = 押していない)

# ★ 関数:回数を画面に表示する
def show_count():
    oled.fill(0)
    oled.text("button:", 0, 0)
    oled.text(str(count) + " times", 0, 16)
    oled.show()

show_count()
while True:
    now = button.value()
    if prev == 1 and now == 0:          # ★ 押された瞬間だけ数える
        count = count + 1
        show_count()                    # ★ 変わったときだけ画面を書きかえる
        time.sleep_ms(50)               # チャタリング対策
    prev = now
    time.sleep_ms(10)
```

### ポイント

- 表示を **関数 `show_count()`** にまとめたので、最初と押したときの2か所から呼べるよ。
- 毎回 `show()` しないので、ボタンの反応が速いんだ。

## Lv3

**超音波センサーの距離を数字とバーで表示する**

### 考え方

- 式:バーの幅 = 距離 ÷ 50 × 128
- 数値を入れる:25cm なら 25 ÷ 50 × 128
- 答え:**64 ドット**(画面の半分)

50cm より遠いと 128 をこえるので、`if` で 128 に止めているよ。

### 解答コード

<!-- include: lv3.py -->
```python
# ---- Lv3 解答例:超音波センサーの距離を数字とバーで表示する ----
# 06 の read_cm() をそのまま使う
from machine import Pin, I2C, time_pulse_us
import ssd1306
import time

i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

trig = Pin(10, Pin.OUT)   # GP10:Trig
echo = Pin(11, Pin.IN)    # GP11:Echo ※分圧回路(1kΩ・2kΩ)経由

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

MAX_CM = 50               # ★ バーがいっぱいになる距離

while True:
    d = read_cm()
    oled.fill(0)
    oled.text("distance", 0, 0)
    if d is None:
        oled.text("---", 0, 16)
    else:
        oled.text("{:.1f} cm".format(d), 0, 16)
        # ★ 距離をバーの長さ(0〜128ドット)に変える
        w = int(d / MAX_CM * 128)
        if w > 128:
            w = 128                       # 画面からはみ出さないように
        oled.rect(0, 40, 128, 16, 1)      # 外の枠
        oled.fill_rect(0, 40, w, 16, 1)   # 中身(ぬりつぶし)
    oled.show()
    time.sleep_ms(200)
```

### ポイント

- `int()` で小数を整数にしている。ドットの数は整数だからね。
- `rect`(枠)と `fill_rect`(ぬりつぶし)を重ねると、メーターみたいになるよ。
- 近いほどバーを長くしたいときは、`w = 128 - w` にしてみよう。

[← ステップ 08 に戻る](../README.md)
