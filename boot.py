# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import uos, machine
uos.dupterm(None, 1) # disable REPL on UART(0)


import gc

import network
import time
ssid=***REMOVED***
password=***REMOVED***
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid,password)
i=0

print('attempt connect to wifi')
while not wlan.isconnected():
    i=i+1
    print('.', end='')
    time.sleep(0.5)

print('connect Wifi True!')
print(wlan.ifconfig())

import webrepl
webrepl.start()
