from testlib.util.enhancedserial import EnhancedSerial
from time import sleep
from subprocess import *
import os



PROMPT = "U-Boot > "
BOOTPROMPT = "Hit any key to stop autoboot:  0"



class UBoot(EnhancedSerial):
    """ UBOOT serial interface
    """
    nfsdir = 1
    verbose = 0

    phy_control_mask         = 0xceff
    phy_control_10Mbps_half  = 0x0000
    phy_control_10Mbps_full  = 0x0100
    phy_control_100Mpbs_half = 0x2000
    phy_control_100Mpbs_full = 0x2100
    phy_control_default      = 0x3100

    phy_status_link          = 0x0400
    phy_status_mask          = 0xe000
    phy_status_10Mbps_half   = 0x0000
    phy_status_10Mbps_full   = 0x2000
    phy_status_100Mbps_half  = 0x4000
    phy_status_100Mbps_full  = 0x6000

    eth10Mbps_half   = 0
    eth10Mbps_full   = 1
    eth100Mbps_half  = 2
    eth10M0bps_full  = 3

    def __init__(self, com_port, baud ):
        print "comport ",com_port
        print "baud ", baud
        super(UBoot, self).__init__(com_port, baud)
        
#====================================================================
#       AirOS Login                  
#====================================================================
    PROMPT = "#"

    def login(self):
        while 1:
            line = self.readline(timeout=0.4).strip( '\n' )
            if len(line) == 0: continue
            print line
            if line.find('login:') > -1: break

        self.write('ubnt\n')
        self.read_until('Password:',1)
        self.write('ubnt\n')
        self.read_until('#',3)
        self.write('\n')
        rsp = self.read_until(self.PROMPT, 1)
        self.PROMPT = rsp.strip()
        
        print "ubnt PROMPT: " + self.PROMPT
       
#====================================================================
#       test eth0 configuration
#       returns config test status
#====================================================================
    def test_eth0_config( self, phy_control, phy_status ):
        control_base = self.read_phy_control_reg() & self.phy_control_mask
        self.write_phy_control_reg( control_base | phy_control )

        tries = 0
        link =  0
        while tries < 6:
            tries = tries + 1
            sleep(1)
            status_reg = self.read_phy_status_reg()
            if status_reg & self.phy_status_link > 0:
                link = 1
                break
            
        if link == 0:
            print "test_eth0_conig FAIL: no link"
            return 0
            
        config = status_reg & self.phy_status_mask
        if config != phy_status:
            print "test_eth0_config FAIL: config match"
            return 0

        return 1                                    

#====================================================================
#       test eth0                  
#====================================================================
    def test_eth0( self ):
        cfgtst = self.test_eth0_config( self.phy_control_10Mbps_half, \
                                             self.phy_status_10Mbps_half)
        print "Test 10Mbps Half %d" % ( cfgtst )

        cfgtst = self.test_eth0_config( self.phy_control_10Mbps_full, \
                                             self.phy_status_10Mbps_full)
        print "Test 10Mbps Full %d" % ( cfgtst )
    
        cfgtst = self.test_eth0_config( self.phy_control_100Mpbs_half, \
                                             self.phy_status_100Mbps_half)
        print "Test 100Mbps Half %d" % ( cfgtst )
    
        cfgtst = self.test_eth0_config( self.phy_control_100Mpbs_full, \
                                             self.phy_status_100Mbps_full)
        print "Test 100Mbps Full %d" % ( cfgtst )
    


#====================================================================
#       write u-boot command and return string response                  
#====================================================================
    def write_cmd(self, cmd, timeout=3 ):
        if self.verbose: print "ub-> %s" % cmd
        self.write( cmd+'\r' )
        response = self.read_until( PROMPT, timeout )
        if self.verbose: print "ub<- %s" % response
        response = response.replace( cmd + '\r\n', '' )
        response = response.replace( '\r\n', '')
        response = response.strip()
        if self.verbose: print response
        return response


#====================================================================
#       Run UBOOT script                 
#====================================================================
    def run_uboot_script( self, script, timeout=10 ):
        self.write( script + '\n')
        while 1:
            line = ub.readline(timeout=0.4).strip( '\n' )
            if len(line) == 0: continue
            print line
            if line.find(PROMPT) > -1: break

#====================================================================
#       read eth0 phy status register 0x11
#====================================================================
    def read_phy_status_reg( self ):
        hexval = self.write_cmd( 'mii read 0 11')
        try:
            regval = int(hexval,16)
        except:
            regval = 0
            print "phy status mii read 0 11 returned %s" % regval

        if self.verbose == 1: print "read_phy_status_reg=%04X\n" % regval
        return regval

