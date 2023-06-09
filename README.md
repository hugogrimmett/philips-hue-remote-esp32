# Philips Hue remote using ESP32

This project allows you to use an ESP32 microcontroller to send messages to a Hue bridge, to change various home automation light settings. I have it configured with six push switches, each corresponding to a particular scene change.

The code is written in micropython. I download my code to the ESP32 using ampy, use mpremote to download external libraries, and use Screen to run python commands remotely on the microcontroller.

Note: this uses the Philips Hue v1.1 API, which is due to be deprecated in favour of v2 at some point in the future (with some breaking changes).

Hugo Grimmett





# Notes on ESP32 micropython experience
2023-04-07

Table of contents:
1. Set-up
2. screen
3. rshell (python package)
4. mpremote (python package)
5. webrepl (github repo)
6. ampy 
    Hue connection
7. phue python repository
8. esp32 philips hue button (using C++)

## 1. set-up


Using esptool.py from github repo (apparently can also use pip to install, but didn't work for me)

Used tutorial from
https://dev.to/tomoyk/esp32-setup-guide-with-macos-m1-mac-2j1c

Discover ESP32 with ```python3 esptool.py flash_id```

~/code/thirdparty/esptool git:master > ```python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 erase_flash```

~/code/thirdparty/esptool git:master > ```python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin```

Micropython ESP32 documentation: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html

There are two files that run on startup: boot.py, followed by main.py

Default boot.py:
'# This file is executed on every boot (including wake-boot from deepsleep)\n#import esp\n#esp.osdebug(None)\n#import webrepl\n#webrepl.start()\n'

## 2. screen
```screen /dev/cu.usbserial-0001 115200```

## 3. rshell  
```pip3 install rshell```
Didn't try yet

## 4. mpremote
```pip3 install mpremote```

This is the only way I could manage to install external packages (mip not available until micropython v1.20, and the latest esp32 version is 1.19)

To add packages from a host machine:
```mpremote connect port:/dev/cu.usbserial-0001 mip install aioble```


## 5. webrepl
On ESP32: 
```
import webrepl_setup
webrepl.start()
```

Web interface never worked for me so far (https://micropython.org/webrepl)

Github repo seems to work (https://github.com/micropython/webrepl)
~/code/thirdparty/webrepl git:master > ```python3 webrepl_cli.py 192.168.178.41```

## 6. Ampy 

```pip3 install adafruit-ampy```

ampy website: https://www.digikey.com/en/maker/projects/micropython-basics-load-files-run-code/fb1fcedaf11e4547943abfdd8ad825ce
```ampy --port /dev/cu.usbserial-0001 --baud 115200 run test.py```

I've been using this to copy files across to esp32
```ampy --port /dev/cu.usbserial-0001 --baud 115200 put main.py```

If ampy stops working because main.py is running, connect with screen
```
import os
os.remove('main.py')
```

## 7. Phue
https://github.com/studioimaginaire/phue/

## 8. esp32-philips-hue-button
https://github.com/mnkii/esp32-philips-hue-button/blob/master/README.md


## 9. Micropython commands to connect to Hue bridge and change lights/scenes

Install urllib.urequest or urequests using mpremote:
``` mpremote connect port:/dev/cu.usbserial-0001 mip install urequests```

```
import urequests
r = urequests.request('GET','http://192.168.178.40/api/newdeveloper')

r = urequests.request('POST','http://192.168.178.40/api','{"devicetype":"hue_remote#esp32"}')
"success":{"username":"zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n"}

credentials = "zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n"

r = urequests.request('GET','http://192.168.178.40/api/zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n/lights')

Turn light on:
r = urequests.request('PUT','http://192.168.178.40/api/zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n/lights/1/state','{"on":true}')

Turn it off:
r = urequests.request('PUT','http://192.168.178.40/api/zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n/lights/1/state','{"on":false}')

Get state
r = urequests.request('GET','http://192.168.178.40/api/zuMLxhoETtzzWnIjlQidaQx-IXLkKsBTaEOaUM9n/lights/1')

r.json()["state"]["on"]
```


## 10. Hue API
Reference: https://developers.meethue.com/develop/hue-api-v2/api-reference/

Website for talking to the bridge (v1): ```https://192.168.178.96/debug/clip.html```

POST /api   {"devicetype":"test"}