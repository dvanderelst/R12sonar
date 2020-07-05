# main.py -- put your code here!
import pyb
from machine import UART

uart = UART(1, 9600)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters
      # read 10 characters, returns a bytes object


def listen():
    message = ''
    while True:
        part = uart.read()
        if part is not None:
            part = part.decode('utf-8')
            part = part.rstrip('\r')
            part = part.rstrip('\n')
            print('part', part)
            message = message + part
        if "*" in message: break
    return message
    


led = pyb.LED(2)
while True:
    msg = listen()
    print('message:', msg)
    if 'on' in msg: led.on()
    if 'off' in msg: led.off()
    


