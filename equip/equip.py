#====================================================================
#           test equipment object
#
#       Manage the opening and closing of test equipment 
#       connections. Provides "global" storage object for active
#       equipment instances.
#====================================================================
import sys
import time
from time import sleep
from ConfigParser import ConfigParser, RawConfigParser
from testlib.util.Cswitch import switch
from testlib.radio.af import *
from testlib.radio.af5ghz import *
from testlib.equip.sgE8267D import *
from testlib.equip.hp11713A import *
from testlib.equip.vsa89601B import *
from testlib.equip.saN9030A import *

from testlib.equip.thermotron8200 import *
from testlib.equip.hp6622A import *
from testlib.equip.netbooter import *
from testlib.GUI.gui import GUI
from testlib.radio.uboot import UBoot
from testlib.equip.labjack import LabJack
from testlib.equip.thermotron8200 import thermotron
from testlib.equip.maint_minder import maint_minder
#from testlib.equip.TS_calibrate import TSCalData
#import u3

import os
            
class Mark:

    start_time = [0,0,0,0,0]
    
    def __init__(self):
        i = 0
        for timer in self.start_time:
            self.start_time[i] = time.time()
            i+=1
        
    def __TS__( self, level, tag ):
        ts = time.time() - self.start_time[level]
        self.start_time[level] = time.time()
        if len(tag):
            sys.stderr.write("Mark!%d,%3.3f,%s\n" % ( level, ts, tag))

    def TS(self, tag=""):
        self.__TS__( 0, tag )
        
    def TS1(self, tag=""):
        self.__TS__( 1, tag )
        
    def TS2(self, tag=""):
        self.__TS__( 2, tag )
        
    def TS3(self, tag=""):
        self.__TS__( 3, tag )
        
    def TS4(self, tag=""):
        self.__TS__( 4, tag )
        

class Equip(Mark):
    af_dir = None       # this is the test data anchor directory
    cfg = None
    cal = None
    sg  = None
    swt = None
    vsa = None
    sa = None
    radio = None
    sradio = None
    therm = None
    pwr = None
    netboot = None
    ub = None
    use_supply = None       # used power supply
    gui = None
    lj = None
    mm = None
    
    def __init__(self, config = "testconfig.ini", equiplist = []):
        self.af_dir = os.getenv("AF_DIR",'c:/airfiber')
        self.cfg = ConfigParser()
        configfile = self.af_dir + '/config/5GHz/' + config
        self.cfg.read(configfile)
        print "Using configfile %s" % configfile
        self.open( equiplist )
        self.mm = maint_minder()

    def openCAL(self, freq_range):
        from testlib.equip.TS_calibrate import TSCalData

        print "CAL"+freq_range
        calfile = self.af_dir + '/calibration/' + self.cfg.get('CALIBRATION','cal_dir_'+freq_range) +'/calibration' + freq_range + '.ini'
        print "Using calfile %s" % calfile
#        self.cal = tscal( calfile )
        self.cal = TSCalData( calfile )
        self.cal.CalibrationDir = self.cfg.get('CALIBRATION','cal_dir_'+freq_range)
        self.cal.setx_path = self.cfg.get('VSA','config_path')  + self.cfg.get('CALIBRATION','cal_dir_'+freq_range)+ '\\'
        print "setx_path=" + self.cal.setx_path

    def open( self, equiplist):
        for item in equiplist:
            for case in switch(item):
                if case('AF'):
                    self.openAF()
                    break
                if case('AFs'):
                    self.openAFs()
                    break
                if case('SG'):
                    self.openSG()
                    break
                if case('VSA'):
                    self.openVSA()
                    break
                if case('SA'):
                    self.openSA()
                    break
                if case('Z11'):
                    self.openZ11()
                    break
