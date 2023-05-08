# This file is executed on every boot (including wake-boot from deepsleep)
import machine
import time
import os

def do_connect(ssid, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        counter = 0
        while not sta_if.isconnected():
            pass
            counter += counter
            if counter > 10000000000:
                print('Connection timed out')
                return False
    print('Successfully connected as:', sta_if.ifconfig())
    return True

def get_wifi_credentials(wifi_file_name):
    dir_contents = os.listdir()
    if wifi_file_name in dir_contents:
        print('Wifi credentials found. Testing.')
        f = open(wifi_file_name)
        d = f.readlines()
        f.close()
        wifi_name = d[0].strip()
        wifi_password = d[1].strip()
        is_connected = False
    else:
        print('No wifi credentials stored')
        wifi_name = input('Enter wifi SSID: ')
        wifi_password = input('Enter wifi password: ')
        # need to test here
        if not do_connect(wifi_name, wifi_password):
            print('Connection failed. Quitting without storing credentials.')
            sys.exit()
        print('Connection succeeded!')
        print('Saving new credentials to ' + wifi_file_name + 'to connect automatically upon future reboots. Delete this file to reset stored credentials.')
        f = open(wifi_file_name,'w')
        f.write(wifi_name + '\n' + wifi_password)
        f.close()
        is_connected = True
    print('Wifi name: ' + wifi_name)
    print('Wifi password: ' + wifi_password)
    return wifi_name, wifi_password, is_connected


#import esp
#esp.osdebug(None)
wifi_file_name = 'wifi_credentials.txt'

try:
    wifi_name, wifi_password, is_connected = get_wifi_credentials(wifi_file_name)
except Exception:
    print('ERROR: could not get one or more of Hue bridge IP address, device name, or credentials') 
    sys.exit()
print('Connected to wifi!')

if not is_connected:
    do_connect(wifi_name, wifi_password)


# different ESP32 packages have the in-build LED on different pins
# pin_led1 = machine.Pin(1, machine.Pin.OUT)
# pin_led2 = machine.Pin(2, machine.Pin.OUT) 

# for _ in range(5):
#     pin_led1.on()
#     pin_led2.on()
#     time.sleep_ms(100)
#     pin_led1.off()
#     pin_led2.off()
#     time.sleep_ms(100)


import webrepl
webrepl.start()


