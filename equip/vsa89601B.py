#====================================================================
#           Agilent PXA 89601B Vector Spectrum Analyzer
#====================================================================
from math import pow,log10,sqrt
from time import *
from telnetlib import *

__all__ = ["vsa89601B"]

IP_PORT = 5024
DEFAULT_IP = '10.8.9.13'
PROMPT = 'SCPI> '

class VSA_Error(Exception):
    def __init__(self, value):
        self.parameter = 'VSA_Error: ' + value
    def __str__(self):
        return repr(self.parameter)

sbyte=lambda n:(255 & n^128)-128 # returns the signed int of an 8-bit
                                 # a fix for the temp(erature) script

EVM2dB    = lambda val: 20 * log10((float(val)/100))
IQOff2dB  = lambda val: 10 * log10(float(val))
IQGain2dB = lambda val: 20 * log10(float(val))

DBM2VOLTS = lambda DBM: sqrt(pow(10,(float(DBM)/10))/10)
VOLTS2DBM = lambda volts: 10 * log10(10 * (float(volts) ** 2))

class vsa89601B(Telnet):
    """ Telnet connection to Agilent PXA 89601B Vector Spectrum Analyzer
    """
    ErrorSummary =[]
    debug = False
    
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
        """Connect to a Agilent PXA 89601B Vector Spectrum Analyzer
         """
        self.host = host
        self.port = IP_PORT
        self.telnet_timeout = 5.0
        self.attempts = 5
        self.openOK = False
        self.ready = False
        
        while self.attempts:
            try:
                self.open(self.host, self.port, self.telnet_timeout)
                self.openOK = True
                break;
                
            except Exception, e:
                print "Retry %d connect to %s" % (self.attempts, host)
                self.attempts-=1

        if self.openOK:
            results = self.read_very_lazy()   # clear Telnet ACK/NAK junk
            print '+++ vsa8961B +++ %s' % results
            self.write_cmd_response('*IDN?', 5)
            response = self.write_cmd_response(':SYST:VSA:STAR?', 10)
            if response == '1':
                print 'VSA app is loaded'
            else:
                print 'Loading VSA app ...'
                self.write_cmd_OPC(":SYST:VSA:STAR", 120)           

                self.write_cmd(':DISP:ENAB 1')
                self.write_cmd(':DISP:ANN:TITL:DATA "I/Q Calibration"')
#                print "loading setup..."
#                self.write_cmd(':MMEM:LOAD:SET "d:\Martys_Setup.setx"')
#                self.write_cmd(':INIT:REST')

            response = self.write_cmd_response(':SYST:VSA:STAR?', 10)
            print response
            if response == '1':
                response = self.write_cmd_response('*IDN?', 20)
                print "Connected: %s" % response
                self.ready = True
                return True
            else:
                print 'VSA app load has failed'
                return False


    #====================================================================
    #           SCPI command write 
    #====================================================================
    def flush(self):
        rsp = " "  # dummy response for first time
        while len(rsp):
            rsp = self.read_until(PROMPT, 1)
            if len(rsp) and self.debug:
                print "flush : ", rsp
#            for character in rsp:
#                print '> ', character.encode('hex')        

    def write_cmd( self, cmd ):
        self.flush()
        if self.debug: print cmd
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
#        raise VSA_Error("OPC timeout cmd=:%s" % cmd)
#        print 'write_cmd_OPC( %s ) timeout=%d error' % (cmd, timeout)
#        print 'results=%s' % results
        return False
