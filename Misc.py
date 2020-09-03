import math


def get_wave(cycles, freq=40000, fs=500000):
    samples = int((fs/freq) * cycles)
    buffer = bytearray(samples)
    for i in range(samples):
        buffer[i] = 128 + int(127 * math.sin(2 *  freq * math.pi * i/fs))
    return buffer, fs


from pyb import DAC
# output the sine-wave at 400Hz
#dac = DAC(1)
#buffer, fs = get_wave(cycles=10, freq=250)
#dac.write_timed(buffer, fs, mode=DAC.CIRCULAR)
#for x in buffer: print(x)

