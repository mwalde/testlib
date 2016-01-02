from time import sleep
from ConfigParser import  RawConfigParser
import pickle
import os
import math
from testlib.equip.equip import Equip
from testlib.util.update_ini import update_testconfig

class TSCalFreq():
    fac2xghz = [2410,2425,2450,2475]
    eng2xghz = range(2400,2501,10) + fac2xghz
    
    fac3xghz = [3300,3325,3400,3420,3540,3600,3660,3780,3800,3875]
    eng3xghz = range(3300,3901,25) + fac3xghz

    fac5xghz = [5275,5475,5675,5775,5850,5925]
    eng5xghz = range(5150,5901,50) + fac5xghz

    # includes AF5L, AF5, AF5U
    fac5ghz  = [5150,5225,5300,5375,5450,5480,5560,5640,5720,5800,5880,5950,5960,6040,6120,6200]
    eng5ghz  = range(5480,6201,200) + fac5ghz
    
    eng24ghz = range(24100,24901,400)
    fac24ghz = [24100,24200]

    facAFX   = fac2xghz + fac3xghz + fac5xghz
    engAFX   = eng2xghz + eng3xghz + eng5xghz
    
    facAF5   = fac5ghz
    engAF5   = eng5ghz
    
    facAF24  = fac24ghz
    engAF24  = eng24ghz

    # fixture to tx/rx offset, frequency list lookup
    #                 fixture           tx   rx       eng           factory
    FIXTURE_LOOKUP = {  "AF5"      : ( -3.0, -3.0,  engAF5,  facAF5),
                        "AFX"      : (  0.0,  0.0,  engAFX,  facAFX),
                        "AF24"     : ( -10.0,-10.0, engAF24, facAF24),
                     }
    freq_list = []
    rxoffset  = 0.0
    txoffset  = 0.0
    
    def __init__(self, fixture, factory ):
    
        try:
            tup = self.FIXTURE_LOOKUP.get(fixture)
            self.txoffset = tup[0]
            self.rxoffset = tup[1]
            if factory:
                self.freq_list = tup[3]
            else:
                self.freq_list = tup[2]
        except:
            print "Unknown test fixture: ",fixture
    

class TSCalData(RawConfigParser):
    freq_list = []
    rxoffset = 0.0
    txoffset = 0.0
    fixture = ""
    base_name = ""
    cal_dir = ""
    pickle_path = ""
    ini_path = ""

    use_vsa_offset = False
    setx_path = ""
    CalibrationDir = ""
    file = ""
    
    
    # collected raw calibration data
    cable = {}
    TX0   = {}
    TX1   = {}
    RX0   = {}
    RX1   = {}
    
    # calculated calibration data
    TX0vv = {}
    TX1vv = {}

    def __init__(self, ini_path=None ):
        RawConfigParser.__init__(self)
        if ini_path:
            self.ini_path = ini_path
            self.readCal()
    
    def find_closest_match(self, freq):
        last_f = 0
        for f in self.freq_list:
            if freq == f:
#                print "return f"
                return f
            if freq > f:
                last_f = f
                continue
            else:   # return closest match
#                print "freq %d, last_f %d, f %d" % (freq,last_f,f)
                if (freq - last_f) > (f - freq):
#                    print "return f"
                    return f
                else:
