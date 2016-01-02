#! /usr/bin/env python
#

"""   
#====================================================================
#       Connect to HP 6622A Power Supply via the
#       ProLogix GPIB controller via Telnet
#====================================================================
"""
import sys
import telnetlib
from telnetlib import *
from time import *
from prologix import *
__all__ = ["hp6622A"]

PROLOGIX_PORT="1234"
DEFAULT_GPIB_ADDR="5"
PROMPT=""
DEFAULTIP="192.168.1.191"

class connectError(Exception): pass

class hp6622A(prologix):
    dbg = 0
    
    def __init__(self, host=DEFAULTIP, addr=DEFAULT_GPIB_ADDR ):
        """Constructor.
        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance.
        """
        prologix.__init__(self, host, addr)
        print '+++ hp6622A IP:%s GPIB:%s +++' % ( host, addr )
        self.write("++auto 0\n")
        self.write("++eos 3\n")

    # Send a query command and wait for a response
    def query( self, cmd ):
        self.write(cmd)
        self.read_eoi_wait()
        result = self.read_eoi_wait()
        result = result.strip('*\n')
        if self.dbg > 0:
            print( "%s = %s\n" % (cmd.strip('\n'), result))
        return result

    # Issue a command and do not wait for a response
    def issue( self, cmd ):
        self.write(cmd)
        if self.dbg > 0:
            print( "%s" % (cmd))

    # Voltage Set 
    def VSET(self, channel, volt_str ):
        cmd = "VSET %s,%s\n" % (channel, volt_str)
        self.issue(cmd)

    # Voltage Set query
    def VSETQ(self, channel ):
        cmd = "VSET? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Voltage Output query
    def VOUTQ(self, channel ):
        cmd = "VOUT? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Current Set
    def ISET(self, channel, amps_str ):
        cmd = "ISET %s,%s\n" % (channel, amps_str)
        self.issue(cmd)

    # Current Set query
    def ISETQ(self, channel ):
        cmd = "ISET? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Output ON/Off
    def OUT(self, channel, on_off ):
        cmd = "OUT %s,%s\n" % (channel, on_off)
        self.issue(cmd)

    # Output ON/OFF query
    def OUTQ(self, channel ):
        cmd = "OUT? %s\n" % (channel)
        result = self.query(cmd)
        return result
    
    # Actual current output
    def IOUTQ(self, channel ):
        cmd = "IOUT? %s\n" % (channel)
        result = self.query(cmd)
        return result
    
    # Over Voltage Set
    def OVSET(self, channel, volt_str ):
        cmd = "OVSET %s,%s\n" % (channel, volt_str)
        self.issue(cmd)

    # Over Voltage Set query
    def OVSETQ(self, channel ):
        cmd = "OVSET? %s\n" % (channel)
        result = self.query(cmd)
        return result
     
    # Over Voltage Reset
    def OVRST(self, channel):
        cmd = "OVRST %s\n" % (channel)
        self.issue(cmd)

    # Over Current Protection
    def OCP(self, channel, on_off ):
        cmd = "OCP %s,%s\n" % (channel, on_off)
        self.issue(cmd)

    # Over Current Protection query
    def OCPQ(self, channel ):
        cmd = "OCP? %s\n" % (channel)
        result = self.query(cmd)
        return result
     
    # Over Current Protection Reset
    def OCRST(self, channel):
        cmd = "OCRST %s\n" % (channel)
        self.issue(cmd)

    # Store register settings
    def STO(self, channel):
        cmd = "STO %s\n" % (channel)
        self.issue(cmd)

    # Recall register settings
    def RCL(self, channel):
        cmd = "RCL %s\n" % (channel)
        self.issue(cmd)

    # Clear to powerup state
    def CLR(self):
        cmd = "CLR\n"
        self.issue(cmd)

    # Status register query
    def STSQ(self, channel ):
        cmd = "STS? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Accumulated status register query
    def ASTSQ(self, channel ):
        cmd = "ASTS? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Unmask register query
    def UNMASKQ(self, channel ):
        cmd = "UNMASK? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Unmask register set
    def UNMASK(self, channel, xxx ):
        cmd = "UNMASK %s,%s\n" % (channel, xxx)
        self.issue(cmd)

    # Fault register query
    def FAULTQ(self, channel ):
        cmd = "FAULT? %s\n" % (channel)
        result = self.query(cmd)
        return result

    # Service ReQuest query
    def SRQQ(self):
        cmd = "SRQ?\n"
        result = self.query(cmd)
        return result

    # Service ReQuest set
    def SRQ(self, fault ):
        cmd = "SRQ %s\n" % (fault)
        self.issue(cmd)

    # Power ON Service ReQuest query
    def PONQ(self ):
        cmd = "PON?\n"
        result = self.query(cmd)
        return result

    # Power ON Service ReQuest set
    def PON(self, on_off ):
        cmd = "PON %s\n" % (on_off)
        self.issue(cmd)

    # Reprogramming Delay Set
    def DLY(self, channel, time_str ):
        cmd = "DLY %s,%s\n" % (channel, time_str)
        self.issue(cmd)

    # Reprogramming Delay Set query
    def DLYQ(self, channel ):
        cmd = "DLY? %s\n" % (channel)
        result = self.query(cmd)
        return result
     
    # LCD Message display
    def DSP(self, msg ):
        cmd = 'DSP "%s"\n' % (msg)
        self.issue(cmd)

    # Error query
    def ERRQ(self ):
        cmd = "ERR?\n"
        result = self.query(cmd)
        return result
     
    # ID query
    def IDQ(self ):
        cmd = "ID?\n"
        result = self.query(cmd)
        return result


    def __del__(self):
        """Destructor -- close the connection."""
        self.close()


