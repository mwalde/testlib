#
# update_ini 
# Generic update the contents of a .ini file
#
# update_testconfig
# update the contents of the factory test station testconfig.ini file
#
import os
from ConfigParser import ConfigParser, RawConfigParser

class update_ini( RawConfigParser):

    def __init__(self, file):
        RawConfigParser.__init__(self)
        self.oldfile = file
        self.read(self.oldfile)
        
    def update(self):
        with open(self.oldfile + '.tmp', 'wb') as calfile:
            self.write(calfile)

    def rename(self):
        try:
            os.remove(self.oldfile + '.sav')
        except Exception:
            pass
        
        os.rename(self.oldfile, self.oldfile + '.sav')
        os.rename(self.oldfile + '.tmp', self.oldfile)
        
        
class update_testconfig( update_ini ):
    def __init__(self):
        self.af_dir = os.getenv("AF_DIR",'c:/airfiber')
        configfile = self.af_dir + '/config/5GHz/testconfig.ini'
        update_ini.__init__(self, configfile)
        
    
        
        
def test():
    ct = update_ini('testconfig.ini')
    ct.set('CALIBRATION','cal_dir_3ghz','Cal_3ghz_15_04_22')
    ct.update()
    ct.rename()
    
def test2():
    ct = update_testconfig()
    ct.set('CALIBRATION','cal_dir_3ghz','Cal_3ghz_15_04_22')
    ct.update()
    ct.rename()
    
if __name__ == '__main__':
    test2()            