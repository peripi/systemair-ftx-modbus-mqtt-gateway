# systemair-ftx-modbus-mqtt-gateway
A modbus mqtt gateway based on micropython for System Air residental ftx units

Modbus library from https://github.com/brainelectronics/micropython-modbus

Tested on ESP32 (Wemos D1 mini) + RS485 (C25B) module
 * GPIO-17 UART TX to C25B DI - driver input
 * GPIO-16 UART RX to C25B RO - receiver output
 * GPIO-19 ctrl pin

C25B, TTL to RS485. Note that A/B-markings on the C25B (at least the one I used) are not correct/confusing.
 * Normal RS485 A(-) should be connected to C25B pin B
 * Normal RS485 B(+) should be connected to C25B pin A

Registers to be shown by mqtt according to document MODBUS_FOR_RESIDENTIAL_D24810_USER_MANUAL_EN__A007_.PDF found on systemairs webpage
