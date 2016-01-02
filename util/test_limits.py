from ConfigParser import ConfigParser

#===========================================================================
#       Airfiber board test limits
#===========================================================================
class Limits(ConfigParser):

    def __init__(self, limits_file='test_limits.ini'):
        ConfigParser.__init__(self)
        self.read(limits_file)

    def print_limits(self):
        print self.get('FILE', 'desc')
        print self.get('FILE', 'version')
        print self.get('FILE', 'date')

#===========================================================================
#       hi-lo range check
#===========================================================================
    def range_check( self, hi, lo, val ):
        if val <= hi and val >= lo:
            return 1
        else:
            return 0

#===========================================================================
#       PASS FAIL limit check
#===========================================================================
    def PassFail_check( self, section, name, value, desc='????'):
        msg = "%s %s %s == %s" % (desc,section,name,value)
        if value == 'PASS' or value == 'NA':
            result = True
        else:
            result = False
        status = ( result, msg )
        return status
    
#===========================================================================
#       value limit check
#===========================================================================
    def limit_check( self, section, name, value, desc='????'):
        msg = ""
        range = self.get(section.strip('_'), name).split(',')
        msg = "%s %s s %s == %s  OK" % (desc,section,name,value)
#        print range
#        print range[0]
#        print range[1]
        try:
            float(value)
            result = self.range_check( float(range[0]), float(range[1]), float(value))
        except:
            result = 0;
        if result == 0:
            msg = "%s %s %s == %s +++OUT OF RANGE+++ : Range High %s  Low %s" % (desc,section,name,value, range[0], range[1])
#            print msg
        status = ( result, msg )
        return status

#===========================================================================
#       value limit check
#===========================================================================
    def limit_plus_minus_check( self, section, name, test_value, ref_value, plus_minus, desc='????'):
        msg = ""
#        range = self.get(section.strip('_'), name).split(',')
        msg = "%s %s s %s == %s  OK" % (desc,section,name,test_value)
#        print range
#        print range[0]
#        print range[1]
        try:
            val = float(test_value)
            ref = float(ref_value)
            pm = float(plus_minus)
            result = self.range_check( ref+pm, ref-pm, val)
        except:
            result = 0;
        if result == 0:
            msg = "%s %s %s == %s +++OUT OF RANGE+++ : Range High %s  Low %s" % (desc,section,name,test_value, ref_value+plus_minus, ref_value-plus_minus)
#            print msg
        status = ( result, msg )
        return status

#===========================================================================
#       return low value of range as a float
#===========================================================================
    def get_float_low( self, section, name ):
        try:
            range = self.get( section, name ).split(',')
#            print range
            fval = float(range[1])
#            print "%s  %f" % (range[1], fval)
            return fval
        except:
            print "get_float_low( %s, %s) -- error" % (section, name)
            return 0
        
        
#===========================================================================
#       test entry
#===========================================================================
def test():
    limit = limits()
    limit.print_limits()
    print limit.limit_check('POWER','RX0','-46')
    print limit.limit_check('POWER','RX1','-55')
    print limit.limit_check('CAPACITY','RX','375000000')
    print limit.limit_check('CAPACITY','TX','352000000')
    print limit.get_float_low('CAPACITY','TX')
  

#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()