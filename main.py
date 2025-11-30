import int_to_binary
from sysair_registers import registers as system_air_registers

import secrets
from int_to_binary import int_to_binary
from machine import unique_id, WDT
from time import time, sleep

from ubinascii import hexlify
from umqtt.simple import MQTTClient

mqtt_server = '10.9.8.143'

publish_reg_info = True
test_values = False                 # will omit modbus-read and use test-values prepared from system air registers
modbus_update_interval_secs = 10           # interval between mqtt data update
mqtt_min_update_interval = 3600    # if value is not updated force an update anyway
enable_wdt = True
wd_timeout = 60  # watch dog timeout

sysair_mb_addr = 1
# Modbus settings
baudrate = 9600
data_bits = 8
parity = None
stop_bits = 1
rtu_pins = (17, 16)
ctrl_pin = 19

enable_alive_led = True
led_pin = 2

ssid = 'HEMMA'
pw = 'perraperra'
import wifi
ip = wifi.connect_wifi(ssid, pw)

enable_web_repl = True

if enable_web_repl:
    import webrepl
    webrepl.start(password='eN3CrUcKEQcy2n')

from timer import Timer
timer = Timer()

if enable_alive_led:
    from alive_led import AliveLed
    alive_led = AliveLed(led_pin, 2500, 40)

# ESP 32, Wemos D1 mini
# GPI17 UART TX to C25B DI - driver input
# GPI16 UART RX to C25B RO - receiver output
# GPIO19 ctrl pin

# C25B, TTL to RS485. Note that A/B-markings on the C25B are not correct/confusing.
# Normal RS485 A(-) should be connected to C25B pin B
# Normal RS485 B(+) should be connected to C25B pin A

# Watchdog - 60 seconds, need to be larger then loop time below. Works only on ESP32
# Don't forget to enable wdt.feed() below
if enable_wdt:
    wdt = WDT(timeout=wd_timeout * 1000)

# Source for modbus driver:
# https://github.com/brainelectronics/micropython-modbus/
from umodbus.serial import Serial as ModbusRTUMaster
# modbus = ModbusRTUMaster(uart_id=2, baudrate=9600, data_bits=8, parity=None, stop_bits=1, pins=rtu_pins, ctrl_pin=ctrl_pin)
modbus = ModbusRTUMaster(baudrate=baudrate, data_bits=data_bits, parity=parity, stop_bits=stop_bits, pins=rtu_pins, ctrl_pin=ctrl_pin)

