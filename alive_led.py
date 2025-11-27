from machine import Pin
from time import ticks_ms

class AliveLed():
    def __init__(self, io:int, period_ms: int = 1000, time_on_ms = 50):
        self.period = period_ms
        self.time_on = time_on_ms
        self.led = Pin(io, Pin.OUT)
        self.status = False
        self.ts = ticks_ms()

    def update(self):
        now = ticks_ms()
        if not self.status:
            if now - self.ts < self.period-self.time_on:
                return
        elif self.status:
            if now - self.ts < self.time_on:
                return
        self.status = not self.status
        self.led.value(self.status)
        self.ts = now

