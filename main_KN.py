# main.py -- put your code here!
import pyb
import json
import time
from machine import UART
import mySettings
import mySonar

green = pyb.LED(2)
red = pyb.LED(1)
sonar = mySonar.sonar()

uart = UART(1, 9600)                         
uart.init(9600, bits=8, parity=None, stop=1)
    

def listen():
    message = ''
    while True:
        part = uart.read()
        green.toggle()
        if part is not None:
            part = part.decode('utf-8')
            part = part.rstrip('\r')
            part = part.rstrip('\n')
            print('part', part)
            message = message + part
        if mySettings.break_char in message: break
    return message



while True:
    red.on()
    A,B = sonar.pulse()
    time.sleep(1)
    print(len(A))
    red.off()
    s = json.dumps(A)
    uart.write(s)
    s = json.dumps(B)
    uart.write(s)
    
    
    



# while True:
#     msg = listen()
#     if '100' in msg:
#         red.on()
#         A,B = mics.measure()
#         print(len(A))
#         red.off()
#         s = json.dumps(A)
#         uart.write(s)
#         s = json.dumps(B)
#         uart.write(s)
#         


