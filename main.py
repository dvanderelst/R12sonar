import utime
import pyb
import array
import pyb
import json
import time
from machine import UART


break_char = '*'

red = pyb.LED(1)
green = pyb.LED(2)
orange = pyb.LED(3)
blue = pyb.LED(4)


# For uart communication
uart = UART(1, 9600)                         
uart.init(9600, bits=8, parity=None, stop=1)
# For usb communication
usb = pyb.USB_VCP()

fs = 100000
ms = 50
samples = int((fs/1000) * ms)
buffer = array.array('H', (0 for i in range(samples)))
timer = pyb.Timer(6, freq=fs)

adc1 = pyb.ADC(pyb.Pin.board.Y11)
trigger_pin1 = pyb.Pin('X1', pyb.Pin.OUT_PP)

adc2 = pyb.ADC(pyb.Pin.board.Y12)
trigger_pin2 = pyb.Pin('X2', pyb.Pin.OUT_PP)


################################################
#
output_type = 'uart'
#
################################################


def measure(channel=1):
    if channel == 1:
        trigger_pin1.high()
        utime.sleep_us(50)
        trigger_pin1.low()    
        adc1.read_timed(buffer, timer)
        
    if channel == 2:
        trigger_pin2.high()
        utime.sleep_us(50)
        trigger_pin2.low()    
        adc2.read_timed(buffer, timer)
        
def listen_for_uart():
    message = ''
    while True:
        part = uart.read()
        green.toggle()
        if part is not None:
            part = part.decode('utf-8')
            part = part.rstrip('\n\r')     
            message = message + part
        if break_char in message: break
    #we want to respond to integer commands
    message = message.rstrip(break_char)
    message = int(message)
    return message


def listen_for_usb():
    message = None
    while True:
        orange.on()
        waiting = usb.any()
        message = usb.read()
        orange.off()
        #Apparently, when plugging in the device to the host some info is sent
        #we want to discard this and only respond to integer commands
        try:
            message = message.decode('utf-8')
            message = message.rstrip(break_char)
            message = int(message)
            break
        except:
            pass
    return message
 



if output_type == 'usb':
    while True:
        red.on()
        channel = listen_for_usb()
        measure(channel=channel)
        red.off()
        usb.send(buffer) #for usb communication
        
        #s = json.dumps(buffer) # for uart communication
        #uart.write(s)


if output_type == 'uart':
    while True:
        blue.on()
        channel = listen_for_uart()
        print(channel)
        measure(channel=channel)
        blue.off()
        s = json.dumps(buffer) # for uart communication
        uart.write(s)
       
