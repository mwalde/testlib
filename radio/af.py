from testlib.util.enhancedserial import EnhancedSerial
import sys
import os
from telnetlib import *
from time import sleep

#====================================================================

sbyte=lambda n:(255 & n^128)-128 # returns the signed int of an 8-bit
                                 # a fix for the temp(erature) script

#====================================================================
#====================================================================
#       AirFiber Common routines                  
#====================================================================
class af_common():
    dbg = 0
    #====================================================================
    #           write_wait() write cmd and wait for a response and
    #           strip off command and prompt from response string
    #====================================================================
    def write_wait( self, cmd, timeout = 4 ):
        """ Write command to the radio and wait for a prompt
            strip off the command echo and the cmd prompt
            return only result of the operation
        """
        cmd = cmd.strip('\n')       # remove any newline
        self.write( cmd + '\n' )
        result = self.read_until(self.PROMPT, timeout)
        result = result.replace(cmd , '')
        result = result.strip()
        result = result.replace(self.PROMPT, '')
        result = result.strip()
#        print "AF> %s" % cmd
        return result;
    
    def wait_rsp( self, timeout=2 ):
        rsp = self.read_until(self.PROMPT, timeout)
#        print rsp
    #====================================================================
    #              Read MAC address
    #====================================================================
    def get_mac( self ):
        """ get this boards mac address
        """
        results = self.write_wait("ifconfig | grep eth0")
        try:
            self.macAddr = results.split()[4]
            maclist = results[results.find('Ethernet'):].split()[2].split(':')
        except:
            print "retry get_mac()"
            maclist = self.get_mac()
        return maclist
    #====================================================================
    #             Read FPGA Version String
    #====================================================================
    def revFPGA( self ):
        revstr = self.write_wait('ver')
        return revstr
        
    #====================================================================
    #             Read SW Version String
    #====================================================================
    def revSW( self ):
        self.write('\n')
        revstr = self.read_until('#', 1)
        revstr = revstr.strip()
        revstr = revstr.strip('#')
        return revstr
    
    #====================================================================
    #             Read memory and return result as an integer
    #====================================================================
    def read_reg( self, cmd ):
        """ issue cmd (mr?) to read the register then return the register value as an integer
        """
        result = self.write_wait( cmd )
        response = result.split()
        intresult = 0
        try:
            intresult = int( response[1], 16 )
        except:
            print "retry read_reg( %s )" % cmd
            intresult = self.read_reg( cmd )
        
        return intresult
   
    #====================================================================
    #             Test for Counterfeit Radio
    #====================================================================
    def isCounterfeit( self ):
        security = self.read_reg('mrb 6000002e')
        if security & 0x3f:
            print "Counterfeit"
            return True
        else:
            return False

    #====================================================================
    #             Make Radio Counterfeit
    #====================================================================
    def mkCounterfeit( self ):
        self.write_wait('mwb 6000002e 3f')
        self.write_wait('af set countrycode 10000')

    #====================================================================
    #             Radio Ready for test
    #====================================================================
    default_ready_state = [ ('reset','idle'), ('slave','syncing') ]
    
    def radio_ready( self, ready_state = default_ready_state, timeout = 20 ):
        ready = False
        for sec in range(timeout):
            rsp = self.write_wait("af get mode;af get state")
            afstatus = rsp.split()
#            print afstatus
            for ready in ready_state:
                if afstatus[0] == ready[0] and afstatus[1] == ready[1]:
                    return True
            sleep(1)
        print "Radio Ready Failed Mode=%s state=%s" % (afstatus[0], afstatus[1])
        return False

    def executeTTLfile(self, filename):
        """
        #====================================================================
        #                   Execute TeraTerm .TTL file to init
        #====================================================================
        """
        print "Execute TTL File: " + filename
        fTTL = open(filename, "r")
        if fTTL < 0:
            print "open(%s)" % filename
        line = fTTL.readline()
#        print line
        while line:
            linelist = line.split("'")
            items = len(linelist)
