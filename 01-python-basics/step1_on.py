from machine import Pin        # Pin:Pico のピンを操作するための道具

led = Pin("LED", Pin.OUT)      # 本体のLEDを「出力」にする
led.value(1)                   # 1 = 点灯