class SysAir400DC:
    def __init__(self, topic = None, slave_addr:int = 1, test_values=False):
        if topic is None:
            self.base_topic = 'system_air_VR400DC_ftx'
        else:
            self.base_topic = topic
        self.test_values = test_values
        self.slave_addr = slave_addr
        self.registers = system_air_registers()
        self.mqtt = self.create_connect_mqtt()
        self.mqtt.set_callback(self.mqtt_callback)
        self.subscribe_to_mqtt()
        self.last_update = None

    def present_sys_info(self):
        self.publish_to_mqtt('ip',value=ip)
        time_alive = timer.elapsed_time()
        self.publish_to_mqtt('time_alive', value=f'{time_alive[0]}d, {time_alive[1]}h, {time_alive[2]}m, {time_alive[3]}s')

    def create_connect_mqtt(self)->MQTTClient:
        mqtt_client = MQTTClient(server=mqtt_server, client_id=hexlify(unique_id()), user="", password="")
        mqtt_client.connect()
        # print(f'Mqtt client: {mqtt_client.client_id}, to server: {mqtt_client.server} created')
        return mqtt_client

    def mqtt_callback(self, topic, msg):
        topic = topic.decode()
        msg = msg.decode()
        sysair_topic = topic.split('/')[1]
        if sysair_topic == 'send_all':
            self.present_sensors(send_all=True)
            return
        register = self.registers.get(sysair_topic)
        mb_addr = register.get('mb_addr')
        scaling = register.get('scaling')
        try:
            self.write_register(mb_addr, scaling, msg)
        except Exception as e:
            print(f'{e}')
            self.publish_to_mqtt(sysair_topic + '/last_error', value=e)
            self.mqtt_count_modbus_error(sysair_topic, str(e))
        # set next mqtt update in one second
        sec_to_next_update = 1
        self.last_update = time() - (modbus_update_interval_secs - sec_to_next_update)

    def mqtt_count_modbus_error(self, sysair_topic, error:str):
        register = self.registers[sysair_topic]
        register['last_error'] = error
        try:
            error_cnt = register['error_cnt'] + 1
        except:
            error_cnt = 1
        self.registers[sysair_topic] = register
        self.publish_to_mqtt(sysair_topic + '/error_cnt', error_cnt)

    def subscribe_to_mqtt(self):
        # mark subscription topics with '/set'
        for sysair_topic, register in self.registers.items():
            if register.get('read_write') != 'rw':
                continue
            mqtt_topic = (self.base_topic + '/' + sysair_topic).lower() + '/set'
            self.mqtt.subscribe(mqtt_topic)
        self.mqtt.subscribe(self.base_topic.lower() + '/send_all')

    def present_sensors(self, send_all = False):
        """
        if topic=None all topics will be presented
        :param topic:
        :return:
        """
        self.last_update = time()
        for sysair_topic, register in self.registers.items():
            if not register.get('include'):
                continue
            mb_addr = register.get('mb_addr')
            scaling = register.get('scaling')
            access = register.get('read_write')
            register_details = register.get('binary_coded')
            last_update = register.get('last_update')
            last_value = register.get('last_value')
            if not self.test_values:
                try:
                    sensor_value = self.read_holding_registers(mb_addr, scaling)
                except Exception as e:
                    print(e)
                    self.publish_to_mqtt(sysair_topic + '/last_error', value=e)
                    self.mqtt_count_modbus_error(sysair_topic, str(e))
                    continue
            else:
                sensor_value = register.get('test_value')
            now = time()
            if (send_all is False and
                    last_value is not None and
                    last_value == sensor_value and
                    now - last_update < mqtt_min_update_interval):
                continue  # dont bother to update mqtt
            register['last_update'] = now
            register['last_value'] = sensor_value
            self.registers[sysair_topic] = register
            last_error = register.get('last_error')
            if last_error is not None:
                self.publish_to_mqtt(sysair_topic + '/last_error', last_error)
                self.publish_to_mqtt(sysair_topic + '/error_cnt', register.get('error_cnt'))
            if publish_reg_info:
                self.publish_to_mqtt(sysair_topic + '/reg_info', f'addr= {mb_addr}, div= {scaling}, access: {access}')

            if register_details.get('type') == 'BOOLEAN':
                self.publish_to_mqtt(sysair_topic + '/value', sensor_value == 1)
            else:
                self.publish_to_mqtt(sysair_topic + '/value', sensor_value)

            if register_details.get('type') == 'SINGLE':
                self.publish_to_mqtt(sysair_topic + '/status',
                                     str(register_details.get('coding').get(sensor_value)).replace(' ', '_'))
                for i, status_item in register_details.get('coding').items():
                    self.publish_to_mqtt(f'{sysair_topic}/binary/{status_item.replace(" ", "_")}', i == sensor_value)

            elif register_details.get('type') == 'BINARY':
                b = int_to_binary(sensor_value)
                for i, status_item in register_details.get('coding').items():
                    bit_value = len(b) > i and b[i] == 1
                    self.publish_to_mqtt(f'{sysair_topic}/binary/{status_item.replace(" ", "_").replace("/","-")}', bit_value)

    def publish_to_mqtt(self, sensor_topic, value):
        mqtt_topic = (self.base_topic + '/' + sensor_topic).lower()
        msg = str(value).lower()
        self.mqtt.publish(str(mqtt_topic), msg)

    def read_holding_registers(self, mb_addr, scaling)-> int | float:
        """
        :param mb_addr:
        :param scaling:
        :return: tuple(read ok, value)
        """
        try:
            recv_value = modbus.read_holding_registers(self.slave_addr, mb_addr-1, 1, False)[0]
        except Exception as e:
            raise OSError(f'{e}, during modbus read addr: {mb_addr}')
        if scaling == 1:
            return recv_value
        else:
            return recv_value / scaling

    def write_register(self, mb_addr, scaling, value):
        try:
            if scaling != 1:
                value = int(value * scaling)
            else:
                value = int(value)
        except Exception as e:
            raise ValueError(f'{e}, mb_addr: {mb_addr}, value: {value}')
        try:
            modbus.write_single_register(self.slave_addr, mb_addr-1, value, signed=False)
        except Exception as e:
            raise OSError(f'{e}, mb_addr: {mb_addr}, value: {value}')

def main():

    sysair_ftx = SysAir400DC(test_values=test_values, slave_addr=sysair_mb_addr)

    print(f'Starting mqtt-server: {sysair_ftx.base_topic}')
    while True:
        now = time()
        sysair_ftx.mqtt.check_msg()

        if sysair_ftx.last_update is None or now - sysair_ftx.last_update > modbus_update_interval_secs:
            sysair_ftx.present_sensors()
            sysair_ftx.present_sys_info()

        if enable_wdt:
            wdt.feed()

        if enable_alive_led:
            alive_led.update()

        sleep(0.5)

# delay start with some seconds to allow WebREPL to connect
start_delay = 6
print(f'Starting in:')
while True:
    if start_delay == 0:
        break
    print(f'{start_delay}')
    sleep(1)
    start_delay -=1

main()
