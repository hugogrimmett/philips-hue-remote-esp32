# Notes on ESP32 micropython experience
2023-04-07
Experience rating: 3/5 stars

Table of contents:
    Init
0. Set-up
    Ways to access ESP32:
1. screen
2. rshell (python package)
3. mpremote (python package)
4. webrepl (github repo)
5. ampy 
    Hue connection
6. phue python repository
7. esp32 philips hue button (using C++)

## 0. set-up

Using esptool.py from github repo (apparently can also use pip to install, but didn't work for me)

Used tutorial from
https://dev.to/tomoyk/esp32-setup-guide-with-macos-m1-mac-2j1c

~/code/thirdparty/esptool git:master > python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 erase_flash

~/code/thirdparty/esptool git:master > python3 esptool.py --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin

There are two files that run on startup: boot.py, followed by main.py

Default boot.py:
'# This file is executed on every boot (including wake-boot from deepsleep)\n#import esp\n#esp.osdebug(None)\n#import webrepl\n#webrepl.start()\n'

## 1. screen
screen /dev/cu.usbserial-0001 115200

## 2. rshell  
pip3 install rshell
Didn't try yet

## 3. mpremote
pip3 install mpremote
This is the only way I could manage to install external packages (mip not available until micropython v1.20, and the latest esp32 version is 1.19)

To add packages from a host machine:
mpremote connect port:/dev/cu.usbserial-0001 mip install aioble


## 4. webrepl
On ESP32: 
import webrepl_setup
webrepl.start()

Web interface never worked for me so far (https://micropython.org/webrepl)

Github repo seems to work (https://github.com/micropython/webrepl)
~/code/thirdparty/webrepl git:master > python3 webrepl_cli.py 192.168.178.41

## 5. Ampy 

ampy website: https://www.digikey.com/en/maker/projects/micropython-basics-load-files-run-code/fb1fcedaf11e4547943abfdd8ad825ce
ampy --port /dev/cu.usbserial-0001 --baud 115200 run test.py


## 6. Phue
https://github.com/studioimaginaire/phue/

## 7. esp32-philips-hue-button
https://github.com/mnkii/esp32-philips-hue-button/blob/master/README.md



https://docs.micropython.org/en/latest/library/network.html
Great ttorial on socket module: https://internalpointers.com/post/making-http-requests-sockets-python
import network
import time
import socket

# Port is always 80 because it's an http protocol
port = 80
host = '192.168.178.40'
request = b"GET / HTTP/1.1\r\nHost:192.168.178.40/api/newdeveloper\r\n\r\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
send_data(s, request)
response = receive_data(s)
s.close()
print(response.decode())

def send_data(socket, request):
    # note: could replace this all with sendall()
    sent    = 0
    while sent < len(request):
        sent = sent + s.send(request[sent:])    # Send a portion of 'request', starting from 'sent' byte

def receive_data(socket):
    chunk_length = 4096
    chunk = socket.recv(chunk_length)
    message_length = get_message_length_from_html_header(chunk)
    response = b""
    if message_length < chunk_length:
        return chunk
    else:
        remainder = socket.recv(message_length - chunk_length)
        return chunk + remainder

def get_message_length_from_html_header(html):
    header_length = len(html.decode().split("\r\n\r\n")[0])+8 # 8 for the \r\n\r\n characters -- but should it be +4 instead? messages seem to be 4 characters shorter than reported
    parts = html.decode().split("\r\n")
    for part in parts:
        if "Content-Length" in part:
            return int(part.split(": ")[1])+ header_length
    return 0