#            print items
            if items:
                ttlcmd = linelist[0]
                ttlcmd = ttlcmd.strip()
#                print "|%s|" % ttlcmd
                try:
                    if ttlcmd == 'sendln':
                        cmd = linelist[1]
#                        print "|%s|" % cmd
#                        cmd = cmd.replace("'")
#                        print cmd
                        response = self.write_wait(cmd)
#                        print response
                except:
                    pass
            line = fTTL.readline()
        sleep(1)    # let the file "digest" a bit
        
    #====================================================================
    #                          Read Capacity
    #           Capacity reg X 8 X frag size reg
    #====================================================================
    def readCapacity(self):
        capreg = self.read_reg('mrl 600000cc')
        if self.dbg == 1:
            print "capreg=%d" % capreg
        fragsize = self.read_reg('mrb 600000f9')
        if self.dbg == 1:
            print "fragsize= %d" % fragsize
        capacity = capreg * fragsize * 8
        if self.dbg == 1:
            print "capacity %f" % capacity
        return capacity
    
    #====================================================================
    #                          Read RSSI
    #====================================================================
    def readRSSI(self):
        return self.read_reg('mrb 6000002d')

    def temp( self ):
        """ read both radio temperature DAC and return the values as integers
        """
        tresults = self.write_wait('temp')
#        slicepos = results.find('tx0')
#        sliceresults = results[slicepos:]
        mylist = tresults.split()
        temp0 = int(mylist[1].strip('c'))
        temp1 = int(mylist[3].strip('c'))
        return sbyte(temp0), sbyte(temp1)

    def temp0( self ):
        tmp0, tmp1 = self.temp()
        return tmp0

    #====================================================================
    #                          Read Rx 0/1 I/Q angles
    #====================================================================
    def readRxAngle(self, rxchnl):
        if rxchnl == 'RX0I':
            angle = self.read_reg('mrw 600000da')
        elif rxchnl == 'RX0Q':
            angle = self.read_reg('mrw 600000dc')
        elif rxchnl == 'RX1I':
            angle = self.read_reg('mrw 600000de')
        elif rxchnl == 'RX1Q':
            angle = self.read_reg(' mrw 600000e0')
        else:
            print "readRxIangle( %s ) failed" % rxchnl
            return -1

        return (angle & 0xfff)
        
    #====================================================================
    #                          Read Tx 0/1 I/Q angles
    #====================================================================
    def readTxAngle(self, txchnl):
        if txchnl == 'TX0I':
            angle = self.read_reg('mrw 600000d2')
        elif txchnl == 'TX0Q':
            angle = self.read_reg('mrw 600000d4')
        elif txchnl == 'TX1I':
            angle = self.read_reg('mrw 600000d6')
        elif txchnl == 'TX1Q':
            angle = self.read_reg(' mrw 600000d8')
        else:
            print "readTxIangle( %s ) failed" % txchnl
            return -1

        return (angle & 0xfff)
        
    #====================================================================
    #                          Read Tx I/Q Dac
    #====================================================================
    def readTxIQdac(self, txchnl):
        if txchnl == 'TX0I':
            val = self.read_reg('mrw 600000f0')
        elif txchnl == 'TX0Q':
            val = self.read_reg('mrw 600000f2')
        elif txchnl == 'TX1I':
            val = self.read_reg('mrw 600000f4')
        elif txchnl == 'TX1Q':
            val = self.read_reg(' mrw 600000f6')
        else:
            print "readTxIQdac( %s ) failed" % txchnl
            return -1
        return (val & 0xffff)
        
    #====================================================================
    #                          Read Tx Power Dac
    #====================================================================
    def readTxPwrdac(self, txchnl):
        if txchnl == 'TX0':
            val = self.read_reg('mrb 6000002c')
        elif txchnl == 'TX1':
            val = self.read_reg('mrb 6000002a')
        else:
            print "readTxPwrdac( %s ) failed" % txchnl
            return -1
        return (val)
        
    #====================================================================
    #                          Write Tx Power Dac
    #====================================================================
    def writeTxPwrdac(self, txchnl, val ):
        if txchnl == 'TX0':
            self.write_wait('mwb 6000002c %02x' % val)
        elif txchnl == 'TX1':
            self.write_wait('mwb 6000002a %02x' % val)
        else:
            print "writeTxPwrdac( %s, %02x ) failed" % (txchnl, val)

    #====================================================================
    #                          Read Tx DC Dac
    #====================================================================
    def readTxDCdac(self, txchnl):
        if txchnl == 'TX0':
            cmd = 'mrw 60000108'
        elif txchnl == 'TX1':
            cmd = 'mrw 6000010a'
        else:
            print "readTxDCdac( %s ) failed" % txchnl
            return -1
        # return an average of 5 reads
        val = (self.read_reg(cmd) & 0x03ff)
        val = val + (self.read_reg(cmd) & 0x03ff)
        val = val + (self.read_reg(cmd) & 0x03ff)
        val = val + (self.read_reg(cmd) & 0x03ff)
        val = val + (self.read_reg(cmd) & 0x03ff)
        print "TxDCdac result=", val/5
        return (val/5)       
        