#====================================================================
#       read eth0 phy control register  0x01                
#====================================================================
    def read_phy_control_reg( self ):
        hexval = self.write_cmd( 'mii read 0 0')
        try:
            regval = int(hexval,16)
        except:
            regval = 0
            print "phy control mii read 0 0 returned %s" % regval
        if self.verbose == 1: print "read_phy_control_reg=%04X\n" % regval
        return regval

#====================================================================
#       write to eth0 phy control register  0x01                 
#====================================================================
    def write_phy_control_reg( self, regval ):
        self.write_cmd( 'mii write 0 0 %04X'% regval)
        if self.verbose == 1: print "write_phy_control_reg=%04X\n" % regval

#====================================================================
#       write to eth0 phy control config                 
#====================================================================
    def write_phy_control_config( self, config ):
        reg = (self.read_phy_control_reg() & self.phy_control_mask)
        reg = reg | config
        self.write_phy_control_reg( reg )

#====================================================================
#       set eth0 ipaddr                 
#====================================================================
    def set_eth0_ipaddr(self, ipaddr ):
        response = self.write_cmd('setenv ipaddr %s' % ipaddr )

#====================================================================
#       execute ttl file            
#====================================================================
    def execute_ttl_file( self, filename_ttl ):
        """ read TeraTerm .ttl file and execute all "sendln"  commands
        """
        ttl = open( filename_ttl, 'r')
        while True:
            line = ttl.readline()
            if not line: break
            if line.find("sendln") == 0:
                line = line.replace("sendln","")
                line = line.strip(" '\n")
                line = line.strip('"')
                print line
                self.write_cmd( line )
#                response = self.readline( ).strip('\n')
#                print response
        ttl.close()
        self.readline()



#====================================================================
#                  
#====================================================================
    def saveenv( self ):
        self.write_cmd( 'saveenv' )
        sleep(1)
        
#====================================================================
#                  
#====================================================================
    def wait_for_boot( self ):
        attempts = 30
        self.verbose = 0
        while attempts > 0:
            attempts = attempts - 1
            result = self.write_cmd('',timeout=.25)
            if self.verbose == 1: print result
            if result.find('xxtimeout') > -1:
                print '.',
                continue
            else:
#                self.verbose = 1
#                self.readline()
                print
                return True
#        self.verbose = 1
        print
        return 

#====================================================================
#                  end of uboot class
#====================================================================
#====================================================================
#                  
#====================================================================
def bootme_switches():
    global ub,power
    pwrOff()
    while True:
        print
        print
        print
        print "Set DIP swiches  D U D D   U U D U"
        raw_input( "Press return when ready" )
        pwrOn()
#        sleep(2)
        while True:
            line = ub.readline( 3 )
            if len(line) > 5: break
        print line
        pwrOff()
        pos = line.find('BOOTME')
        print pos
        if pos > -1: break
    print "BOOTME Found"
    
#====================================================================
#                  
#====================================================================
    
def uboot_switches(boot_from):
    global ub,power
    pwrOff()
    while True:
        print
        print
        print
        if boot_from == 'NAND':
            print "Set DIP swiches  U U U U   U D D D"
        if boot_from == 'SPI':
            print "Set DIP swiches  U U U U   U U D D"
        raw_input( "Press return when ready" )
        pwrOn()
#        sleep(2)
        if ub.wait_for_boot() > 0: break
    print "radio booted"
    
   
#====================================================================
#       test eth0                  
#====================================================================
def xtest_eth0( ):
    cfgtst = ub.test_eth0_config( ub.phy_control_10Mbps_half, \
                                     ub.phy_status_10Mbps_half)
    print "Test 10Mbps Half %d" % ( cfgtst )

    cfgtst = ub.test_eth0_config( ub.phy_control_10Mbps_full, \
                                     ub.phy_status_10Mbps_full)
    print "Test 10Mbps Full %d" % ( cfgtst )

    cfgtst = ub.test_eth0_config( ub.phy_control_100Mpbs_half, \
                                     ub.phy_status_100Mbps_half)
    print "Test 100Mbps Half %d" % ( cfgtst )

    cfgtst = ub.test_eth0_config( ub.phy_control_100Mpbs_full, \
                                     ub.phy_status_100Mbps_full)
    print "Test 100Mbps Full %d" % ( cfgtst )
    
    pingtst = ping('192.168.1.1')
    print "ping %d" % ( pingtst )


def xmii_test():
    global cfg, ub, pwr
    global nand, spi

    nand = 'true'
    spi = 'true'
    
    cfgSetup()
    pwrSetup()
    ubSetup()
    print '---- Test eth0 ----'
    ub.wait_for_boot()
#    sleep(4)
    ub.set_eth0_ipaddr("192.168.1.20")
    test_eth0()
    ub.write('boot\n')
    ub.login()
    ub.close()



if __name__ == '__main__':
#    mii_test()
#    update_sw_fpga_uboot()
    program_flash()

        
        
        