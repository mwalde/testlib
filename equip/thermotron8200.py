#! /usr/bin/env python
#

"""   
#====================================================================
#       Connect to the Thermotron 8200 controller via Telnet
#====================================================================
"""
import sys
import os
import telnetlib
from telnetlib import *
from time import *

__all__ = ["thermotron"]

THERMOTRON_PORT="8888"
DEFAULT_GPIB_ADDR="18"
PROMPT=""
DEFAULTIP="10.8.9.20"

class connectError(Exception): pass

class thermotron(Telnet):
    """ Telnet connection to ProLogix GPIB controller

    blah blah blah

    some more blah blahs
    """
    dbg = 0
    setTemp = None
    offsetTemp = None
    refresh_interval = 10
    soak_time = 10      # test soak time
    
    def __init__(self, host=DEFAULTIP ):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance.
        """
        Telnet.__init__(self, None)        
        self.sock = None
        if host is not None:
            self.connect( host )

    def connect(self, host):
        """Connect to a Thermotron controller.

         """
        
        self.host = host
        self.port = THERMOTRON_PORT
        self.telnet_timeout = 0.1
        try:
            self.open(self.host, self.port, self.telnet_timeout)

        except Exception, e:
            print "Failed to connect to %s" % host, e
            raise connectError('thermotron')


    def write_wait( self, cmd ):
        self.write(cmd + '\n')
        result = self.read_until( '\n' , 3.0 )
        return result

    def read_temp_chamber( self):
        return float(self.write_wait( 'PVAR1?').strip())
        
                         
    def read_temp_product( self):
        return float(self.write_wait( 'PVAR3?').strip())

    def read_humidity( self):
        return float(self.write_wait( 'PVAR2?').strip())

    def set_temp_chamber( self, temp):
        print "Chamber setpoint= %d" % temp
        self.setTemp = temp
        return self.write_wait( 'SETP1,%f' % temp).strip()
                         
    def set_humidity( self, relh ):
        return self.write_wait( 'SETP2,%f' % relh).strip()
                         
    def start( self ):
        return self.write_wait( 'RUNM' ).strip()

    def stop( self ):
        return self.write_wait( 'STOP' ).strip()

#====================================================================
#  test for chamber temp equal to the the current set point +- .5 degrees
#====================================================================

    def testTempChamber( self ):
        if abs( self.setTemp - self.read_temp_chamber()) <= .5 :
            return 1
        else:
            return False

    def waitTempChamber( self, soak_time=0):
        wait_time = 0
        while self.testTempChamber() == False:
            print "TempChamber wait: %dsec Chamber temp= %s Chamber setpoint= %f +- .5\r" % (wait_time, self.read_temp_chamber(), self.setTemp),
            sleep(self.refresh_interval)
            wait_time += self.refresh_interval
        print "\ntempChamber= %d" % self.read_temp_chamber()
        if soak_time:
            self.SoakTime( soak_time )
            
    def waitTempDUT( self, tempDUTfunction, offsetDUT, timeout=0 ):
        wait_time = 0
        while self.testTempDUT( tempDUTfunction, offsetDUT )== False:
            print "TempDUT wait: %dsec tempDUT= %d C Chamber setpoint= %f  DUT setpoint= %d +-2\r" % (wait_time, os.system(tempDUTfunction), self.setTemp, self.setTemp+offsetDUT),
            sleep(self.refresh_interval)
            wait_time += self.refresh_interval
        print "\nTempDUT= %s" % os.system(tempDUTfunction)
            
#====================================================================
#  test for DUT temp equal to the the current set point + 
#  the DUT offset +- 2 degrees 
#  external function tempDUTfunction return the temperature of the DUT
#====================================================================
    def testTempDUT( self, tempDUTfunction, offsetDUT ):
        tempDUT = os.system(tempDUTfunction)
#        print "setTemp==%s + offset - tempDUT==%f" % (self.setTemp, self.setTemp + offsetDUT - tempDUT)
#        print self.read_temp_chamber()
        if abs( self.setTemp + offsetDUT - tempDUT) <= 2 :
            return 1
        else:
            return False

    def SoakTime( self, minutes ):
        for elapsed in range(0,minutes):
            print 'Time Remaining %2d minutes\r' % (minutes - elapsed),
            sleep(60)
        print 
        print 'Soak Time Complete'
            


    def __del__(self):
        """Destructor -- close the connection."""
        self.close()

#====================================================================
#       test
#====================================================================
def test():
    """ Test program for Thermotron telnet session

    """
    debuglevel = 0
    try:
       therm = thermotron()
    except connectError , e:
        print e, 'Connection to host %s failed' % host
    else:
        therm.set_debuglevel(debuglevel)
        
        print 'Chamber temp %s C' % therm.read_temp_chamber()
        print 'Product temp %s C' % therm.read_temp_product()
        print 'Relative Humidity %s %%' % therm.read_humidity()


        therm.interact()
        
    print '+++ close +++'
    therm.close()

#====================================================================


if __name__ == '__main__':
    test()
