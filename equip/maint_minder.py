import os
from testlib.util.odometer import Odometer
from testlib.GUI.entry_frame import InfoWindow

class maint_minder():
    AFX_count = 1000
#    CAL_count = 1000
    
    def __init__(self):
        self.af_dir = os.getenv("AF_DIR",'c:/airfiber')    
        self.AFX = Odometer(self.af_dir + "/odometer/AFX_FIXTURE.odo")
        self.CAL = Odometer(self.af_dir + "/odometer/CALIBRATION.odo")
        
    def maintTest(self):
        msg = ""
        if int(self.AFX.get_count()) >= self.AFX_count:
            msg = msg + "AFX Fixture Maintainence Required\n"
#            self.CAL.set_count(self.CAL_count)   # fixture repair requires calibration
#        if int(self.CAL.get_count()) >= self.CAL_count:
#            msg = msg + "Station Calibration Required\n"
        if len(msg):
            pw = InfoWindow( None, 'Maintainence Required', msg)
        
        
    def bumpAFX(self):
        self.AFX.bump_count()
    
    def clearAFX(self):
        print "clearAFX"
        self.AFX.set_count(0)
        
    def bumpCAL(self):
        self.CAL.bump_count()

    def clearCAL(self):
        self.CAL.set_count(0)
        

        
#===========================================================================
#       test entry
#===========================================================================
def test():
    mm = maint_minder()
    mm.bumpAFX()
    mm.bumpCAL()
    
    
#    tkroot = Tk()

#    s = Style()

#    s.configure('Title.TLabel', font="ariel 20 bold")
#    s.configure('TButton', font="ariel 14 bold")
#    tkroot.option_add("*TButton.Font", "ariel 12 bold")
#    tkroot.option_add("*Label.Font", "Helvetica 10")

#    fail_str = "LogFinalTestStatus RT_Final='FAIL'\n+++OUT OF RANGE+++ F1_TX0_IQOffset == -16.2532762607\n+++OUT OF RANGE+++ F1_TX1_PwrDac == 28\n+++OUT OF RANGE+++ F1_TX1_DataEvm == -31.6506357937\n+++OUT OF RANGE+++ F1_TX1_IQOffset == -2.30501317739\n+++OUT OF RANGE+++ F2_TX0_IQOffset == -15.214029339\n+++OUT OF RANGE+++ F2_TX1_DataEvm == -30.5567960708\n+++OUT OF RANGE+++ F2_TX1_IQOffset == -12.6593769606"

#    StatusWindow( tkroot, "Test Status -- 00:27:22:DA:00:01", "PASS\n".rstrip() )
#    StatusWindow( tkroot, "Test Status -- 00:27:22:DA:00:01", "FAIL\n".rstrip(), fail_str )
    


#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()