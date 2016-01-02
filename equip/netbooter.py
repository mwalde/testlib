#! /usr/bin/env python
#

"""   
#====================================================================
#       Connect to the Synaccess NetBooter via Telnet
#====================================================================
"""
import sys
import telnetlib
from telnetlib import *
from time import sleep

__all__ = ["netBooter"]

PROMPT=">"
DEFAULTIP="10.8.9.157"

class connectError(Exception): pass

class netBooter(Telnet):
    """ Telnet connection to netBooter
    blah blah blah

    some more blah blahs
    """
    dbg = 0
    
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
        """Connect to a netBooter controller.

         """
        
        self.host = host
        self.port = 23
        self.telnet_timeout = 0.1
        try:
            self.open(self.host, self.port, self.telnet_timeout)
            print " +++ netBooter +++ %s" % host
            self.read_until( PROMPT , 3.0 )
            sleep(1)  
            self.read_until( PROMPT , 3.0 )

        except Exception, e:
            print "Failed to connect to %s" % host, e
            raise connectError('netbooter')


    def write_wait( self, cmd ):
        self.write(cmd + '\r')
        result = self.read_until( PROMPT , 3.0 )
        return result

    def pset( self, outlet, on_off):
#        print "pset %d %d" % ( outlet, on_off )
        return self.write_wait( 'pset %d %d' % ( outlet, on_off ))
                         
    def OneOn( self ):
        self.pset( 1, 1 )

    def OneOff( self ):
        self.pset( 1, 0 )

    def OneReboot( self ):
        self.pset( 1, 0 )
        sleep(1)
        self.pset( 1, 1 )
        
    def TwoOn( self ):
        self.pset( 2, 1 )

    def TwoOff( self ):
        self.pset( 2, 0 )

    def TwoReboot( self ):
        self.pset( 2, 0 )
        sleep(1)
        self.pset( 2, 1 )

def test():
    """ Test program for Thermotron telnet session

    """
    debuglevel = 0
    while sys.argv[1:] and sys.argv[1] == '-d':
        debuglevel = debuglevel+1
        del sys.argv[1]
    host = DEFAULTIP
    therm = None
    if sys.argv[1:]:
        host = sys.argv[1]
    try:
       power = netBooter(host)
    except connectError , e:
        print e, 'Connection to host %s failed' % host
    else:
        power.set_debuglevel(debuglevel)
        power.OneReboot()
        power.pset( 2, 1)
        sleep(1)
        power.pset( 2, 0)
        sleep(1)
        power.pset( 2, 1)
        power.TwoReboot()
        
#        power.interact()
        
    print '+++ close +++'
    power.close()

#====================================================================


if __name__ == '__main__':
    test()
