import myEmitter
import myMics
import mySettings
import utime


class sonar:
    def __init__(self):
        self.mics = myMics.mics()
        self.emitter = myEmitter.emitter()
    
    def pulse(self, dac_cycles=None):
        if dac_cycles is None: dac_cycles = mySettings.dac_cycles
        self.emitter.emit(dac_cycles)
        A, B = self.mics.measure()
        return A,B