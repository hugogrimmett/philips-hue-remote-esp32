import machine
import time
import socket
import network

def toggle(p):
   p.value(not p.value())

def request(self, mode='GET', address=None, data=None):
    """ Utility function for HTTP GET/PUT requests for the API"""
    connection = httplib.HTTPConnection(self.ip, timeout=10)

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

hue_bridge_ip_address = '192.168.178.40' #test bridge

pin_led = machine.Pin(2, machine.Pin.OUT)
pin_switch = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)
#print(pin13.value())
#for x in range(8):

#while (True):
#    print(pin_switch.value())
#    print('Checking switch value and matching LED status to it... ctrl+C to interrupt.')
#    pin_led.value(pin_switch.value())
#    time.sleep_ms(10)


port = 80
host = '192.168.178.40'
request = b"GET / HTTP/1.1\r\nHost:192.168.178.40/api/newdeveloper\r\n\r\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
send_data(s, request)
response = receive_data(s)
s.close()
print(response.decode())

