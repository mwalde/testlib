#====================================================================
#           Agilent E8267D Signal Generator
#====================================================================
from time import *
from telnetlib import *

__all__ = ["sgE8267D"]

IP_PORT = 5025
DEFAULT_IP = '10.8.9.11'

class sgE8267D(Telnet):
    """ Telnet connection to Agilent E8267D Signal Generator
    """
    
    def __init__(self, host ):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance.
        """
        Telnet.__init__(self, None)        
        self.sock = None
        
        if host is not None:
            self.connect( host )

    def connect(self, host):
        """Connect to a Agilent E8267D Signal Generator
         """
        self.host = host
        self.port = IP_PORT
        self.telnet_timeout = 0.1
        try:
            self.open(self.host, self.port, self.telnet_timeout)
            self.read_very_lazy()   # clear Telnet ACK/NAK junk
            print '+++ sgE8267D +++'
            
        except Exception, e:
            print "Failed to connect to Agilent E8267D Signal Generator ip=%s" % host, e
            raise connectError('E8267D')

    #====================================================================
    #           Initialize the Agilent E8267D Signal Generator
    #====================================================================

    def initSigGen(self, freq, ampl):
        print 'freq %s  ampl %s' % (freq, ampl)
        
        self.write(':FREQ %sGHZ\n' % freq)  # Set Frequency

        self.write(':POW %sDBM\n' % str(ampl)) # Set Amplitude

        self.write(':DM:STAT ON\n')         # Enable the internal I/Q modulator
        
#        print "Calibrating..."
#        self.write(':CAL:IQ:DC\n')          # Perform I/Q Calibration at DC
        
        self.waitOPC()
        
        self.write(':OUTP on\n')               # Enable RF output
              
        self.write(':OUTP:MOD on\n')           # Enable Modulation output
       
    def runCalibration( self ):
            print "Sig Gen Calibrating..."
            self.write(':CAL:IQ:DC\n')          # Perform I/Q Calibration at DC

    def waitOPC(self):
        """ wait for OPeration Complete
        """
        self.write('*OPC?\n')               # Returns "1\n" when operation complete
        
        results = self.read_until('1\n', 10) # wait upto 10 seconds
        if results != '1\n': print 'waitOPC() timeout error'
            
    def getPowerOffset( self ):
        self.write(':POW:OFFSet?\n')
        resp = self.read_until('\n', 10)
        print resp

    def setPowerOffset( self, Db ):
        print "setPowerOffest %s" % Db
        self.write(':POW:OFFSet %s\n' % Db)


    def setPOWer( self, ampl):
        self.write(':POW %sDBM\n' % str(ampl))        
        
    def setFREQ( self, freq ):
        self.write(':FREQ %sGHZ\n' % freq)  # Set Frequency

    def rclPreset( self, preset ):
        self.write('*RCL %s\n' % preset )
        
    def setMODoff( self ):
        self.write(':OUTP:MOD:STAT OFF\n')
        
    def setMODon( self ):
        self.write(':OUTP:MOD:STAT ON\n')

    def enableRF( self ):
        self.write(':OUTP on\n')               # Enable RF output

    def disableRF( self ):
        self.write(':OUTP off\n')              # Disable RF output
        

def test():
	sg = sgE8267D(DEFAULT_IP)
#	sg.getPowerOffset()
	sg.setPowerOffset(-17.68)
#	sg.getPowerOffset()
	sg.initSigGen( 24.1, -40)
	sg.close() 

if __name__ == '__main__':
    test()
 