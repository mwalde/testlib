
#===========================================================================
#
#           Log events
#
#===========================================================================

class Log():
    LogArray = []
    PrintEntry = False
    
    def clear( self ):
        self.LogArray = []
        
    def entry ( self, str ):
        if self.PrintEntry:
            print str
        self.LogArray.append( str )
        
    def dump( self ):
        str = ''
        for n in range(0, len(self.LogArray), 1):
            str = str + self.LogArray[n] + '\n'
        return str

#===========================================================================
#           Log test
#===========================================================================
def test():
    test_log = Log()

    for n in range( 0, 10, 1):
        test_log.entry("first log entry %d" % n)
    print test_log.dump()
    for n in range( 0, 10, 1):
        test_log.entry("second log entry %d" % n)
    print test_log.dump()
    test_log.clear()
    for n in range( 0, 10, 1):
        test_log.entry("third log entry %d" % n)
    print test_log.dump()
    
    
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':

    test()
