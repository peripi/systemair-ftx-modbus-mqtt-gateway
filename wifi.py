import network
import time

def connect_wifi(SSID, pw)->str:
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(SSID, pw)
        i = 0
        print('Attempt connect to wifi')
        while not wlan.isconnected():
            i = i + 1
            print('.', end='')
            time.sleep(0.5)
        ip = wlan.ifconfig()[0]
        print(f'Connected to Wifi: {SSID}, IP: {ip}')
    except Exception as e:
        raise OSError(e)
    return ip
