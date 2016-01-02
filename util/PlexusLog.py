from ConfigParser import SafeConfigParser
import os
import io
import datetime
import time
import logging

#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

class PlexusLog(SafeConfigParser):
    TestDesignator = ''
    TestData = '1'
    TestUnits = '1'
    TestLowLimit = '1'
    TestHiLimit = '1'

    def __init__(self, file='C:\plexus\config.ini', part_number="",hwrev="",ccode="", operatorID="", mac="",product="" ):
        SafeConfigParser.__init__(self)

        if os.path.isfile( file ):
            self.no_log = False
        else:
            self.no_log = True
            print "PlexusLog config file not found: %s" % file
        
        self.file = file
        self.read(file)
        logging.debug("loading: %s " % self.file)
        self.operatorID = operatorID
        self.mac = ''.join(mac)

        self.AssemblyNo = "113-%s-%s-%s" % ( part_number, hwrev, ccode)
        self.FixtureID = self.get_data('Datalog','FixtureID','NoFixture')
        self.SystemID = self.get_data('Datalog','SystemID','NoSystemID')
        self.Extension = self.get_data('Datalog','Extension','NoExtension')
        self.EventTyp  = self.get_data('Datalog','EventTyp','NoEventTyp')
        self.ProcessTyp = self.get_data('Datalog','ProcessTyp','NoProcessTyp')