#                    print "return last_f"
                    return last_f
    
    # sig gen offset
    def get_RX_cal_offset( self, channel, freq):
        new_freq = self.find_closest_match(freq)
        if channel:
            offset = self.RX1.get(new_freq, 0)
        else:
            offset = self.RX0.get(new_freq, 0)
        if offset == 0:
            
            print "SG Cal offset not found, channel:%d freq: %s" % (channel, new_freq)
        return offset + self.rxoffset

    # temp methods
    def get_offset( self, channel, freq ):
        return self.get_RX_cal_offset( channel, freq )

    def get_offset5GHzLite( self, channel, freq ):
        return self.get_RX_cal_offset( channel, freq )

    def get_offset24GHz( self, channel, freq ):
        return self.get_RX_cal_offset( channel, freq )


    #  VSA offset
    def get_TX_cal_offset( self, channel, freq ):
        new_freq = self.find_closest_match(freq)
        if channel:
            offset = self.TX1.get(new_freq, 0)
        else:
            offset = self.TX0.get(new_freq, 0) 
            
        if offset == 0:
            print "VSA Cal offset not found, channel:%d freq: %s" % (channel, new_freq)
        return offset + self.txoffset
        
    # temp methods
    def get_vsa_offset( self, channel, freq ):
        return self.get_TX_cal_offset( channel, freq )

    def get_vsa_offset5GHzLite( self, channel, freq ):
        return self.get_TX_cal_offset( channel, freq )

    def get_vsa_offset24GHz( self, channel, freq ):
        return self.get_TX_cal_offset( channel, freq )

    
        
    def writeCal(self):
        print "self.ini_path ", self.ini_path
        try:
            self.add_section('TSCALIBRATION')
        except:
            print "except"

        self.set('TSCALIBRATION','fixture', str(self.fixture))
        self.set('TSCALIBRATION','freq_list', str(self.freq_list))
        self.set('TSCALIBRATION','rxoffset', str(self.rxoffset))
        self.set('TSCALIBRATION','txoffset', str(self.txoffset))

        try:
            self.add_section('CAL_DICT')
        except:
            print "except2"
        self.set('CAL_DICT','cable', str(self.cable))
        self.set('CAL_DICT','TX0', str(self.TX0))
        self.set('CAL_DICT','TX1', str(self.TX1))
        self.set('CAL_DICT','TX0vv', str(self.TX0vv))
        self.set('CAL_DICT','TX1vv', str(self.TX1vv))
        self.set('CAL_DICT','RX0', str(self.RX0))
        self.set('CAL_DICT','RX1', str(self.RX1))
       
        with open(self.ini_path, 'wb') as calfile:
            self.write(calfile)

    def __get_dict( self, major, minor ):
        try:
            data = self.get( major, minor )
            return eval(data)
        except:
            return {}

    def readCal(self):
        print "self.ini_path ", self.ini_path
        self.read(self.ini_path)
        self.rxoffset  = self.__get_dict('TSCALIBRATION','rxoffset')
        self.txoffset  = self.__get_dict('TSCALIBRATION','txoffset')
        try:
            self.freq_list = eval(self.get('TSCALIBRATION','freq_list'))
            self.freq_list.sort()
        except:
            pass
            
        try:
            self.fixture   = self.get('TSCALIBRATION','fixture')
        except:
            pass
        print "self.fixture ", self.fixture
        self.RX0 = self.__get_dict('CAL_DICT','RX0')
        self.RX1 = self.__get_dict('CAL_DICT','RX1')
        self.TX0 = self.__get_dict('CAL_DICT','TX0')
        self.TX1 = self.__get_dict('CAL_DICT','TX1')
    
    def list_exist(self, cal_list ):
        print "self.freq_list ", self.freq_list
        print "Cal_list ", cal_list
        if len(self.freq_list):
            if len(self.freq_list) == len(cal_list):
                return True
        return False
    
        
        
class TSCalibrate( ):
    cal = None
    
                   
#====================================================================
#
#====================================================================
    def __init__(self, fixture, factory, cal_dirname):
        base_name = "calibration%s" % fixture

#       # does the calibration directory exist?
        cal_dir = os.getenv("AF_DIR",'c:/airfiber') + '/calibration/' + cal_dirname
        if not os.path.exists(cal_dir):
            os.makedirs(cal_dir)
        pickle_path = cal_dir + '/' + base_name + '.pkl'
        ini_path    = cal_dir + '/' + base_name + '.ini' 

        self.cal = self.read_pickle(pickle_path)
        if self.cal == None:
            self.cal = TSCalData()
            print self.cal
            if self.cal.fixture != fixture:
                # initialize data first time
                self.flist = TSCalFreq( fixture, factory )
                self.cal.base_name = base_name
                self.cal.cal_dir = cal_dir
                self.cal.pickle_path = pickle_path
                self.cal.ini_path = ini_path
                self.cal.fixture = fixture
                self.cal.freq_list = self.flist.freq_list
                self.cal.rxoffset = self.flist.rxoffset
                self.cal.txoffset = self.flist.txoffset
            
        self.writeCal()
            
    def cable_exist( self ):
        return self.cal.list_exist( self.cal.cable )
    
    def TX0_exist( self ):
        return self.cal.list_exist( self.cal.TX0 )

    def TX1_exist( self ):
        return self.cal.list_exist( self.cal.TX1 )
        
    def RX0_exist( self ):
        return self.cal.list_exist( self.cal.RX0 )
        
    def RX1_exist( self ):
        return self.cal.list_exist( self.cal.RX1 )
            
    def read_pickle( self, path = None ):
        if path == None:
            path = self.cal.pickle_path
        d = None
        try:
            with open( path, 'rb') as handle:
                d = pickle.load(handle)
                if self.dbg:
                    print "reading ", file
                if self.dbg:
                    print d
                self.cal = d
        except:
            a = 1  # duumy
        return d

    def write_pickle(self, path = None):
        if path == None:
            path = self.cal.pickle_path
        with open( path, 'wb') as handle:
            pickle.dump(self.cal, handle)
            
    def writeCal(self):
        self.write_pickle()
        self.cal.writeCal()
        
       
        
