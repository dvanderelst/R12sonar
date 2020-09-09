import utime
import pyb
import array
import pyb
import json
import time
from machine import UART


green = pyb.LED(2)
red = pyb.LED(1)

uart = UART(1, 9600)                         
uart.init(9600, bits=8, parity=None, stop=1)
    

break_char = '*'
fs = 1000
ms = 50
samples = int((fs/1000) * ms)
buffer = array.array('H', (0 for i in range(samples)))
timer = pyb.Timer(6, freq=fs)

adc1 = pyb.ADC(pyb.Pin.board.Y11)
trigger_pin1 = pyb.Pin('X1', pyb.Pin.OUT_PP)


def measure(channel=1):
    if channel == 1:
        trigger_pin1.high()
        utime.sleep_us(50)
        trigger_pin1.low()    
        adc1.read_timed(buffer, timer)
        
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
        if break_char in message: break
    return message


    


while True:
    red.on()
    measure()
    time.sleep(1)
    red.off()
    
    s = json.dumps(buffer)
    uart.write(s)
   