#        self.TestSystemID = self.get_data('Datalog','TestSystemID','NoTestSystemID')
        self.CustomerID = self.get_data('Datalog','CustomerID','NoCustomerID')
        self.EcRevLvl = hwrev
        self.product = product
        self.TestSystemID = self.product + self.ProcessTyp + self.SystemID
        default_path = file.replace('config.ini','Log')
        self.Result_path = self.get_data('Path','Result_path', default_path)
        if os.path.isdir( self.Result_path ) == False:
            self.no_log = True
            print "PlexusLog path not found: %s" % self.Result_path
        
        
    def get_data(self, section, option, default):
        if self.has_section(section):
            if self.has_option(section,option):
                return self.get(section,option)
        return default
        
    def get_date(self):
        format = "%Y%m%d%H%M%S"
        today = datetime.datetime.today()
        s = today.strftime(format)
        return s
        
    def log_data( self, pass_fail, failure_str ):
        if self.no_log:
            return
        self.date = self.get_date()
        self.logFile = self.Result_path + '/' + self.FixtureID + '_' + self.date + '.' + self.Extension

        logging.debug("PlexusLog %s" % self.logFile)
        
        EV = "EV|%s|%s|%s||||%s||%s|||%s||%s|||||%s|||||%s|%s||||||||||||||||||||\n"
        ME = "ME|%s|%s|%s|%s||%s|Fail|%s|||||||||%s|%s\n"
        
        EVrec = EV % ( \
                self.AssemblyNo, \
                self.mac, \
                self.date, \
                self.EventTyp, \
                self.operatorID, \
                self.ProcessTyp, \
                pass_fail, \
                self.TestSystemID, \
                self.CustomerID, \
                self.EcRevLvl )

       
        with open( self.logFile, 'a') as log:
            log.write(EVrec)
            if pass_fail == 'FAIL':
                lines = failure_str.split('\n')
                for line in lines:
                    self.getErrData( line )
                    if self.TestDesignator:
                        MErec = ME % ( \
                                self.AssemblyNo, \
                                self.mac, \
                                self.date, \
                                self.TestDesignator,
                                self.TestData,
                                self.TestUnits,
                                self.TestLowLimit,
                                self.TestHiLimit )
                        log.write(MErec)
 
    def isFloat(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    units_of_measurement = { 
        'txmodrate' : 'modrate',
        'rtxmodrate' : 'modrate',
        'RX0_POWER' : 'dbm',
        'RX1_POWER' : 'dbm',
        'RX0_POWER_REMOTE' : 'dbm',
        'RX1_POWER_REMOTE' : 'dbm',
        'RSSI_0' : 'db',
        'RSSI_1' : 'db',
        'RxCapacity' : 'bps',
        'TxCapacity' : 'bps',
        'InitCurrent' : 'amp',
        'ambient' : 'degC',
        'rssi' : 'db',
        'evm' : 'db',
        'power' : 'dbm',
        'cap' : 'bps',
        
    }
            
    def getErrData(self, line):
            self.TestDesignator = ''
            self.TestData = '1'
            self.TestUnits = '1'
            self.TestLowLimit = '1'
            self.TestHiLimit = '1'
            line = line.replace('  ',' ')
            e = line.split(' ')
#            print e
            # this should catch all RF Out Of Range messages
            if self.isFloat(e[0]):  # log range limits tests, anything starting with a frequency
                self.TestDesignator = e[0]+e[1]+e[2]+e[3]+e[4]  # test discription
                self.TestData = e[6]    # test data
                self.TestLowLimit = e[15]   # test low limit
                self.TestHiLimit = e[13]    # test high limit
                # units of measurement
                self.TestUnits = self.units_of_measurement[e[4]]
                return
                
#            if e[0] == 'Capacity_Error:':
#                self.TestDesignator = e[2]+e[1]+e[3]+e[4]
#            if e[0] == 'Calibration' of e[0] == 'Calibration_Error:' or e[0] == 'BoardLimits' or e[0] == 'Exception:':
            # INITIAL and FINAL Test Out Of Range messages
            if '+++OUT OF RANGE+++' in line:
                self.TestDesignator = e[3]  # test discription
                self.TestData = e[5]    # test data
                self.TestLowLimit = e[14]   # test low limit
                self.TestHiLimit = e[12]    # test high limit
                # units of measurement
                self.TestUnits = self.units_of_measurement[e[3]]
                return


            for substr in ['Calibration','Capacity','BoardLimits','Exception','FinalLimits']: # log these messages
                if substr in line:
                    if 'raise' in line: # filter out raise Calibration_Error
                        continue
                    line = line.strip()
#                    line = line.replace('+++OUT OF RANGE+++ :','')
                    line = line.replace('FinalLimits test FINAL','')
                    line = line.replace('BoardLimits test BOARD','')
                    line = line.replace(' ','')
                    self.TestDesignator = line[:40] if len(line) > 40 else line
                    break
                
#====================================================================
#                 Main entry point
#====================================================================
global err_str


xxerr_str = \
'5.950 ch 0  RXCAL rssi == 77 +++OUT OF RANGE+++ : Range High 110  Low 85\n' + \
'5.880 ch 0  RXCAL rssi == 78 +++OUT OF RANGE+++ : Range High 110  Low 85\n' + \
'Capacity_Error: RX0 5800MHz Low Capacity: 28160000MAC=24:a4:3c:38:49:d1\n' + \
'Capacity_Error: RX0 5800MHz Low Capacity: 22644480MAC=24:a4:3c:38:49:d1\n' + \
'5.800 ch 0  TXCAL evm == -36.0827756903 +++OUT OF RANGE+++ : Range High -37.00000  Low -45.00000\n' + \
'5.800 ch 1  TXCAL evm == -36.8513140567 +++OUT OF RANGE+++ : Range High -37.00000  Low -45.00000\n' + \
'Capacity_Error: RX1 2475MHz Low Capacity: 0 MAC=04:18:d6:e3:24:66\n' + \
'BoardLimits test BOARD GPSpulse == FAIL\n' + \
'2.475 ch 1  RXCAL cap == 26352640 +++OUT OF RANGE+++ : Range High 32080000  Low 28570000\n' + \
'6.200 ch 0  TXCAL power == None +++OUT OF RANGE+++ : Range High 17.5  Low 16.5\n' + \
'6.200 ch 0  TXCAL evm == None +++OUT OF RANGE+++ : Range High -37.00000  Low -45.00000\n' + \
'Exception: TxData Error: TX0 6200MHz No Power (could not convert string to float: ) MAC=24:a4:3c:38:01:47\n' + \
'Traceback (most recent call last):\n' + \
'  File "C:\airfiber\5GHz\test_station.py", line 589, in rf_test\n' + \
'    RxTxCalSense( tdata, eq, channel, tx_freq_list, rx_freq_list, fdd_freq )\n' + \
'  File "C:\airfiber\5GHz\test_station.py", line 353, in RxTxCalSense\n' + \
'    TxPwrAdj( eq, txData, txlvl, 5 )\n' + \
'  File "C:\airfiber\5GHz\test_station.py", line 258, in TxPwrAdj\n' + \
'    waitEVM( eq, txData, retrycnt)\n' + \
'  File "C:\airfiber\5GHz\test_station.py", line 240, in waitEVM\n' + \
'    txData.readTxData( eq.radio, eq.vsa )\n' + \
'  File "C:\airfiber\5GHz\TxData.py", line 78, in readTxData\n' + \
'    raise Calibration_Error( msg )\n' + \
'6.200 ch 1  TXCAL power == 15.4833789084 +++OUT OF RANGE+++ : Range High 17.5  Low 16.5\n' + \
'Calibration Error: TX1 6200MHz No Power (could not convert string to float: )  MAC=24:a4:3c:38:01:47\n' + \
'5.720 ch 0  TXCAL power == None +++OUT OF RANGE+++ : Range High 17.5  Low 16.5\n' + \
'5.720 ch 0  TXCAL evm == None +++OUT OF RANGE+++ : Range High -37.00000  Low -45.00000\n' + \
'Calibration_Error: TxData Error: TX0 6200MHz No Power (could not convert string to float: )\n' + \
'Calibration Error: TX0 5720MHz Low Power (IMM) MAC=24:a4:3c:38:4d:1c\n'

xerr_str = \
'BoardLimits test BOARD OverCurrent == FAIL\n' + \
'BoardLimits test BOARD GPSpulse == FAIL\n' + \
'BoardLimits test BOARD LEDtestOn == FAIL\n' + \
'BoardLimits test BOARD ResetSwitch == FAIL\n' + \
'BoardLimits test BOARD LEDtestOff == FAIL\n' + \
'BoardLimits test BOARD LEDtestOn == FAIL\n' + \
'BoardLimits test PWR InitCurrent == 2.2345 +++OUT OF RANGE+++ : Range High 1.0  Low 0.35\n' + \
'BoardLimits test TEMP ambient == 100 +++OUT OF RANGE+++ : Range High 34  Low 0\n' + \
'BoardLimits test BOARD Config10Half == FAIL\n' + \
'BoardLimits test BOARD Config10Full == FAIL\n' + \
'BoardLimits test BOARD Config10Ping == FAIL\n' + \
'BoardLimits test BOARD Config100Half == FAIL\n' + \
'BoardLimits test BOARD Config100Full == FAIL\n' + \
'BoardLimits test BOARD Config100Ping == FAIL\n' + \
'BoardLimits test BOARD Data10Half == FAIL\n' + \
'BoardLimits test BOARD Data10Full == FAIL\n' + \
'BoardLimits test BOARD Data10Ping == FAIL\n' + \
'BoardLimits test BOARD Data100Half == FAIL\n' + \
'BoardLimits test BOARD Data100Full == FAIL\n' + \
'BoardLimits test BOARD Data100Ping == FAIL\n' + \
'BoardLimits test BOARD Data1000Link == FAIL\n' + \
'BoardLimits test BOARD Data1000Ping == FAIL\n' + \
'BoardLimits test BOARD SwVer == FAIL\n' + \
'Operational Status Failure: bad status\n' + \
'FinalLimits test FINAL txmodrate == 4 +++OUT OF RANGE+++ : Range High 8  Low 6\n' + \
'FinalLimits test FINAL rtxmodrate == 4 +++OUT OF RANGE+++ : Range High 8  Low 6\n' + \
'95% Capacity Failure:\n' + \
'GIGE connection not good Not 1000Mbps-Full\n' + \
'FinalLimits test FINAL signed == FAIL\n' + \
'FinalLimits test FINAL Ping == FAIL\n' + \
'FinalLimits test FINAL Label == FAIL\n' + \
'FinalLimits test FINAL SwVer == FAIL\n' + \
'FinalLimits test FINAL FCC_Lock == FAIL\n' + \
'FinalLimits test FINAL RX0_POWER == -46 +++OUT OF RANGE+++ : Range High -47  Low  -60\n' + \
'FinalLimits test FINAL RX1_POWER == -46 +++OUT OF RANGE+++ : Range High -47  Low  -60\n' + \
'FinalLimits test FINAL RX0_POWER_REMOTE == -46 +++OUT OF RANGE+++ : Range High -47  Low  -60\n' + \
'FinalLimits test FINAL RX1_POWER_REMOTE == -46 +++OUT OF RANGE+++ : Range High -47  Low  -60\n' + \
'FinalLimits test FINAL RSSI_0 == 66 +++OUT OF RANGE+++ : Range High 65  Low  51\n' + \
'FinalLimits test FINAL RSSI_1 == 66 +++OUT OF RANGE+++ : Range High 65  Low  51\n' + \
'FinalLimits test FINAL RxCapacity == 400000001 +++OUT OF RANGE+++ : Range High 400000000  Low  380000000\n' + \
'FinalLimits test FINAL TxCapacity == 400000001 +++OUT OF RANGE+++ : Range High 400000000  Low  380000000\n'

err_str = xxerr_str + xerr_str

if __name__ == '__main__':
    print err_str
    PLog = PlexusLog(part_number='00362',hwrev='19',ccode='840',operatorID='OP123456', mac='010203040506',product='AF5')
    PLog.log_data('FAIL',err_str)
    