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
