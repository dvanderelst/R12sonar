import utime
import pyb
import array
import pyb
import json
import time
import machine

break_char = '*'

red = pyb.LED(1)
green = pyb.LED(2)
orange = pyb.LED(3)
blue = pyb.LED(4)

baud =  9600 #
uart = pyb.UART(1, baud)                         
uart.init(baud, bits=8, parity=None, stop=1)


signal_threshold = 2000

adc1 = pyb.ADC(pyb.Pin.board.Y11)
trigger_pin1 = pyb.Pin('X1', pyb.Pin.OUT_PP)

adc2 = pyb.ADC(pyb.Pin.board.Y12)
trigger_pin2 = pyb.Pin('X2', pyb.Pin.OUT_PP)

trigger_pin1.low()
trigger_pin2.low()


test = False

def measure(channel, fs, duration):
    value = 0
    samples = int((fs/1000) * duration)
    timer = pyb.Timer(6, freq=fs)
    buffer = array.array('H', (0 for i in range(samples)))
    if test: print('Channel', channel)
    
    if channel == 1: trigger_pin1.high()
    if channel == 2: trigger_pin2.high()
    
    utime.sleep_us(50)
    
    trigger_pin1.low()
    trigger_pin2.low()
    
    start_counter = utime.ticks_ms()
    while value < signal_threshold:
        if channel == 1: value = adc1.read()
        if channel == 2: value = adc2.read()
        current_counter = utime.ticks_ms()
        if current_counter - start_counter > 1000: break

    
    if channel == 1: adc1.read_timed(buffer, timer)
    if channel == 2: adc2.read_timed(buffer, timer) 
    
    return buffer


def measure_both(first, second, fs, duration):
    buffer1 = measure(first, fs, duration)
    utime.sleep_ms(100)
    buffer2 = measure(second, fs, duration)
    total = buffer1 + buffer2
    return total
    
    
def listen_for_uart():
    message = ''
    while True:
        part = uart.read()
        #green.toggle()
        if part is not None:
            part = part.decode('utf-8')
            part = part.rstrip('\n\r')     
            message = message + part
        if break_char in message: break
    message = message.rstrip(break_char)
    message = message.split(',')
    parameters = []
    for x in message: parameters.append(int(x))
    return parameters




if test:
    while True:
        buffer = measure_both(1, 2, 10000, 10)
        utime.sleep(0.1)
        print('done')
else:
    blue.off()
    while True:
        parameters = listen_for_uart()
        blue.on()
        first_channel = parameters[0]
        second_channel = parameters[1]
        sample_rate = parameters[2]
        duration = parameters[3]
        green.on()
        total_buffer = measure_both(first_channel, second_channel, sample_rate, duration)
        green.off()
        orange.on()
        uart.write(total_buffer)
        orange.off()
        blue.off()
        


       
