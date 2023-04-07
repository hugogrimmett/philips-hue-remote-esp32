import machine
import time

def toggle(p):
   p.value(not p.value())

pin_led = machine.Pin(2, machine.Pin.OUT)
pin_switch = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
#print(pin13.value())
#for x in range(8):

while (True):
    print(pin_switch.value())
    pin_led.value(pin_switch.value())
    time.sleep_ms(10)