def test():
    debuglevel = 0
    dbg = 1
    while sys.argv[1:] and sys.argv[1] == '-d':
        debuglevel = debuglevel+1
        del sys.argv[1]
    host = DEFAULTIP
    sa = None
    if sys.argv[1:]:
        host = sys.argv[1]
    try:
        power = hp6622A(host)
    except connectError , e:
        print e, 'Connection to host %s failed' % host
    else:
        power.set_debuglevel(debuglevel)
        power.dbg = 1
#        power.CLR()
#        power.IDQ()
        power.DSP("MARTYBROESKE")
        power.ERRQ()
        power.STSQ("1")
        power.ASTSQ("1")
        power.UNMASKQ("1")
        power.FAULTQ("1")
        power.SRQQ()
        power.PONQ()
        power.DLYQ("1")

        power.VSETQ("1")
        power.VSET("1","48")
        power.VSETQ("1")
        power.VOUTQ("1")

        power.ISETQ("1")
        power.ISET("1","1.0")
        power.ISETQ("1")

        power.OUTQ("1")
        power.OUT("1","0")
        power.OUTQ("1")
        power.OUT("1", "1")
        power.OUTQ("1")

        power.OVSETQ("1")
        power.OVSET("1","50.0")
        power.OVSETQ("1")
        power.OVRST("1")

        power.OCPQ("1")
        power.OCP("1","1")
        power.OCPQ("1")
        power.OCRST("1")

        power.DLYQ("1")
        power.DLY("1",".05")
        power.DLYQ("1")
        
        power.STO("10")
        power.RCL("1")        
        power.VSETQ("1")
        power.RCL("10")
        power.VSETQ("1")


        power.VSETQ("1")
        power.VSET( "1", "5.25")
        power.VSETQ("1")
        power.VSETQ("1")
        power.VSETQ("1")
        power.VSETQ("1")
        power.VSET( "1", "48.69")
        power.VSETQ("1")
        power.VSETQ("1")
        power.VSETQ("1")
        power.VSETQ("1")

#        switch.interact()

    print '+++ close hp6622A +++'
    power.close()

#====================================================================


if __name__ == '__main__':
    test()
