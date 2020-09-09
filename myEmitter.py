import math
import pyb
from pyb import DAC,delay
import MySettings
import Misc

# At 40Khz, 40 cycles == 1 ms
class emitter:
    def __init__(self):
        self.dac = DAC(MySettings.dac_channel)
        self.cycles = 0
        self.frequency = 40000
        self.fs = None
    
    def make_buffer(self, cycles):
        self.buffer, self.fs = Misc.get_wave(cycles)
        self.cycles = cycles
        
    def emit(self, cycles=40):
        if cycles != self.cycles: self.make_buffer(cycles)
        self.dac.write_timed(self.buffer, self.fs, mode=DAC.NORMAL)
        

if __name__ == "__main__":
    s = emitter()
    s.emit(5)
    print('done')