#        self.mt_interact()

    def write_cmd_response( self, cmd, timeout=1 ):
        self.write_cmd( cmd )
        response = self.read_until('\n', timeout)
        self.flush()
        response = response.strip()
        if response == '':
            print 'write_cmd_response( %s ) == %s timeout=%d error' % (cmd,response,timeout)
        return response

    def wait_response(self, match, timeout=1 ):
        response = self.read_until(match, timeout)
        self.flush()
        response = response.strip()
        if response == '':
            print 'wait_response( %s ) == %s timeout=%d error' % (match,response,timeout)
        return response
    
    #====================================================================
    #           Initialize the Agilent PXA 89601B Vector Spectrum Analyzer
    #====================================================================
    #  return True on success False on load failure Timeout
    def loadSetupFile( self, setupconfigdir, setupfile, setuptitle ):
        self.write_cmd(':DISP:ENAB 1')
        self.write_cmd(':DISP:ANN:TITL:DATA "%s"' % setuptitle)
        print "loading setup...   %s" % (setupfile)
        return self.write_cmd_OPC(':MMEM:LOAD:SET "%s%s"' % (setupconfigdir,setupfile),30)

    def loadSetupFileImmediate( self, setupconfigdir, setupfile, setuptitle ):
        self.write_cmd(':DISP:ENAB 1')
        self.write_cmd(':DISP:ANN:TITL:DATA "%s"' % setuptitle)
        print "loading setup...   %s" % (setupfile)
        return self.write_cmd(':MMEM:LOAD:SET "%s%s"' % (setupconfigdir,setupfile))


    def runCalibration(self, status=None):
        print 'VSA Calibration...',
        self.write_cmd(":CAL:AUTO 1")
        self.write_cmd_response(':CAL:AUTO?')
        while 1:
            if status:
                status("Calibrating")
            sleep(2)
            if self.CalStatus() == 'OK':
                if status:
                    status("Calibration Complete")
                print "\nComplete"
                self.write_cmd(':CALibration:AUTO 0')
                break;
            else:
                print '.',

    def CalAutoOff(self):
        self.write_cmd(':CALibration:AUTO 0')

    def CalAutoOn(self):
        self.write_cmd(':CALibration:AUTO 1')
        
        
    def CalStatus(self):
        self.write_cmd(":CAL:MESS?")
        calstatus = self.wait_response('"\n', timeout=2)
        calstatus = calstatus.replace('"','')
        calstatus = calstatus.upper()
