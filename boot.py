# This file is executed on every boot (including wake-boot from deepsleep)

def do_connect(ssid, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('Network config:', sta_if.ifconfig())

#import esp
#esp.osdebug(None)

do_connect('FRITZ!Box 7490', '69860468098356516509')
#do_connect('Hugo', '31415926')
#do_connect('Schneckenbox', 'Schneckenhaus')

import webrepl
webrepl.start()