#====================================================================
#       AirFiber Telnet Login                  
#====================================================================
TELNET_PORT = 23

class connectError(Exception): pass

class af_telnet(Telnet, af_common):
    PROMPT = "#"
    
    def __init__(self, ip=None ):
        
        Telnet.__init__(self, None)        
        
        if ip:
            self.connect( ip )


    def connect(self, ip, user='ubnt', passwd='ubnt', retry=5):
        while 1:
            try:
                self.open(ip,TELNET_PORT,0.5)
                response = self.read_until("login:")
                self.write( '%s\n'% user)
                self.read_until('Password:',1)
                self.write('ubnt\n')
                self.read_until('#',3)
                self.write('\n')
                rsp = self.read_until(self.PROMPT, 1)
                self.PROMPT = rsp.strip()
                break
                    
            except Exception, e:
                print "Failed to connect to %s %s" % (ip, e)
                if retry:
                    retry-=1
                    cmd = 'arp -d %s' % ip
#                    print cmd

                    os.system(cmd)
#                    sleep(5)
                else:
                    print "Abort connect to %s" % ip
                    sys.exit()
#                    raise connectError('airfiber')



#====================================================================
#       AirFiber Serial Login                  
#====================================================================

class af_serial(EnhancedSerial, af_common):
    status = None
    def __init__(self, comport=None, baudrate=115200, status=None, username='ubnt', password='ubnt'):
        self.status = status
        if comport != None:
            EnhancedSerial.__init__( self, comport, baudrate )
            self.login( username, password)
        else:
            print "COM port required"
            
    #====================================================================
    #       Login                  
    #====================================================================
    PROMPT = "#"

    def login(self, username, password):
        self.write('\n')
        while 1:
            line = self.readline(timeout=0.4).strip( '\n' )
            self.updStatus()
            if len(line) == 0: continue
            print "%s" % line
            if line.find('login:') > -1:
                self.write('%s\n' % username)
                self.read_until('Password:',1)
                self.write('%s\n' % password)
                self.read_until('#',3)
                self.write('\n')
                rsp = self.read_until(self.PROMPT, 1)
                self.PROMPT = rsp.strip()
                break
#            elif line.find(self.PROMPT) > -1:
            elif len(line) > 1:
                if line[-2] == self.PROMPT:
                    self.PROMPT = line.strip()
                    break
        print "ubnt PROMPT: " + self.PROMPT


    def updStatus( self ):
        if self.status:
            self.status( '')

#====================================================================
#       Test                  
#====================================================================
        
if __name__ == '__main__':
#    radio = af_telnet(ip='192.168.1.20')
#    print radio.get_mac()
#    print radio.revFPGA()
#    print radio.revSW()
#    radio.close()
#    radio.interact()
    
    radio = af_serial( 1 )
    print radio.get_mac()
    print radio.revFPGA()
    print radio.revSW()
    radio.close()
#    print serial.write_wait('af af')
    
    
    
