from machine import Pin        # Pin:Pico のピンを操作するための道具
import time                    # time:待ち時間を作るための道具

led = Pin("LED", Pin.OUT)      # 本体のLEDを「出力」にする

while True:                    # ずっとくり返す(止めるときは停止ボタン)
    led.value(1)               # 点灯
    time.sleep(0.5)            # 0.5秒待つ
    led.value(0)               # 消灯
    time.sleep(0.5)            # 0.5秒待つ
