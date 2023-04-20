import machine
import time
import urequests
import os

# hue_bridge_ip_address = '192.168.178.96' # wenckebachstr 2


# credentials = "zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n"
# light_index = 1

# pin_led = machine.Pin(2, machine.Pin.OUT)
# pin_switch = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
# r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index))
# light_state = r.json()["state"]["on"]

# print('Scanning for button presses...')
# while (True):
#     if pin_switch.value() == 1:
#         # print('button is on')
#         if pin_switch.value() == 0:
#             print('Button pressed and released')
#             # print('button is off')
#             r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index))
#             light_state = r.json()["state"]["on"]
#             print('   light state was %s...' % light_state)
#             r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":%s}' % str(not light_state).lower())
#             print('   ... switching to %s' % (not light_state))

# turn light on
# r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":true}')
# turn light off
# r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":false}')


# print(pin13.value())
# for x in range(8):

# while (True):
#    print(pin_switch.value())
#    print('Checking switch value and matching LED status to it... ctrl+C to interrupt.')
#    pin_led.value(pin_switch.value())
#    time.sleep_ms(10)

def get_ip_device_credentials(saved_info_file_name):
    dir_contents = os.listdir()
    if saved_info_file_name in dir_contents:
        print('Credentials found. Testing.')
        f = open(saved_info_file_name)
        d = f.readlines()
        f.close()
        # if len(d) != 2:
        #     raise Exception('Credentials file is corrupt')
        hue_bridge_ip_address = d[0].strip()
        device_name = d[1].strip()
        credentials = d[2].strip()
        if not test_hue_bridge_connection(hue_bridge_ip_address):
            print("ERROR: could not locate Hue bridge at the address: " + hue_bridge_ip_address)
            return False
        if not test_credentials(hue_bridge_ip_address, credentials):
            print("ERROR: credentials invalid: " + credentials)
            return False
    else:
        print('No credentials stored')
        hue_bridge_ip_address = input('Hue bridge IP address (e.g. 192.168.178.96): ')
        if not test_hue_bridge_connection(hue_bridge_ip_address):
            print("ERROR: could not locate Hue bridge at the address: " + hue_bridge_ip_address)
            return False
        device_name = input('Choose a device name for your ESP32: ')
        credentials = get_new_credentials(device_name, hue_bridge_ip_address)
        print('Saving new credentials to ' + saved_info_file_name + 'to connect automatically upon future reboots. Delete this file to reset stored credentials.')
        f = open(saved_info_file_name,'w')
        f.write(hue_bridge_ip_address + '\n' + device_name + '\n' + credentials)
        f.close()
    print('Hue bridge IP address: ' + hue_bridge_ip_address)
    print('Device name: ' + device_name)
    print('Credentials: ' + credentials)
    return hue_bridge_ip_address, device_name, credentials


def get_new_credentials(device_name, hue_bridge_ip_address):
    # test IP address
    if not test_hue_bridge_connection(hue_bridge_ip_address):
        return False

    # get new credentials:
    input('Press the button on the Hue bridge, and then ENTER on your keyboard, within 10 seconds of each other')
    r = urequests.request('POST','http://' + hue_bridge_ip_address + '/api','{"devicetype":"' + device_name + '"}')
    # print(r.text)
    try:
        credentials = r.json()[0]['success']['username']
    except TypeError:
        print('ERROR: could not parse Hue bridge response')
        return False
    return credentials

def test_credentials(hue_bridge_ip_address, credentials):
    r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/'+ credentials)
    try:
        r.json()[0]["error"]["description"]
    except KeyError:
        # this is the good outcomel, because the error field doesn't exist
        return True
    except:
        print('ERROR: in test_credentials. Something else went wrong')
        return False
        # return True
    # else, credentials fail
    print("ERROR: credentials are invalid")
    return False


def test_hue_bridge_connection(hue_bridge_ip_address):
    try:
        r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/newdeveloper')
    except OSError:
        print('ERROR: cannot connect to Hue bridge on given IP address: ' + hue_bridge_ip_address)
        return False
    return True



saved_info_file_name = 'hue_ip_credentials.txt'
light_index = 1
hue_bridge_ip_address, device_name, credentials = get_ip_device_credentials(saved_info_file_name)
# flash the light on and off
r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":true}')
time.sleep_ms(1000)
r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":false}')

# def is_hue_bridge_connected(hue_bridge_ip_address):
#     # send test message
#     try: 
#         r = urequests.request('GET','http://'+hue_bridge_ip_address+'/api/newdeveloper')