#====================================================================
#   Measure the signal loss using the Signal Generator and Signal
#   Analyser
#====================================================================
    def SignalLoss( self, eq, freq, testdBm ):
        if eq.sa:
            return self.saSignalLoss( eq, freq, testdBm)
        else:
            return self.z11SignalLoss( eq, freq, testdBm)
            
            
    def saSignalLoss( self, eq, freq, testdBm ):
        f = float(freq)/1000
        print freq
        print f
        eq.sg.setFREQ( f )
        sleep(1)
        eq.sg.setPOWer( testdBm )
        sleep(1)
        eq.sg.enableRF()

        eq.sa.setCenterFREQ( freq )
        sleep(2)
        eq.sa.setSPAN( 100 )
        sleep(2)
        loss1 = eq.sa.peakSearch()
        sleep(2)
        loss2 = eq.sa.peakSearch()
        sleep(2)
        loss3 = eq.sa.peakSearch()
        
        ave_loss = (loss1 + loss2 + loss3)/3
        print "SignalLoss( %.4f %.4f %.4f ave %.4f" % ( loss1,loss2,loss3,ave_loss)

        eq.sg.disableRF()
        return ave_loss
    
#====================================================================
#   Measure the signal loss using the Signal Generator and Signal
#   Analyser
#====================================================================
    def z11SignalLoss( self, eq, freq, testdBm ):
        f = float(freq)/1000
        print freq
        print f
        eq.sg.setFREQ( f )
#        sleep(1)
        eq.sg.setPOWer( testdBm )
#        sleep(1)
        eq.sg.enableRF()
        sleep(1)

        ave_loss = eq.z11.avgPower( samples=3)

        eq.sg.disableRF()
        return ave_loss
 
#====================================================================
#                    Calibrate Test Cable 
#
#====================================================================
    def calCable( self, eq ):
        cableDict = {}
        for freq in self.cal.freq_list:
            loss = self.SignalLoss( eq, freq, 0 )    # 0 dBM offset
            cableDict[freq] = loss
        return  cableDict
        
#====================================================================
#                    Calibrate Rx Chain 
#
#====================================================================
    def calChainRx( self, eq):
        chainDict = {}
        for freq in self.cal.freq_list:
            loss = self.SignalLoss( eq, freq, abs(self.cal.cable[freq]) )    # lookup cable offset
            chainDict[freq] = loss  # do not add 3 db
    #        chainDict[freq] = (loss + -3)  # add -3dBm
        return chainDict
        
#====================================================================
#                    Calibrate TxChain 
#
#====================================================================
    def calChainTx( self, eq ):
        dBDict = {}
        vvDict = {}
        for freq in self.cal.freq_list:
            loss = self.SignalLoss( eq, freq, abs(self.cal.cable[freq]) )    # lookup cable offset
            dBDict[freq] = loss
            vvDict[freq] = math.pow(10,abs((float(dBDict[freq])/20)))
        return dBDict, vvDict


#====================================================================
#                   calibrate cable
#
#====================================================================
    def calibrate(self, test ):
        eq = Equip(equiplist=['SG','SWT'])
        power_dev = eq.cfg.get('CALIBRATION','power_measurement')
        power_dev = power_dev.split()
        eq.open(power_dev)
        print power_dev
        eq.sg.initSigGen( 5.8, 0 )
        eq.sg.setMODoff()
        eq.sg.disableRF()
        eq.sg.setPowerOffset(0)
        eq.sg.setPOWer(0)
        if self.cal.fixture == "AF5":
            eq.selectAF5()
        elif self.cal.fixture == "AFX":
            eq.selectAF5Lite()
        elif self.cal.fixture == "AF24":
            eq.selectAF24()
        print test
