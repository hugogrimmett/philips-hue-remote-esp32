Used tutorial from
https://dev.to/tomoyk/esp32-setup-guide-with-macos-m1-mac-2j1c

~/code/thirdparty/esptool git:master > python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 erase_flash

~/code/thirdparty/esptool git:master > python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin


screen /dev/cu.usbserial-0001 115200

ampy website: https://www.digikey.com/en/maker/projects/micropython-basics-load-files-run-code/fb1fcedaf11e4547943abfdd8ad825ce
ampy --port /dev/cu.usbserial-0001 --baud 115200 run test.py

import webrepl_setup
webrepl.start()

import network
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('FRITZ!Box 7490', '69860468098356516509')

'# This file is executed on every boot (including wake-boot from deepsleep)\n#import esp\n#esp.osdebug(None)\n#import webrepl\n#webrepl.start()\n'


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('FRITZ!Box 7490', '69860468098356516509')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())