# This file is executed on every boot (including wake-boot from deepsleep)
import machine
import time

def do_connect(ssid, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
            # machine.Pin(2, machine.Pin.OUT).on()
            # time.sleep_ms(100)
            # machine.Pin(2, machine.Pin.OUT).off()
            # time.sleep_ms(100)
    print('Successfully connected as:', sta_if.ifconfig())


#import esp
#esp.osdebug(None)

# do_connect('FRITZ!Box 7490', '69860468098356516509')
#do_connect('Hugo', '31415926')
do_connect('Schneckenbox', 'Schneckenhaus')

pin_led = machine.Pin(2, machine.Pin.OUT)
for _ in range(5):
    machine.Pin(2, machine.Pin.OUT).on()
    time.sleep_ms(100)
    machine.Pin(2, machine.Pin.OUT).off()
    time.sleep_ms(100)


import webrepl
webrepl.start()