#        print "CalStatus=%s" % calstatus
        return calstatus
        
        
    def getTxPWR( self ):
        pwr = self.write_cmd_response(':TRAC2:MARK1:Band:POW?',20)
        return float(pwr)

    # retry Error Summary read if full 60 element summary not retreived
    def getOFDMErrorSummary( self ):
        self.__readOFDMErrorSummary()
        if len(self.ErrorSummary) < 60:
            self.__readOFDMErrorSummary()
            print "__readOFDMErrorSummary() retry"
        

    def __readOFDMErrorSummary( self ):
        response = self.write_cmd_response(':TRACe4:DATA:TABLe:VALUE?',20)
        self.ErrorSummary = response.split(',')
        
    def getIQOffset( self, getsummary=1 ):
        if getsummary: self.getOFDMErrorSummary()
        return (IQOff2dB(self.ErrorSummary[45]), EVM2dB(self.ErrorSummary[0]))
        
    def getIQQuadErr( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return float(self.ErrorSummary[50])
        
    def getIQGainlmb( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return IQGain2dB(self.ErrorSummary[55])
        
    def getEVMPeak( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return EVM2dB(self.ErrorSummary[5])

    def getEVM( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return EVM2dB(self.ErrorSummary[0])

    def getEVMPilot( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return EVM2dB(self.ErrorSummary[10])

    def getEVMData( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return EVM2dB(self.ErrorSummary[15])

    def getEVMPreamble( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
#        self.getOFDMErrorSummary()
        return EVM2dB(self.ErrorSummary[20])

    def getFreqErr( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return float(self.ErrorSummary[29])

    def getSymbolClkErr( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return float(self.ErrorSummary[30])

    def getCPE( self, getsummary=1  ):
        if getsummary: self.getOFDMErrorSummary()
        return float(self.ErrorSummary[35])

#   return True if restart ok False if timeout   
    def initiateRestart( self, timeout=20 ):
#        self.write_cmd_OPC("*RST")
        return self.write_cmd_OPC(":INIT:IMM", timeout)
#        self.write_cmd_OPC("*RST")
#        sleep(2)        

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
            
    #====================================================================
    #    
    #====================================================================
    def measure_status(self, timeout=4):
        status = self.write_cmd_response(':MEAS:STAT?', timeout=timeout)
#        print status, hex(int(status))
        try:
            stat_int = int(status)
        except:
            print "VSA measure status timeout"
            stat_int = 0
        return stat_int
    
    def auto_range( self, timeout=4):
        self.write_cmd(":INP:ANAL:RANG:AUTO")
        for t in range(timeout):
            status = self.measure_status()
            if status & 0x80000000 == 0:
                return True
            sleep(1)
        return False

    def over_range( self ):
        status = self.measure_status()
        if status & 0x200000:
            return True
        else:
            return False
        
    def freq_center( self, freq_str):
        self.write_cmd(":SENS:FREQ:CENTER %s" % freq_str)
        
    def freq_marker( self, freq_str):
        self.write_cmd(":TRACE2:MARKER1:X %s" % freq_str)
        
    def read_freq_center( self ):
        rsp = self.write_cmd_response(":SENS:FREQ:CENTER? DEFAULT", timeout = 2)
        return rsp
        
    def freq_span( self, freq_str):
        print "freq_span"
        self.write_cmd(":SENS:FREQ:SPAN %s" % freq_str)
        
    def read_freq_span( self ):
        rsp = self.write_cmd_response(":SENS:FREQ:SPAN?", timeout = 2)
        return rsp
        
    def display_title( self, title_str ):
        self.write_cmd(':DISP:ANN:TITL:DATA "%s"' % title_str)
        
    #====================================================================
    #    Read and write VSA Analog range
    #====================================================================
    def read_analog_range( self ):
        volts = self.write_cmd_response(':INP:ANAL:RANGE?')
        dB = VOLTS2DBM(volts)
        return dB
        
    def write_analog_range( self, dB, timeout=4 ):
        volts = DBM2VOLTS( dB )
        cmd = ':INP:ANAL:RANGE %f' % volts
        self.write_cmd_OPC(cmd, 20)
                
def convert_test():
    data = [\
        '6.64931058883667','***','***','***','6.64931058883667',\
        '26.2495651245117','***','***','***','26.2495651245117',\
        '6.59683752059937','***','***','***','6.59683752059937',\
        '6.66229724884033','***','***','***','6.66229724884033',\
        '3.33431601524353','***','***','***','3.33431601524353',\
        '***','***','***','***','735434.434932927',\
        '3.05105895677116E-05','***','***','***','3.05105895677116E-05',\
        '27.1523303985596','***','***','***','27.1523303985596',\
        '***','***','***','***','0.986548732683209',\
        '0.000206878932658583','***','***','***','0.000206878932658583',\
        '0.0425050184130669','***','***','***','0.0425050184130669',\
        '0.99920380115509','***','***','***','0.99920380115509' \
        ]
    print len(data)
    printErrorSummary( data )

def printErrorSummary( data ):
    print "EVM       %0.3f  from %s" % (EVM2dB(data[0]), data[0])
    print "EVMPeak   %0.3f  from %s" % (EVM2dB(data[5]), data[5])
    print "PilotEVM  %0.3f  from %s" % (EVM2dB(data[10]), data[10])
    print "DataEVM   %0.3f  from %s" % (EVM2dB(data[15]), data[15])
    print "PmblEVM   %0.3f  from %s" % (EVM2dB(data[20]), data[20])
    print "IQOffset  %0.3f  from %s" % (IQOff2dB(data[45]), data[45])
    print "IQQuadErr %0.5f  from %s" % (float(data[50]), data[50])
    print "IQGainlmb %0.4f  from %s" % (IQGain2dB(data[55]), data[55])
   
def test():
    vsa = vsa89601B(DEFAULT_IP)
    vsa.debug = False
    if vsa.ready:
        print vsa.write_cmd_response('*IDN?', 5)
        while 1:
            cmd = raw_input('XCPI> ')
            if cmd == 'x' or cmd == 'X':
                break
            print vsa.write_cmd_response(cmd, 5)

        for n in range(10):
            print "test ", n
            freq = vsa.read_freq_center()
            print freq
            vsa.freq_center("5.34GHz")
            print vsa.read_freq_center()
            vsa.freq_center(freq)
            
            span = vsa.read_freq_span()
            print span
            vsa.freq_span("140MHz")
            print vsa.read_freq_span()

            
            vsa.freq_span(span)
            
            vsa.auto_range()
            orig = vsa.read_analog_range()
            print orig
    #        vsa.write_analog_range( 0 )
#        print vsa.read_analog_range()
#        print vsa.over_range()
#        vsa.auto_range(  )
#        print vsa.read_analog_range()
#        print vsa.over_range()

      
#        vsa.loadSetupFile('D:/Users/Instrument/Documents/Agilent/custom-ofdm-data/Reference Custom ODFM Configs/Factory_VSA_Cal_112213/', 'TX0_FACTORY_CAL_5480MHz.setx','TX0_FACTORY_CAL_5480MHz.setx')
#        vsa.loadSetupFile('D:/', 'marty.setx','marty.setx')
#        print "TxPWR : ",vsa.getTxPWR()
#        vsa.initiateRestart( 120 )        
#        print "TxPWR : ",vsa.getTxPWR()
#        print "getEVM : ",vsa.getEVM()
#        vsa.mt_interact()
    vsa.close()
    

 
if __name__ == '__main__':
    test()
 
