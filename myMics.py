import pyb
import array
import gc
import utime
import mySettings

gc.collect()

class mics:
    def __init__(self):
        adc_rate = mySettings.adc_rate
        adc_samples = mySettings.adc_samples
        adc_bits = mySettings.adc_bits
        
        self.micA = pyb.ADC(mySettings.mic_A)    # Create ADC's
        self.micB = pyb.ADC(mySettings.mic_B)
        self.timer = pyb.Timer(8, freq=adc_rate)        # Create timer
        self.rxA = array.array(adc_bits, (0 for i in range(adc_samples)))
        self.rxB = array.array(adc_bits, (0 for i in range(adc_samples)))
    
    def measure(self):
        start = utime.ticks_us()
        mics = (self.micA, self.micB)
        buffers = (self.rxA, self.rxB)
        pyb.ADC.read_timed_multi( mics, buffers, self.timer)
        end = utime.ticks_us()
        duration = end - start
        return self.rxA, self.rxB


