import os
from datetime import *
from time import sleep


#===========================================================================
#
#           LogFile -- Log file class
#
#===========================================================================

class LogFile( ):
    db_debug = False
    file = None
    path = None
    logfile = None
    extention = None
    mac_addr = None
    
    def __init__( self, path, logname, extention="", mac_addr=None ):
        if logname and path:
            self.open( path, logname, extention, mac_addr )
            
    #====================================================================
    #                   LogFile Open
    #           logname -   database path and filename
    #
    #====================================================================
    def open( self, path, logname, extention, mac_addr=None ):
        self.path = path
        self.extention = extention
        if mac_addr:
            self.mac_addr = mac_addr
            self.logfile = "%s%s%s_%s_%s" % ( self.mac_addr[3], self.mac_addr[4], self.mac_addr[5], datetime.strftime(datetime.now(),"%y%m%d_%H%M%S"), logname,)
        else:
            self.logfile = logname
        if (self.db_debug):
            print "---Open LogFile( %s ) ---" % self.logfile
            
        self.file = open( "%s/_%s%s" % (self.path, self.logfile, self.extention),'a' )
       
    #====================================================================
    #                   write record 
    #====================================================================
    def write( self, str ):
        self.file.write( str )
        self.file.flush()
        os.fsync(self.file)
        
    #====================================================================
    #                   Database Close
    #====================================================================
    def close( self ):
        self.file.close()
        os.rename("%s/_%s%s" % (self.path, self.logfile, self.extention), "%s/%s%s" % (self.path, self.logfile, self.extention))

#===========================================================================
#           db test
#===========================================================================
def mytest():
#    radio = airfiber('192.168.1.20')
#    mac_addr = radio.get_mac()
    
    test = LogFile('.', 'TestLog', '.csv')
    test.write('line 1,')
    test.write('line 2,')
    test.write(' item 1\n')
    test.write(' item 2')
    test.write('\n')


   

#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':

    mytest()
