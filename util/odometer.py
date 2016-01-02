from ConfigParser import ConfigParser, RawConfigParser

#===========================================================================
#       Airfiber odometer file
#===========================================================================
class Odometer(ConfigParser):

    def __init__(self, file='odometer.ini'):
        ConfigParser.__init__(self)
            
        self.file = file
        self.read(file)
        print self.file
        
        try:
            self.get_count()
        except:
#            print 'Create file'
            self.config = RawConfigParser()
            self.config.add_section('ODOMETER')
            self.config.set('ODOMETER','count','0')
            with open(self.file, 'wb') as configfile:
                self.config.write(configfile)

            self.read(file)

#        print 'Odometer = ' + self.get_count()

    def get_count(self):
        return self.get('ODOMETER','count')

    def set_count(self, count):
        self.set('ODOMETER','count', '%d' % count)
        # Writing our configuration file to 'example.cfg'
        with open(self.file, 'wb') as configfile:
            self.write(configfile)
        self.read(self.file)

    def bump_count( self ):
        count = int(self.get_count(),10)
        count = count + 1
        self.set_count( count )
        
#===========================================================================
#       test entry
#===========================================================================
def test():
    Odo = Odometer()
    print 'Odo = ' + Odo.get_count()
    print 'Bump...'
    Odo.bump_count()
    print 'Odo = ' + Odo.get_count()
    
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()