#                if case('CAL'):
#                    self.openCAL( '5ghz' )
#                    break;
#                if case('CAL5GHz'):
#                    self.openCAL( '5ghz' )
#                    break;
                if case('CAL24GHz'):
                    self.openCAL( '24ghz' )
                    break;
                if case('SWT'):
                    self.openSWT()
                    break
                if case('PWR'):
                    self.openPWR()
                    break
                if case('UBOOT'):
                    self.openUBOOT()
                    break
                if case('LJ'):
                    self.openLJ()
                    break
                if case('THERM'):
                    self.openTHERM()
                    break
                if case(): # default, could also just omit condition or 'if True'
                    print "could not open %s" % case
                    # No need to break here, it'll stop anyway
    
    
    #====================================================================
    #                   close all open equipment
    #====================================================================
    def close(self, equiplist):
        for item in equiplist:
            for case in switch(item):
                if case('AF'):
                    if self.radio:
                        self.radio.close()
                    break
                if case('AFs'):
                    if self.sradio:
                        self.sradio.close()
                    break
                if case('SG'):
                    if self.sg:
                        self.sg.close()
                    break
                if case('VSA'):
                    if self.vsa:
                        self.vsa.close()
                    break
                if case('SA'):
                    if self.sa:
                        self.sa.close()
                    break
                if case('Z11'):
                    if self.z11:
                        self.z11.close()
                    break
                if case('SWT'):
                    if self.swt:
                        self.swt.close()
                    break
                if case('PWR'):
                    if self.pwr:
                        self.pwr.close()
                    break
                if case('UBOOT'):
                    if self.ub:
                        self.ub.close()
                    break
                if case('THERM'):
                    if self.therm:
                        self.therm.close()
                    break
                if case('LJ'):
                    break
                if case(): # default, could also just omit condition or 'if True'
                    print "could not close %s" % case
                    # No need to break here, it'll stop anyway
 


    def __del__(self):
        for item in [self.sg, self.swt, self.vsa, self.sa, self.radio, self.therm, self.pwr, self.netboot]:
            if item:
                item.close()
    
    #====================================================================
    #                   init Lab Jack
    #====================================================================
    def openLJ(self):
        print "open LJ"
        self.lj = LabJack(self.cfg.get('LABJACK','use'))
#            self.lj = u3.U3()
            # enable counter for GPS pulse
#            self.lj.configIO( TimerCounterPinOffset = 5, EnableCounter0 = True, NumberOfTimersEnabled = 1)
  
    #====================================================================
    #                   init Signal Generator 
    #====================================================================
    def openSG(self):
        print "open SG"
        self.sg  = sgE8267D(self.cfg.get('SG', 'ip_addr') )
#        preset = self.cfg.get('SG','initial_preset')
#        if len(preset):
#            self.sg.rclPreset(preset)
#        else:
#            self.sg.initSigGen( self.cfg.get('SG', 'init_freq'), self.cfg.get('SG', 'init_power'))
#            self.sg.setPowerOffset(self.cfg.get('SG', 'init_offset'))

        
    #====================================================================
    #                   init Airfiber Radio
    #====================================================================
    def openAF(self):
        print "open AF"
        self.radio = af5ghz_telnet(self.cfg.get('AF','ip_addr'))

    #====================================================================
    #                   init Airfiber Radio serial port
    #====================================================================
    def openAFs(self):
        print "open AFs"
        self.sradio = af5ghz_serial(int(self.cfg.get('TS','com_port')), status=self.progress )

    #====================================================================
    #                   init Radio UBOOT interface
    #====================================================================
    def openUBOOT(self):
        print "open UBOOT"
        self.ub = UBoot(int(self.cfg.get('TS','com_port')), 115200 )

    #====================================================================
    #                   init Rx Tx channel 0/1 switch 
    #
    #     --- three way switch ---
    #       S1     S9  
    #       ON     ON      5GHz_lite
    #       ON     OFF      5GHz
    #       OFF    xx      24GHz
    #
    #       S0     
    #       OFF  channel 0
    #       ON   channel 1
    #
    #     --- two way switch --
    #       S1     S9  
    #       xx    OFF      5GHz_lite
    #       xx    OFF      5GHz
    #       xx     ON      24GHz
    #
    #       S0
    #       ON   channel 0
    #       OFF  channel 1
    #
    #====================================================================
    def openSWT(self):
        print "open SWT"
        self.swt = hp11713A( self.cfg.get('SWT','ip_addr'))
        self.threeway = self.cfg.get('SWT','three_way_switch')
        print "self.threeway = ", self.threeway


    
    def selectAF5(self):
        if self.threeway:
            self.swt.SwitchOn( 1 ) # AF5
            self.swt.SwitchOff( 9 )  # 5GHz
        else:
            self.swt.SwitchOff( 9 )
        
    def selectAF5Lite(self):
        if self.threeway:
            self.swt.SwitchOn( 1 )  # AF5
            self.swt.SwitchOn( 9 )  # 5GHz_lite
        else:
            self.selectAF5()
        
    def selectAF24(self):
        if self.threeway:
            self.swt.SwitchOff( 1 ) # 24GHz
        else:
            self.swt.SwitchOn( 9 )

    def selectChannel(self, channel):
        if self.threeway:
            if channel == 0:
                self.swt.SwitchOff ( 0 )
            else:
                self.swt.SwitchOn( 0 )
        else:
            if channel == 0:
                self.swt.SwitchOn ( 0 )
            else:
                self.swt.SwitchOff( 0 )
        

    #====================================================================
    #                   Thermotron 
    #====================================================================
    def openTHERM(self):
        print "open THERM"
        self.therm = thermotron( self.cfg.get('THERM','ip_addr'))

    #====================================================================
    #                   VSA control
    #====================================================================
    def openVSA(self):
        print "open VSA"
        self.vsa = vsa89601B( self.cfg.get('VSA','ip_addr'))
