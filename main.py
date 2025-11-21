print('starting main.py')

import help_functions
import sysair_registers

from machine import Pin, unique_id

import time

from ubinascii import hexlify

from umqtt.simple import MQTTClient

# from uModBusSerial_OLD_MODBUS import uModBusSerial
from umodbus.serial import Serial as ModbusSerial

# from pichler_registers import pichler_input_registers

mqtt_server = '10.9.8.143'

test_values = False     # will omit modbus-read and use test-values prepared from system air registers

#####
# Schematic/Notes
######

# GPIO1 UART TX
# GPIO3 UART RX
# GPIO15 TX enable + RX not-enable changed to GPIO14 due to problem to boot (was pulled high)

#####
# Watchdog - 60 seconds, need to be larger then loop time below. Works only on ESP32
# Don't forget to enable wdt.feed() below
#####

# wdt = WDT(timeout=60000)

#####
# RS485/modbus via UART
#####
print('Before modbus creation')

# modbus = uModBusSerial.ModBusSerial(uart_id=1, baudrate=19200, data_bits=8, parity=0, stop_bits=1, pins=[Pin(17), Pin(16)], ctrl_pin=16)
modbus = ModbusSerial(uart_id=1, baudrate=19200, data_bits=8, parity=0, stop_bits=1, pins=[Pin(17), Pin(16)], ctrl_pin=16)

print("modbus created")
#####
# LG350 connection
#####

class PichlerLG350:
    def __init__(self, modbus):
    #def __init__(self):    
        self.modbus = modbus
    
    @property
    def luftstufe(self):
        #value = self.modbus.read_holding_registers(20, 2, 1)[0]
        value = 132
        return value

    @luftstufe.setter
    def luftstufe(self, value):
        value = int(value)
        if value >= 0 and value < 4:
            self.modbus.write_single_register(20, 2, value)
        else:
            print("luftstufe out of range")

    def get_input_registers(self):
        results = {}
        for name, params in pichler_input_registers.items():
            if params[3] == True:
                value = self.modbus.read_input_registers(20, params[0], 1)[0]
                value += params[1]
                value *= params[2]
                results.update({name: value})
        results.update({"str1": 12})    
        results.update({"str2": 23})
        results.update({"str3": 34})
        return results

# pichler = PichlerLG350(modbus)

class SysAir400DC:
    def __init__(self, topic = None, slave_addr:int = 1, test_values=False):
        if topic is None:
            self.base_topic = 'system_air_VR400DC_ftx'
        else:
            self.base_topic = topic

        self.test_values = test_values
        self.slave_addr = slave_addr
        self.registers = sysair_registers.registers()
        self.mqtt = self.create_mqtt()

    def create_mqtt(self)->MQTTClient:
        mqtt_client = MQTTClient(server=mqtt_server, client_id=hexlify(unique_id()), user="", password="")
        mqtt_client.connect()
        print(f'Mqtt client: {mqtt_client.client_id}, to server: {mqtt_client.server} created')
        return mqtt_client

    def present_sensors(self):
        for sensor_topic, register in self.registers.items():
            if not register.get('include'):
                continue
            mb_addr = register.get('mb_addr')
            scaling = register.get('scaling')
            if not self.test_values:
                sensor_value = self.read_input_registers(mb_addr, scaling)
            else:
                sensor_value = register.get('test_value')
            self.publish_to_mqtt(sensor_topic + '/value', sensor_value)
            register_details = register.get('binary_coded')
            if register_details is not False:
                if register_details.get('type') == 'SINGLE':
                    self.publish_to_mqtt(sensor_topic + '/status',
                                         str(register_details.get('coding').get(sensor_value)).replace(' ', '_'))
                    for i, status_item in register_details.get('coding').items():
                        self.publish_to_mqtt(f'{sensor_topic}/binary/{status_item.replace(" ", "_")}', i == sensor_value)
                elif register_details.get('type') == 'BINARY':
                    print(f'Number of reg details: {len(register_details.get("coding"))}')
                    b = help_functions.int_to_binary(sensor_value)
                    for i, status_item in register_details.get('coding').items():
                        bit_value = len(b) > i and b[i] == 1
                        self.publish_to_mqtt(f'{sensor_topic}/binary/{status_item.replace(" ", "_").replace("/","-")}', bit_value)

    def publish_to_mqtt(self, sensor_topic, value):
        mqtt_topic = (self.base_topic + '/' + sensor_topic).lower()
        msg = str(value).lower()
        print(f'mqtt publish, topic: {mqtt_topic}, value: {msg}')
        self.mqtt.publish(str(mqtt_topic), msg)

    def read_input_registers(self, mb_addr, scaling)-> float | int:
        recv_value = modbus.read_input_registers(self.slave_addr, mb_addr, 1)[0]
        if scaling == 1:
            return recv_value
        else:
            return recv_value / scaling


#####
# MQTT connection
#####

class SensorClient:
    def __init__(self, sensor, client_id, server):
        self.sensor = sensor
        self.mqtt = MQTTClient(client_id, server, user="", password="")
        self.name = b'myhome/lueftung'
        self.mqtt.connect()
        self.mqtt.set_callback(self.callback_mqtt_msg)
        self.mqtt.subscribe(self.name + b'/set_luftstufe')

    def publish_luftstufe(self, ls):
        print("Sending luftstufe = {0}".format(ls))
        self.mqtt.publish(self.name + b'/luftstufe', str(ls))

    def publish_generic(self, name, value):
        print("Sending {0} = {1}".format(name, value))
        self.mqtt.publish(self.name + b'/' + bytes(name, 'ascii'), str(value))

    def callback_mqtt_msg(self, topic, msg):
        print("received MQTT message")
        print(topic, msg)
        if topic == self.name + b'/set_luftstufe':
            pass
            # pichler.luftstufe = int(msg)  

def connect_mqtt():
    print("connect mqtt")
    try:
        # init_wifi()
        print("try to connect to MQTT server")        
        sc_try = SensorClient('lueftung', hexlify(unique_id()), '10.9.8.143')
    except:
        sc_try = None

    return sc_try

#####
# Main loop
#####

def mainloop():
    count = 1
    sa = SysAir400DC(test_values=test_values)
    errcount = 0 
    while count < 10:
        sa.present_sensors()
        count +=1

        #if sa is None:
        #    print('recreating SA')
        #    count += 1
        #    sa = SysAir400DC(test_values=True)
        #    continue
        #else:
        #    try:
        #        print('attempting publish to mqtt')
        #        sa.present_sensors()
#
        #    except:
        #        count += 1

        #if errcount > 20:
        #    reset()

        # wdt.feed()

        time.sleep(2)

mainloop()