#        sg_init( eq )
        if eq.sa:
            eq.sa.CalAutoOn()
            eq.sa.CalAutoOff()
        
        if test == 'cable':
            self.cal.cable = self.calCable( eq )
            self.writeCal()
            
        if test == 'tx0':
            eq.selectChannel( 0 )
            self.cal.TX0, self.cal.TX0vv = self.calChainTx( eq )
            self.writeCal()
            
        if test == 'tx1':
            eq.selectChannel( 1 )
            self.cal.TX1, self.cal.TX1vv = self.calChainTx( eq )
            self.writeCal()
            
        if test == 'rx0':
            eq.selectChannel( 0 )
            self.cal.RX0 = self.calChainRx( eq )
            self.writeCal()
            
        if test == 'rx1':
            eq.selectChannel( 1 )
            self.cal.RX1 = self.calChainRx( eq )
            self.writeCal()

        if eq.sa:
            eq.sa.CalAutoOn()
           
#====================================================================
#       Write Rx Offset file
#
#====================================================================
    def writeRxOffset( self ):
        outfile = "%s/config%s.cal" % (self.cal.cal_dir, self.cal.fixture)
        outf = open( outfile, 'w')
        
        if len(self.cal.RX0):
            print self.cal.RX0
            for freq in self.cal.freq_list:
                rx0 = float(self.cal.RX0[freq]) + self.cal.rxoffset
                Rx0 = "Rx0_offset_%d  = %s\n" % ( freq, rx0 )
                print Rx0
                outf.write( Rx0 )
            for freq in self.cal.freq_list:
                rx1 = float(self.cal.RX1[freq]) + self.cal.rxoffset
                Rx1 = "Rx1_offset_%d  = %s\n" % ( freq, rx1 )
                print Rx1
                outf.write( Rx1 )
        outf.close()        
           
#====================================================================
#       Write CSV file
#
#====================================================================
    def writeCSV(self):
        outfile = "%s/cal%s.csv" % (self.cal.cal_dir, self.cal.fixture)
        outf = open( outfile, 'w')
 
        csvdata = "Freq,Cable,RX0,TX0,TX0AmpOff,RX1,TX1,TX1AmpOff\n"
        print csvdata,
        outf.write( csvdata )
        for freq in self.cal.freq_list:
            csvdata = "%d,%s,%s,%s,%s,%s,%s,%s\n" % (freq,self.cal.cable[freq],\
            self.cal.RX0[freq],\
            self.cal.TX0[freq],self.cal.TX0vv[freq],\
            self.cal.RX1[freq],\
            self.cal.TX1[freq],self.cal.TX1vv[freq])
            print csvdata,
            outf.write( csvdata )
        outf.close()        
          
#====================================================================
#       Write testconfig.ini
#
#====================================================================
    def write_testconfig(self):
        ct = update_testconfig()
        label = 'cal_dir_%s' % str(self.cal.fixture)
        ct.set('CALIBRATION',label, os.path.basename(self.cal.cal_dir))
        ct.update()
        ct.rename()
          
#====================================================================
#       Test code
#
#====================================================================
def test():
    fixture = "AFX" 
    factory = True
    cal_dir = "Cal_AFX_15_04_30_Factory"
    tscal = TSCalibrate( fixture, factory, cal_dir)
#    tscal.write_testconfig()

    print "Cable exists? ",tscal.cable_exist()
    print "TX0 exists? ",tscal.TX0_exist()
    print "TX1 exists? ",tscal.TX1_exist()
    print "RX0 exists? ",tscal.RX0_exist()
    print "RX1 exists? ",tscal.RX1_exist()
    
#    tscal.writeCSV()
def test2():
    ini_path = "C:/airfiber/calibration/Cal_AFX_15_05_01_Eng/calibrationAFX.ini"
    print "exists? ",str(os.path.exists(ini_path))
    
    cal = TSCalData(ini_path)
    print cal.freq_list
    print cal.fixture
    print cal.rxoffset
    print cal.txoffset

    print cal.find_closest_match( 2304 )
    print cal.find_closest_match( 2409 )
    print cal.find_closest_match( 2410 )
    print cal.find_closest_match( 5900 )
    print cal.find_closest_match( 5901 )

    for freq in range(2400,2500,3):
        print cal.get_RX_cal_offset( 0, freq )
        print cal.get_RX_cal_offset( 1, freq )
        print cal.get_TX_cal_offset( 0, freq )
        print cal.get_TX_cal_offset( 1, freq )
        
    sys.exit()
    
    ini_path = "C:/airfiber/calibration/Cal_AF5_15_04_30_Factory/calibrationAF5.ini"
    print "exists? ",str(os.path.exists(ini_path))
    
    cal = TSCalData(ini_path)
    print cal.freq_list
    print cal.fixture
    print cal.rxoffset
    print cal.txoffset
    
    
if __name__ == '__main__':
    test2()

