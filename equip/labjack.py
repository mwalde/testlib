from time import sleep

class LabJack( ):
    labjack = None
    #====================================================================
    #                   init Lab Jack
    #====================================================================
    def __init__(self, use_labjack):
        if use_labjack == 'true':
            import u3
            self.labjack = u3.U3()
            self.u3 = u3
            # enable counter for GPS pulse
            self.labjack.configIO( TimerCounterPinOffset = 5, EnableCounter0 = True, NumberOfTimersEnabled = 1)
  
    def getAmbientTemp( self ):
        if self.labjack:
            temperature = self.labjack.getTemperature() - 273
        else:
            temperature = 28    # default ambient temperature
        return temperature
        
    def GPSpulseTest( self ):
        if self.labjack:
            test_count = 4
            counter = self.labjack.getFeedback(self.u3.Counter(counter = 0, Reset = True))
            sleep(test_count + 1)
            counter = self.labjack.getFeedback(self.u3.Counter(counter = 0, Reset = False))
            if counter[0] >= test_count:
                print 'GPS PULSE PASS %d' % counter[0]
                GPSpulse ='PASS'
            else:
                print 'GPS PULSE FAIL %d' % counter[0]
                GPSpulse = 'FAIL'
        else:
            GPSpulse = 'NA'
        return GPSpulse