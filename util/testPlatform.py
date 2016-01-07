import os
import sys
import platform


class testPlatform():

    __system  = None
    __release = None
    __version = None

    def __init__(self, **kwargs):
        self.__system  = platform.system()
        self.__release = platform.release()
        self.__version = platform.version()
        
#        self.setSysPath = kwargs.get('setSysPath',  False)
        self.getAF_DIR()
#        sys.path.append(self.af_dir)
        self.setSysPath( self.af_dir)

    def getAF_DIR(self):
        if self.__system == 'Windows':
            self.af_dir = os.getenv("AF_DIR",'c:\\airfiber')
        else: # assume Ubuntu linix
            self.af_dir = os.getenv("AF_DIR",'\\home\\ubnt\\airfiber')
        return self.af_dir
    
    def setSysPath(self, path):
        sys.path.append(path)
    
    def getSystem(self):
        return self.__system
        
    def getRelease(self):
        return self.__release
        
    def getVersion(self):
        return self.__version

#################################################################################
#
#
def test():
    tp = testPlatform()
    
    print "getSystem() = ", tp.getSystem()
    print "getRelease() = ", tp.getRelease()
    print "getVersion() = ", tp.getVersion()
    print "SysPath  = ", sys.path
  

        
if __name__ == '__main__':
    test()
        