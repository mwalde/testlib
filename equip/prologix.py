#! /usr/bin/env python
#

"""   
#====================================================================
#       Connect to the ProLogix GPIB controller via Telnet
#====================================================================
"""
import sys
import telnetlib
from telnetlib import *
from time import *

__all__ = ["prologix"]

PROLOGIX_PORT="1234"
DEFAULT_GPIB_ADDR="25"
PROMPT=""
DEFAULTIP="192.168.1.158"

class connectError(Exception): pass

#class KeyboardInterrupt(Exception): pass

class prologix(Telnet):
    """ Telnet connection to ProLogix GPIB controller

    blah blah blah

    some more blah blahs
    """
    dbg = 0
    
    def __init__(self, host=DEFAULTIP, addr=DEFAULT_GPIB_ADDR ):
        """Constructor.

        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance.
        """
        Telnet.__init__(self, None)        
        self.sock = None
        if host is not None:
            try:
                self.connect( host, addr )
            except:
                print "second attempt to connect to %s" % host
                self.connect( host, addr )

    def connect(self, host, addr):
        """Connect to a prologix GPIB controller.

         """
        
        self.host = host
        self.addr = addr
        self.port = PROLOGIX_PORT
        self.telnet_timeout = 0.1
        try:
            self.open(self.host, self.port, self.telnet_timeout)
            self.write("++clr\n")
            self.write("++mode 1\n")
            self.write("++auto 1\n")
            self.write("++eos 2\n")
            self.write("++eoi 1\n")
            self.write("++eot_char 42\n")
            self.write("++eot_enable 1\n")
            GPIB_tmo=int(3000);
            self.set_GPIB_timeout( GPIB_tmo )
            self.write("\n")
            self.read_until("Unrecognized command\n", 1) # clear telnet open negoiation response
            self.write("++addr " + self.addr + "\n");

        except Exception, e:
            print "Retry 1 connect to %s" % host, e
            try:
                self.open(self.host, self.port, self.telnet_timeout)
                self.write("++clr\n")
                self.write("++mode 1\n")
                self.write("++auto 1\n")
                self.write("++eos 2\n")
                self.write("++eoi 1\n")
                self.write("++eot_char 42\n")
                self.write("++eot_enable 1\n")
                GPIB_tmo=int(3000);
                self.set_GPIB_timeout( GPIB_tmo )
                self.write("\n")
                self.read_until("Unrecognized command\n", 1) # clear telnet open negoiation response
                self.write("++addr " + self.addr + "\n");

            except Exception, e:
                print "Retry 2 connect to %s" % host, e
                try:
                    self.open(self.host, self.port, self.telnet_timeout)
                    self.write("++clr\n")
                    self.write("++mode 1\n")
                    self.write("++auto 1\n")
                    self.write("++eos 2\n")
                    self.write("++eoi 1\n")
                    self.write("++eot_char 42\n")
                    self.write("++eot_enable 1\n")
                    GPIB_tmo=int(3000);
                    self.set_GPIB_timeout( GPIB_tmo )
                    self.write("\n")
                    self.read_until("Unrecognized command\n", 1) # clear telnet open negoiation response
                    self.write("++addr " + self.addr + "\n");
                except Exception, e:
                    print "Retry 3 connect to %s" % host, e









                pass
#               raise connectError('prologix')

    def set_addr(self, addr):
        self.addr = addr
        self.write("++addr " + self.addr + "\n");

    def set_GPIB_timeout(self, timeout ):
        """ Set GPIB read and telnet timeouts
        """
        if self.dbg ==1:
            print 'set GPIB timeout %s' %timeout
        data = '++read_tmo_ms '+str(timeout)
        if self.dbg ==1:
            print "data = %s" % data
        self.write( data );

    def clear( self ):
        """ send (SDC) Send Device Clear to current addressed device
        """
        self.write("++clr\n");
        sleep(5)

    def read_eoi(self):
        self.write("++read eoi\n");
#        sleep(.5)
        try:
            result = self.read_until( "*", 3.0);


        except Exception, e:
            print "read_eoi timeout %s" % e
            result = None

        return result;

    def write_delay(self, cmd, delay=0):
        """ write command then delay before returning. No results are read.
        """
        print "write_delay(%s, %s)" %  (cmd.strip('\n'), delay)
        self.write(cmd)
        sleep(delay)
       
    def write_eoi(self, cmd, delay=0):
        """ write command and wait for an eoi response with timeout
        """
        print "write_eoi(%s, %s)" %  (cmd.strip('\n'), delay)
        self.write(cmd)
        sleep(delay)
        result = self.read_eoi()
        print "result=%s" % result
        return result
    
    def write_eoi_wait(self, cmd, delay=0):
        """ write command and wait for an eoi response forever
        """
        if self.dbg == 1:
            print "write_eoi_wait(%s, %s)" %  (cmd.strip('\n'), delay)
        self.write(cmd)
        sleep(delay)
        result = self.read_eoi_wait()
        if self.dbg ==1:
            print "result=%s" % result
        return result

    def read_eoi_wait(self):
        result = ''
        while result == '':
            self.write("++read eoi\n");
#            sleep(.5)
            result = self.read_until( "*", 3.0);

        return result;

    def close(self):       
#        self.write("++auto 0\n")       # if you don't do this the next telnet open will fail
        Telnet.close(self)
        
    def __del__(self):
        """Destructor -- close the connection."""
        print "Prologix __del__"
#        self.close()

def test():
    """ Test program for defiant telnet session

    """
    debuglevel = 0
    while sys.argv[1:] and sys.argv[1] == '-d':
        debuglevel = debuglevel+1
        del sys.argv[1]
    host = DEFAULTIP
    pf = None
    if sys.argv[1:]:
        host = sys.argv[1]
    try:
        pf = prologix(host)
    except connectError , e:
        print e, 'Connection to host %s failed' % host
    else:
        pf.set_debuglevel(debuglevel)
        pf.interact()
        print '+++ close +++'
        pf.close()

#====================================================================


if __name__ == '__main__':
    test()
