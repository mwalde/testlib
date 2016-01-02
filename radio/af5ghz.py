#====================================================================
#       AirFiber 5GHz routines                  
#====================================================================
from testlib.radio.af import *
from testlib.util.dict import *
#====================================================================

sbyte=lambda n:(255 & n^128)-128 # returns the signed int of an 8-bit
                                 # a fix for the temp(erature) script

s16=lambda n:(0xffff & n^0x8000)-0x8000 # returns the signed int of a
                                        # signed 16-bit number
#====================================================================
  
class adi():        

    def readADIreg(self, rxtx, reg ):
        cmd = 'cr%s %s' % (rxtx, reg)
    #    print cmd
        rsp = self.write_wait(cmd)
    #    print rsp
        if len(rsp) < 6:
            print "Retry %s" % cmd
            rsp = self.write_wait(cmd)
            
    
        dict = adi_reg_dict( rsp )
    #    print dict
        _reg = int(reg,16)
    #    print _reg
        _regstr = '%03X' % _reg
    #    print _regstr
        val = int(dict[_regstr],16) 
    #    print '_reg=%d  _regstr=%s  val=%d' % (_reg, _regstr, val)
        return val
    
    def writeADIreg(self, rxtx, reg, data ):
        cmd = 'cw%s %s,%X' % (rxtx, reg, data)
    #    print cmd
        self.write_wait(cmd)

    
    def readADIgain(self, chan ):
        if chan:
            return self.readADIreg( 'rx' ,'10c')   # RX1
        else:
            return self.readADIreg( 'rx', '109')   # RX0
            
    def readADIgainDFS(self, chan ):
        if chan:
            return self.readADIreg( 'tx' ,'10c')   # TX1 rx gain
        else:
            return self.readADIreg( 'tx', '109')   # TX0 rx gain
            
    # read / write TX attenuation       
    def readADIatten(self, chan ):
        if chan:
            lsb = self.readADIreg( 'tx' ,'075')    # TX1
            msb = self.readADIreg( 'tx', '076') & 1
        else:
            lsb = self.readADIreg( 'tx', '073')   # TX0
            msb = self.readADIreg( 'tx', '074') & 1

        db = lsb + (msb * 256)
    #    print 'readADIatten=%X' % db
        return db
            
    attenLimit = 0x60
     
    def setADIattenLimit(self, limit ):
        self.attenLimit = limit
 
    #====================================================================
    #   read the Hittite attenuation setting and convert to dB
    #====================================================================
    def readHittiteAttn( self ):
        reg = self.readADIreg( 'tx', '020')
        reg = reg & 3
        if reg == 0:
            db = 7
        elif reg == 1:
            db = 2
        elif reg == 2:
            db = 5
        else:
            db = 0
        return db
            
 
    #====================================================================
    #   Write attenuation value to proper ADI register value
    #   Before write test new value against limit to prevent PA 
    #   from damage.
    #
    #   return true (1) of value in range
    #   return false (0) if limit exceeded and set atten to the limit 
    #
    #====================================================================
    def writeADIatten( self, chan, db ):

        rtn = 1
        if db < self.attenLimit:
            print "attenuation: 0x%X exceeds limit 0x%X" % (db, self.attenLimit)
            db = self.attenLimit
            rtn = 0

        msb = (db & 0x100) >> 8
        lsb = db & 0xff

    #    print 'writeADIatten  db= %X msb=%X  lsb=%X' % ( db,msb,lsb)
        if chan:
            self.writeADIreg( 'tx' ,'075', lsb)   # TX1
            self.writeADIreg( 'tx' ,'076', msb)
        else:
            self.writeADIreg( 'tx', '073', lsb)   # TX0
            self.writeADIreg( 'tx' ,'074', msb)
        return rtn
        
          
    def SetRxFrequencyGHz(self, GHz):
        af_str = 'af set rxfrequency %d' % int(GHz*1000)
        print af_str
        self.write_wait( af_str )

    def SetTxFrequencyGHz(self, GHz):
        af_str = 'af set txfrequency %d' % int(GHz*1000)
        print af_str
        self.write_wait( af_str )


    def RadioTemp( self, rxtx):
        if rxtx == 'tx':
            rsp = self.write_wait('af get temp1')
            try:
                temp = int(rsp)
                return temp
            except:
                print "direct ADI temp read"
                
        else:
            rsp = self.write_wait('af get temp0')
            try:
                temp = int(rsp)
                return temp
            except:
                print "direct ADI temp read"
                

        
class   af5ghz_telnet( af_telnet, adi ):
    
    def __init__(self, ip, username='ubnt', password='ubnt'):
        af_telnet.__init__(self, ip) #, user=username, passwd=password)
        

class   af5ghz_serial( af_serial, adi ):
    
    def __init__(self, comport, status=None, username='ubnt', password='ubnt'):
        af_serial.__init__(self, comport=comport, status=status, username=username, password=password)
        


#====================================================================
#       Test                  
#====================================================================
        
if __name__ == '__main__':
    radio = af5ghz_telnet(None)     # ip='192.168.1.20')
    radio.connect('192.168.1.20')   # ,user='ubnt', passwd='ubnt', retry=400)
    
    print radio.RadioTemp('tx')
    print radio.RadioTemp('rx')
    print radio.get_mac()
    print radio.revFPGA()
    print radio.revSW()
    radio.close()
#    radio.interact()
    
    radio = af5ghz_serial(1)     # ip='192.168.1.20')

    print radio.RadioTemp('tx')
    print radio.RadioTemp('rx')
    print radio.get_mac()
    print radio.revFPGA()
    print radio.revSW()
    radio.close()

           