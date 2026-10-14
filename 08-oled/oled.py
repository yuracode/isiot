# ---- 必要な道具を読み込む ----
# I2C:2本の線(SDA・SCL)で部品とやりとりするしくみ
from machine import Pin, I2C
import ssd1306            # OLED(SSD1306)を動かすライブラリ(Thonny で入れておく)
import time

# ---- I2C と OLED の設定 ----
i2c = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)   # I2C1:SDA=GP18、SCL=GP19
print("見つかった部品:", i2c.scan())   # [60] と出れば OK(60 = 0x3C)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)   # 横128 × 縦64 ドットの画面

# ---- 最初のあいさつ ----
oled.fill(0)                      # 画面を全部消す(0 = 黒)
oled.text("Hello Pico!", 0, 0)    # 文字, x(横), y(縦)
oled.text("SSD1306 OLED", 0, 16)
oled.rect(0, 40, 128, 20, 1)      # 四角の枠:x, y, 幅, 高さ, 色(1 = 白)
oled.show()                       # ← show() を呼んで、はじめて画面に出る
time.sleep(2)

# ---- メインの繰り返し:数を数えて表示 ----
n = 0
while True:
    oled.fill(0)                  # 前の表示を消す
    oled.text("count:", 0, 0)
    oled.text(str(n), 0, 16)      # 数は str() で文字に変えてから表示
    oled.show()
    n = n + 1
    time.sleep_ms(500)            # 0.5秒ごとに数える
