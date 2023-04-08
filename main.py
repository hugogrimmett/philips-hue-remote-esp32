import machine
import time
import urequests

hue_bridge_ip_address = '192.168.178.40' #test bridge
credentials = "zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n"
light_index = 1

pin_led = machine.Pin(2, machine.Pin.OUT)
pin_switch = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index))
light_state = r.json()["state"]["on"]

print('Scanning for button presses...')
while (True):
    if pin_switch.value() == 1:
        # print('button is on')
        if pin_switch.value() == 0:
            print('Button pressed and released')
            # print('button is off')
            r = urequests.request('GET','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index))
            light_state = r.json()["state"]["on"]
            print('   light state was %s...' % light_state)
            r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":%s}' % str(not light_state).lower())
            print('   ... switching to %s' % (not light_state))

# turn light on
# r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":true}')
# turn light off
# r = urequests.request('PUT','http://' + hue_bridge_ip_address + '/api/' + credentials + '/lights/' + str(light_index) + '/state','{"on":false}')


#print(pin13.value())
#for x in range(8):

#while (True):
#    print(pin_switch.value())
#    print('Checking switch value and matching LED status to it... ctrl+C to interrupt.')
#    pin_led.value(pin_switch.value())
#    time.sleep_ms(10)




