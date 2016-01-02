#====================================================================
#           Agilent PXA 89601B Vector Spectrum Analyzer
#====================================================================
from math import *
from time import *
from telnetlib import *

__all__ = ["saN9030A"]

IP_PORT = 5023
DEFAULT_IP = '10.8.9.13'



sbyte=lambda n:(255 & n^128)-128 # returns the signed int of an 8-bit
                                 # a fix for the temp(erature) script

EVM2dB    = lambda val: 20 * log10((float(val)/100))
IQOff2dB  = lambda val: 10 * log10(float(val))
IQGain2dB = lambda val: 20 * log10(float(val))


class saN9030A(Telnet):
    """ Telnet connection to Agilent SA N9030A Spectrum Analyzer
    """
    ErrorSummary =[]
    PROMPT = 'SCPI> '    
    
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
        """Connect to a Agilent SA N9030A Spectrum Analyzer
         """
        self.host = host
        self.port = IP_PORT
        self.telnet_timeout = 5.0
        try:
            self.open(self.host, IP_PORT, self.telnet_timeout)
#            results = self.read_very_lazy()   # clear Telnet ACK/NAK junk
            response = self.read_until(self.PROMPT, 5)
            print '+++ saN9030A +++ %s' % response

            response = self.write_wait('*IDN?', 20)
            print "Connected: %s" % response
            
             
        except Exception, e:
            print "Failed to connect to Agilent PXA 89601B Vector Spectrum Analyzer ip=%s" % host, e
#            raise connectError('vsa8961B')

    #====================================================================
    #           write_wait() write cmd and wait for a response and
    #           strip off command and prompt from response string
    #====================================================================
    def write_wait( self, cmd, timeout = 4 ):
        """ Write command to the radio and wait for a prompt
            strip off the command echo and the cmd prompt
            return only result of the operation
        """
        print cmd
        cmd = cmd.strip('\n')       # remove any newline
        self.write( cmd + '\n' )
        result = self.read_until(self.PROMPT, timeout)
        result = result.strip( cmd )
        result = result.strip( self.PROMPT )
        result = result.rstrip()
        return result;
    
    def wait_rsp( self, timeout=2 ):
        rsp = self.read_until(self.PROMPT, timeout)
#        print rsp
    #====================================================================
    #           SCPI command write 
    #====================================================================
    def flush(self):
        rsp = self.read_until('gagme', 1)

    def write_cmd( self, cmd ):
        self.write( cmd + '\n' )

    def write_cmd_OPC( self, cmd, timeout=10):
        if len(cmd):
            self.write_cmd(cmd +';*OPC?')
        else:
            self.write_cmd('*OPC?')
        results = self.read_until('1', timeout)
        self.flush()
        if '1' in results:
            return True
        print 'write_cmd_OPC( %s ) timeout=%d error' % (cmd, timeout)
        print 'results=%s' % results
        return False

    def write_cmd_response( self, cmd, timeout=1 ):
        self.write_cmd( cmd )
        response = self.read_until(self.PROMPT, timeout)
        response = response.strip()
        if response == '':
            print 'write_cmd_response( %s ) == %s timeout=%d error' % (cmd,response,timeout)
        return response
        
    #====================================================================
    #           Initialize the Agilent N9030 Spectrum Analyzer
    #====================================================================

    def setCenterFREQ(self, freq ):
        self.write_wait('FREQ:CENTER %f' % (freq * 1000000))
#        sleep(1)
        
    def setSPAN(self, span):
        self.write_wait('FREQ:SPAN %f' % (span * 1000))
#        sleep(1)
        
    def peakSearch(self):
        rsp = self.write_cmd_OPC('POW:PCEN')
        print rsp
#        sleep(.5)
        rsp = self.write_wait('CALC:MARK1:Y?')
#        print rsp
        return float(rsp)
        
    def CalAutoOff(self):
        print "CalAutoOff()"
        self.write_cmd(':CALibration:AUTO OFF')

    def CalAutoOn(self):
        print "CalAutoOn()"
        rsp = self.write_cmd_OPC(':CALibration:AUTO ON', timeout=40)
        
        
    #====================================================================
    #           Initialize the Agilent PXA 89601B Vector Spectrum Analyzer
    #====================================================================

    def initSigGen(self, freq, span):
        print 'freq %s  ampl %s' % (freq, ampl)
        
        self.write_wait(':FREQ:CENT %sGHZ' % freq)  # Set Center Frequency

        self.write_wait(':SPEC:FREQ:SPAN %s' % span)
        
    def waitOPC(self, timeout=10):
        """ wait for OPeration Complete
        """
        self.write('*OPC?\n')               # Returns "1\n" when operation complete
        
        results = self.read_until('1\n', timeout) # wait upto 10 seconds
        if results != '1\n': 
            print 'waitOPC() timeout error'
            print 'results=%s' % results
            vsa.mt_interact()
            
            
  
def test():
    sa = saN9030A(DEFAULT_IP)
    sa.setCenterFREQ( 5800 )
    sa.setSPAN( 100 )
    rsp = sa.peakSearch()
    print rsp
#    sa.mt_interact()
    sleep(2)
    sa.close()
    
    
if __name__ == '__main__':
    test()
 
