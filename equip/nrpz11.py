import visa 
from time import sleep
from math import pow,log10,sqrt

#read the help here: http://pyvisa.readthedocs.org/en/latest/api/highlevel.html
# import numpy as np #read the help here: http://docs.scipy.org/doc/numpy/
# import matplotlib.pyplot as plt #read the help here: http://matplotlib.org/users/pyplot_tutorial.html

MW2DBM = lambda mw: 10 * log10(abs(float(mw) * 100)) + 10

class nrpz11 ():
        
    def __init__( self, resource_name, **keyw ):
        self.rm = visa.ResourceManager()
        print self.rm.list_resources()
        self.nrpz = self.rm.open_resource( resource_name )
        self.resource_name = resource_name
#        self.nrpz = visa.instrument( resource_name, **keyw )
        print self.nrpz.ask("*idn?")
        self.nrpz.ask("SYST:INIT")
        self.nrpz.write("*RST")
        self.nrpz.write("SENS:AVER:STAT OFF")
        
    def close( self ):
        self.nrpz.close()
        
    def calibrate( self ):
        print "Calibrating %s. . ." % self.resource_name
        self.nrpz.write("CAL:ZERO:AUTO ONCE")
        print "Complete"
        
    def function( self, mode ):
        sensemode = { \
            "average": "POW:AVG",
            "timeslot": "POW:TSL:AVG",
            "burst": "POW:BURS:AVG",
            "scope": "POW:XTIM:POW"
            }

        cmd = sensemode.get( mode , None )
        if cmd:
            cmd = "SENS:FUNC " + cmd
            print cmd
            self.nrpz.write(cmd)
        else:
            print "mode unknown: ", mode
            
    def get_function( self ):
            funct = self.nrpz.ask("SENS:FUNC?")
            print funct
            return funct
            
    def setoffset( self, dB ):
        self.nrpz.write("SENS:CORR:OFFSet %f" % dB)
        #self.nrpz.write("SENS:CORR:OFFSet:STATe ON")
        
    def getoffset( self ):
        offset = self.nrpz.ask("SENS:CORR:OFFSet?")
        return offset
        
    def setfreq( self, freq_mhz):
         cmd = "SENS:FREQ %e" % (freq_mhz * 1.0e6)
         print cmd
         self.nrpz.write(cmd)
   
    def getfreq( self ):
        cmd = "SENS:FREQ?"
        freq_mhz = float(self.nrpz.ask( cmd )) / 1.0e6
        print cmd, freq_mhz
        return freq_mhz
        
    def initIMM( self ):
        cmd = "INIT:IMM"
#        print cmd
 #       self.nrpz.write(cmd)
        
        values = self.nrpz.query(cmd).split(',')
#        print "Values:"
#        print values
#        print values[0]
        dB = MW2DBM( values[0] )
        sleep(.1)
        return dB
        
    def avgPower(self, samples=3):
        totalloss = 0
        for i in range(samples):
            loss = self.initIMM()
            print loss,", ",
            totalloss += loss
        avgloss = totalloss/samples
        print "avg ", avgloss
        return avgloss
            
    
    
    # set multiple setting commands
    def setmulti( self, cmd_list ):
        cmd = "SYST:TRAN:BEG"
        self.nrpz.write(cmd)
        for cmd in cmd_list:
            self.nrpz.write(cmd)
        cmd = "SYST:TRAN:END"
        self.nrpz.write(cmd)



def test():        
    # RSNRP::0x000c::100769:INSTR  
    #open the instrument session
    #NRPZ1 = visa.instrument ("RSNRP::0x000c::100759::INSTR")
    #NRPZ2 = visa.instrument ("RSNRP::0x000c::100760::INSTR")

    #reset the instrument
    #print NRPZ1.ask("*idn?")
    #print NRPZ2.ask("*idn?")

    #NRPZ1 = nrpz11("RSNRP::0x000c::100759::INSTR")
    NRPZ1 = nrpz11("RSNRP::0x000c::100760::INSTR", timeout=10)
    #NRPZ1 = nrpz11("USB::0x0aad::0x000c::100760")

    #help(NRPZ1)
    #print NRPZ1.interface_type
    #print NRPZ1.resource_class
    print NRPZ1.resource_name
    print NRPZ1.get_function()
    print NRPZ1.avgPower(samples=3)
    #for n in range(10):
    #    print NRPZ1.initIMM()
    #NRPZ1.calibrate()
    #print NRPZ1.getoffset()
    #NRPZ1.setoffset( 0)

    #print NRPZ1.getoffset()
    #print NRPZ1.getfreq()
    #NRPZ1.setfreq( 5800 )
    print NRPZ1.getfreq()
    #NRPZ1.setfreq( 5980)
    #print NRPZ1.getfreq()
    #NRPZ1.function("average")

#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    NRPZ1 = nrpz11("RSNRP::0x000c::103034::INSTR", timeout=10)
#    NRPZ1 = nrpz11("USB::0x0aad:0x00c::103034", timeout=10)
    NRPZ1.close()
    print NRPZ1.resource_name    
#    test()


