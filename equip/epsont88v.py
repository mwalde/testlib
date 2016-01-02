#import os, sys
import win32print 

CutPaper        = '\x1dV\x01'
PrintFF3        = '\x1b\x64\x06'
RevPrintOn      = '\x1dB\x01'
RevPrintOff     = '\x1dB\x00'
FontB11         = '\x1bM\x01'     # font 1
FontA11         = '\x1bM\x00'     # font 0
DoubleSizeOn    = '\x1B!\x38'       # Double Height/Width/Emphasize
DoubleSizeOff   = '\x1B!\x00'




class EpsonT88V:

#    self.hPrinter=None
    
    def __init__(self, printer_name='EPSON TM-T88V ReceiptE4'):
        self.dbg=False

        try:
            self.hPrinter = win32print.OpenPrinter (printer_name)
        except:
            self.hPrinter = None
                
        if self.hPrinter == None:
            if self.dbg: print "printer: %s Not Found" % printer_name
        if self.PrinterReady() == False:
            if self.dbg: print "printer: %s Not Ready" % printer_name

        
    def PrinterReady(self):
        if self.hPrinter == None:
            return False

        t = win32print.GetPrinter(self.hPrinter)

        if t[18] == 0:
            return True
        else:
#            print "printer not ready %d" % t[18]
            return False
        

    def StartDocPrinter(self):
        if self.PrinterReady():
            self.hJob = win32print.StartDocPrinter (self.hPrinter, 1, ("test_station", None, "RAW"))
        
        
    def EndDocPrinter(self):
        if self.PrinterReady():
            win32print.EndDocPrinter (self.hPrinter)
        
    def WritePrinter(self, raw_data):
        if self.PrinterReady():
            win32print.WritePrinter (self.hPrinter, raw_data)

    def FontSmall(self):
        if self.PrinterReady():
            win32print.WritePrinter (self.hPrinter, FontB11)
        
    def FontNormal(self):
        if self.PrinterReady():
            win32print.WritePrinter (self.hPrinter, FontA11)
        
    def Eject(self):
        if self.PrinterReady():
            win32print.WritePrinter (self.hPrinter, PrintFF3)
            win32print.WritePrinter (self.hPrinter, CutPaper)
        
    def DoubleSizeOn(self):
        if self.PrinterReady():
            win32print.WritePrinter (self.hPrinter, DoubleSizeOn)
        
    def DoubleSizeOff(self):
        if self.PrinterReady():
            win32print.WritePrinter (self.hPrinter, DoubleSizeOff)
        
    def Close(self):
        if self.hPrinter == None:
            return
        win32print.ClosePrinter (self.hPrinter)
        
        
#===========================================================================
#       print test log
#===========================================================================
def PrintTestLog( mac, msg ):
    p = EpsonT88V()

    p.StartDocPrinter()
    p.DoubleSizeOn()
    p.WritePrinter(mac + "\n")
    p.DoubleSizeOff()
    p.FontSmall()
    p.WritePrinter(msg)
    p.FontNormal()
    p.Eject()
    p.EndDocPrinter()
    p.Close()
    
#===========================================================================
#       test entry
#===========================================================================
def _test():
    p = EpsonT88V()

    p.StartDocPrinter()
    p.DoubleSizeOn()
    p.WritePrinter("00:27:22:DA:00:00\n")
    p.DoubleSizeOff()
    p.FontSmall()
    fail_str = "LogFinalTestStatus RT_Final='FAIL'\n+++OUT OF RANGE+++ F1_TX0_IQOffset == -16.2532762607\n+++OUT OF RANGE+++ F1_TX1_PwrDac == 28\n+++OUT OF RANGE+++ F1_TX1_DataEvm == -31.6506357937\n+++OUT OF RANGE+++ F1_TX1_IQOffset == -2.30501317739\n+++OUT OF RANGE+++ F2_TX0_IQOffset == -15.214029339\n+++OUT OF RANGE+++ F2_TX1_DataEvm == -30.5567960708\n+++OUT OF RANGE+++ F2_TX1_IQOffset == -12.6593769606"
    p.WritePrinter(fail_str)
    p.FontNormal()
#    p.WritePrinter(fail_str)
    p.Eject()
    p.EndDocPrinter()
    

#===========================================================================
#       test entry
#===========================================================================
def test():
    mac = "00:27:22:DA:00:00"
    msg = "LogFinalTestStatus RT_Final='FAIL'\n+++OUT OF RANGE+++ F1_TX0_IQOffset == -16.2532762607\n+++OUT OF RANGE+++ F1_TX1_PwrDac == 28\n+++OUT OF RANGE+++ F1_TX1_DataEvm == -31.6506357937\n+++OUT OF RANGE+++ F1_TX1_IQOffset == -2.30501317739\n+++OUT OF RANGE+++ F2_TX0_IQOffset == -15.214029339\n+++OUT OF RANGE+++ F2_TX1_DataEvm == -30.5567960708\n+++OUT OF RANGE+++ F2_TX1_IQOffset == -12.6593769606"
    PrintTestLog(mac, msg)

    

#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()        
