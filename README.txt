# Hugo Grimmett's notes on ESP32 micropython experience
# 2023-04-07

0. Set-up

Ways to access ESP32:

1. screen
2. rshell (python package)
3. mpremote (python package)
4. webrepl (github repo)
5. ampy 

0. set-up

Using esptool.py from github repo (apparently can also use pip to install, but didn't work for me)

Used tutorial from
https://dev.to/tomoyk/esp32-setup-guide-with-macos-m1-mac-2j1c

~/code/thirdparty/esptool git:master > python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 erase_flash

~/code/thirdparty/esptool git:master > python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin

There are two files that run on startup: boot.py, followed by main.py

Default boot.py:
'# This file is executed on every boot (including wake-boot from deepsleep)\n#import esp\n#esp.osdebug(None)\n#import webrepl\n#webrepl.start()\n'

1. screen
screen /dev/cu.usbserial-0001 115200

2. rshell  
pip3 install rshell
Didn't try yet

3. mpremote
pip3 install mpremote
This is the only way I could manage to install external packages (mip not available until micropython v1.20, and the latest esp32 version is 1.19)

To add packages from a host machine:
mpremote connect port:/dev/cu.usbserial-0001 mip install aioble


4. webrepl
On ESP32: 
import webrepl_setup
webrepl.start()

Web interface never worked for me so far (https://micropython.org/webrepl)

Github repo seems to work (https://github.com/micropython/webrepl)
~/code/thirdparty/webrepl git:master > python3 webrepl_cli.py 192.168.178.41

5. Ampy 

ampy website: https://www.digikey.com/en/maker/projects/micropython-basics-load-files-run-code/fb1fcedaf11e4547943abfdd8ad825ce
ampy --port /dev/cu.usbserial-0001 --baud 115200 run test.py
