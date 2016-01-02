#! /usr/bin/env python
#

"""   
#====================================================================
#       Connect to HP 11713A Attenuator/Switch Driver via the
#       ProLogix GPIB controller via Telnet
#====================================================================
"""
import sys
import telnetlib
from telnetlib import *
from time import *
from prologix import *
__all__ = ["hp11713A"]

PROLOGIX_PORT="1234"
GPIB_ADDR0="25"
GPIB_ADDR1="26"
PROMPT=""
DEFAULTIP="10.8.9.191"

class connectError(Exception): pass

class hp11713A(prologix):
    """ Telnet connection to ProLogix GPIB controller

    blah blah blah

    some more blah blahs
    """
    dbg = 0
    
    def __init__(self, host=DEFAULTIP, addr=GPIB_ADDR0 ):
        """Constructor.
        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance.
        """
        print '+++ hp11713A %s %s +++' % ( host, addr )
        prologix.__init__(self, host, addr)

    def SwitchOn( self, n ):
        self.set_addr(GPIB_ADDR0)
        self.write("A%d\n" % n)
        sleep(.5)

    def SwitchOff( self, n ):
        self.set_addr(GPIB_ADDR0)
        self.write("B%d\n" % n)
        sleep(.5)

    def SwitchOn9( self ):
        self.set_addr(GPIB_ADDR0)
        self.write("A9\n")
        sleep(.5)

    def SwitchOff9( self ):
        self.set_addr(GPIB_ADDR0)
        self.write( "B9\n")
        sleep(.5)
        
    def SwitchOn0( self ):
        self.set_addr(GPIB_ADDR0)
        self.write("A0\n")
        sleep(.5)

    def SwitchOff0( self ):
        self.set_addr(GPIB_ADDR0)
        self.write( "B0\n")
        sleep(.5)

#   2nd hp11713A        
    def SwitchOn_1( self, n ):
        self.set_addr(GPIB_ADDR1)
        self.write("A%d\n" % n)
        sleep(.5)

    def SwitchOff_1( self, n ):
        self.set_addr(GPIB_ADDR1)
        self.write("B%d\n" % n)
        sleep(.5)

    def SwitchOn9_1( self ):
        self.set_addr(GPIB_ADDR1)
        self.write("A9\n")
        sleep(.5)

    def SwitchOff9_1( self ):
        self.set_addr(GPIB_ADDR1)
        self.write( "B9\n")
        sleep(.5)
        
    def SwitchOn0_1( self ):
        self.set_addr(GPIB_ADDR1)
        self.write("A0\n")
        sleep(.5)

    def SwitchOff0_1( self ):
        self.set_addr(GPIB_ADDR1)
        self.write( "B0\n")
        sleep(.5)
    
    def close( self ):
        self.write("CLR\n")
    
    def __del__(self):
        """Destructor -- close the connection."""
        self.close()


def test():
    """ Test program for defiant telnet session

    """
    debuglevel = 0
    while sys.argv[1:] and sys.argv[1] == '-d':
        debuglevel = debuglevel+1
        del sys.argv[1]
    host = DEFAULTIP
    sa = None
    if sys.argv[1:]:
        host = sys.argv[1]
    try:
        switch = hp11713A(host)
    except connectError , e:
        print e, 'Connection to host %s failed' % host
    else:
#        switch.interact()
        switch.set_debuglevel(debuglevel)
        i = 10
        while i > 0:
            switch.SwitchOn9()
            sleep(1)
            switch.SwitchOn0()
            sleep(1)
            switch.SwitchOn9_1()
            sleep(1)
            switch.SwitchOn0_1()
            sleep(1)
            switch.SwitchOff9()
            sleep(1)
            switch.SwitchOff0()
            sleep(1)
            switch.SwitchOff9_1()
            sleep(1)
            switch.SwitchOff0_1()
            sleep(1)
            i = i - 1

#        switch.interact()

    print '+++ close +++'
    switch.close()

#====================================================================


if __name__ == '__main__':
    test()
