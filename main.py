import machine
import time
import urequests
import os
import sys

def main():
    saved_info_file_name = 'hue_ip_credentials.txt'
    light_index = 1
    try:
        hue_bridge_ip_address, device_name, credentials = get_ip_device_credentials(saved_info_file_name)
    except Exception:
        print('ERROR: could not get one or more of Hue bridge IP address, device name, or credentials') 
        sys.exit()
    print('Connected to bridge!')

    pin_led = machine.Pin(2, machine.Pin.OUT)
    pin_switch = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pin_button1 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pin_button2 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pin_button3 = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pin_button4 = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pin_button5 = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_DOWN)
    pin_button6 = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_DOWN)

    room = 'office'
    group_id = 1
    scene_button1 = 'aoYhBTLiGLJYEYy'
    scene_button2 = 'fFTqOx3xZFwSjvu'
    scene_button3 = 'A6SMSLSLbYPL0pj'
    scene_button4 = '9nmL2oMZ0MWEstw'
    scene_button5 = 'sK2PYzdtkWIzklc'
    scene_button6 = 'jW--LK2MtUzKJ-B'

    scenes = ['aoYhBTLiGLJYEYy', 'fFTqOx3xZFwSjvu', 'A6SMSLSLbYPL0pj', '9nmL2oMZ0MWEstw', 'sK2PYzdtkWIzklc', 'jW--LK2MtUzKJ-B']
    # button_to_scene = {}
    # for k in range(6):
    #     button_to_scene[k] = 
    
    # call: aoYhBTLiGLJYEYy
    # solo work - daytime: fFTqOx3xZFwSjvu 
    # night: A6SMSLSLbYPL0pj
    # movie: 9nmL2oMZ0MWEstw
    # techno: sK2PYzdtkWIzklc
    # reading: jW--LK2MtUzKJ-B

    # r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index))
    # light_state = r.json()["state"]["on"]
    # r.close()

    print('Scanning for button presses...')
    while True:
        # first = pin_switch.value()
        # time.sleep_ms(10)
        # second = pin_switch.value()
        first_values = (pin_button1.value(), pin_button2.value(), pin_button3.value(), pin_button4.value(), pin_button5.value(), pin_button6.value())
        time.sleep_ms(10)
        second_values = (pin_button1.value(), pin_button2.value(), pin_button3.value(), pin_button4.value(), pin_button5.value(), pin_button6.value())
        button_id = 0;
        for first, second in zip(first_values, second_values):
            if second and not first:
                print('Button ' + str(button_id) + ' pressed!')
            elif first and not second:
                print('Button ' + str(button_id) + ' released!') 
                activate_scene(hue_bridge_ip_address, credentials, group_id, scenes[button_id])
            button_id += 1
                # r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index))
                # light_state = r.json()["state"]["on"]
                # r.close()
                # print('   light state was %s...' % light_state)
                # r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":%s}' % str(not light_state).lower())
                # print('   ... switching to %s' % (not light_state))
                # r.close()

def activate_scene(hue_bridge_ip_address, credentials, group_id, scene_id, transition_time=4):
    # r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/groups/' + str(group_id) + '/action','{"scene":"' + scene_id + '", "transitiontime": "' + str(transition_time) + '"}')
    r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/groups/' + str(group_id) + '/action','{"scene":"' + scene_id + '"}')
    # return self.request('PUT', '/api/' + self.username + '/groups/' +
    #                     str(group_id) + '/action',
    #                     {
    #                         "scene": scene_id,
    #                         "transitiontime": transition_time
    #                     })

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
            raise Exception
        # if not test_credentials(hue_bridge_ip_address, credentials):
        #     print("ERROR: credentials invalid: " + credentials)
        #     raise Exception
    else:
        print('No credentials stored')
        hue_bridge_ip_address = input('Hue bridge IP address (e.g. 192.168.178.96): ')
        if not test_hue_bridge_connection(hue_bridge_ip_address):
            print("ERROR: could not locate Hue bridge at the address: " + hue_bridge_ip_address)
            raise Exception
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
        r.close()
        return False
    r.close()
    return credentials

def test_credentials(hue_bridge_ip_address, credentials):
    print(hue_bridge_ip_address)
    print(credentials)
    print('http://' + hue_bridge_ip_address + '/api/'+ credentials)
    r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/'+ credentials)
    print('JSON contains: \n' + r.json())
    try:
        print('JSON contains: \n' + r.json())
        r.json()[0]["error"]["description"]
        r.close()
    except KeyError:
        # this is the good outcomel, because the error field doesn't exist
        print('   ...credentials pass')
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
        r.close()
    except OSError:
        print('ERROR: cannot connect to Hue bridge on given IP address: ' + hue_bridge_ip_address)
        return False
    print('   ...bridge connection passes')
    return True



if __name__ == "__main__":
    main()





# to automate getting the hue bridge IP:
# def get_ip_address(self, set_result=False):

#     """ Get the bridge ip address from the meethue.com nupnp api """

#     connection = httplib.HTTPSConnection('www.meethue.com')
#     connection.request('GET', '/api/nupnp')

#     logger.info('Connecting to meethue.com/api/nupnp')

#     result = connection.getresponse()