#        self.vsa.loadSetupFile( self.cfg.get('VSA', 'config_dir'), self.cfg.get('VSA', 'init_config'),self.cfg.get('VSA', 'init_config'))

    #====================================================================
    #                   SA control
    #====================================================================
    def openSA(self):
        print "open SA"
        self.sa = saN9030A( self.cfg.get('VSA','ip_addr'))

    #====================================================================
    #                   nrpz11 control
    #====================================================================
    def openZ11(self):
        print "open Z11"
        from testlib.equip.nrpz11 import nrpz11
        self.z11 = nrpz11( self.cfg.get('NRPZ11','dev_id'), timeout=10)

    #====================================================================
    #                   init Rx Tx channel 0/1 switch 
    #====================================================================
    def openGUI(self, title, odo_name ):
        print "open GUI"
        self.gui = GUI(title, odo_name )

    #====================================================================
    #                   init PWR control
    #====================================================================
    def openPWR(self):
        self.use_supply = self.cfg.get('PWR','use_supply')
        print "openPWR use_supply=%s" % self.use_supply
        if self.use_supply == 'HP':
            self.pwr = hp6622A(self.cfg.get('PWR','ip_addr'))

            self.pwr.CLR()

            self.pwr.VSET('1',self.cfg.get('PWR','VSET_1'))
            self.pwr.ISET('1',self.cfg.get('PWR','ISET_1'))
            self.pwr.OVSET('1',self.cfg.get('PWR','OVSET_1'))
            self.pwr.OCRST('1')
            self.pwr.OCP('1',"0")
            self.pwr.OCRST('1')

            self.pwr.VSET('2',self.cfg.get('PWR','VSET_2'))
            self.pwr.ISET('2',self.cfg.get('PWR','ISET_2'))
            self.pwr.OVSET('2',self.cfg.get('PWR','OVSET_2'))
            self.pwr.OCRST('2')
            self.pwr.OCP('2',"0")
            self.pwr.OCRST('2')
            self.pwr.issue("DSP 1\n")

        elif self.use_supply == 'NETBOOT':
            self.pwr = netBooter(self.cfg.get('PWR','netbooter_ip'))
            
    
    #====================================================================
    #                   Power On
    #====================================================================
    def pwrOn(self, output = '1'):
        if self.use_supply == 'HP':
            self.pwr.OUT(output, '1')
        elif self.use_supply == 'NETBOOT':
            if output == '1':
                self.pwr.OneOn()
            else:
                self.pwr.TwoOn()
        sleep(1)
        
    #====================================================================
    #                   Power Off
    #====================================================================
    def pwrOff(self, output = '1'):
        if self.use_supply == 'HP':
            self.pwr.OUT(output, '0')

        elif self.use_supply == 'NETBOOT':
            if output == '1':
                self.pwr.OneOff()
            else:
                self.pwr.TwoOff()
        sleep(1)
        
    #====================================================================
    #                   Over Current Test
    #       True == PASS   False == FAIL
    #====================================================================
    def OverCurrent(self, output = '1'):
        if self.use_supply == 'HP':
            stsquery = self.pwr.STSQ( output )
            if stsquery == '2':
                print "Over Current"
                return False
            else:
                return True
        elif self.use_supply == 'NETBOOT':
            print "Over Current test not supported"
            return True
            
    #====================================================================
    #                   Read Current -- return current as a float
    #====================================================================
    def readCurrent(self, output = '1'):
        if self.use_supply == 'HP':
            current = self.pwr.IOUTQ( output )
#            print current
            try:
                current = float(current)
            except ValueError:
                current = 0.0
            return current
        elif self.use_supply == 'NETBOOT':
            print "Read Current not supported"
            return 0.0
        
    #===========================================================================
    #           Monitor Progress
    #===========================================================================
    def progress( self, str ):
        if str != '':
            print str
        if self.gui:
            self.gui.updProgressBar( str )
    
    def progressComplete( self ):
        if self.gui:
            self.gui.completeProgressBar()
            
    def progressStart( self ):
        if self.gui:
            self.gui.closeProgressBar()
            
    #===========================================================================
    #           set GUI information
    #===========================================================================
    def setSwVer( self, SwVer ):
        print "Version %s" % SwVer
        
    
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
#    eq = Equip( equiplist = ['AF','SWT','SG','VSA','PWR'])
    eq = Equip( )
    
    for freq in eq.cal.freq_list:
        print "RX0_OFFSET_%s=%s" % (freq,eq.cal.get_offset( 0, freq))
        print "RX1_OFFSET_%s=%s" % (freq,eq.cal.get_offset( 1, freq)        )