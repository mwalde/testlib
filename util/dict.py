import pickle

class History():
    filename = None
    default = None
    h = {}          # history dictionary
    
    def __init__( self, file=None, default=None ):
        if file:
            self.filename = file
            self.h = read_dict_file(self.filename)
        else:
            print "No history filename"
            
        if default:
            self.default=default
        else:
            print "No history default value"
            
    def get( self, keyname ):
        return self.__get__(keyname)
        
    def __get__( self, keyname ):
        thing = self.h.get(keyname, self.default)
        return thing


    def set( self, keyname, thing ):
        self.__set__(keyname, thing )

    def __set__( self, keyname, thing ):
        change = False
        try:
            thing1 = self.h[keyname]
            if thing != thing1:
                change = True
        except:
            change = True
 
        if change:
            self.h[keyname] = thing
            self.write()
        return change
        
    def write( self ):
        write_dict_file( self.h, self.filename)
        
    def read( self ):
        if self.filename:
            self.h = read_dict_file(self.filename)
            return True
        else:
            print "No history filename"
            return False
            
def write_dict_file(d, file ):
    with open( file + '.dict', 'wb') as handle:
        pickle.dump(d, handle)
        
def read_dict_file( file ):
    d = {}
    try:
        with open( file + '.dict', 'rb') as handle:
            d = pickle.load(handle)
    except:
        print "no such file %s" % file
    return d
    
    
#===========================================================================
#
#       Convert ADI register read comma separated PORT,VALUE python dictionary
#
#===========================================================================
def adi_reg_dict( csv_str ):

    d = {}

    sp_lstr = csv_str.split()
#    print sp_lstr
    length = len(sp_lstr)
    length = length - length%2
    if length == 0:
        length=1
#    print length

    for n in range(0, length, 1):
        sub_str = sp_lstr[n]
#        print sub_str
        sub_lstr = sub_str.split(',')
#        print sub_lstr
        x = { sub_lstr[0]: sub_lstr[1]}
#        print x
        d.update(x)
#   print d
    return d

#===========================================================================
#
#       Convert comma separated af status string into a python dictionary
#
#===========================================================================
def af_status_dict( csv_str ):

    d = {}

    sp_lstr = csv_str.split(',')
#   print sp_lstr
    length = len(sp_lstr)
    length = length - length%2
#    print length


    for n in range(0, length, 2):
        x = { sp_lstr[0+n]: sp_lstr[1+n] }
#       print x
        d.update(x)
#   print d
    
#    for n in range(0, len(sp_lstr), 2):
#        print "%s=%s\n" % (sp_lstr[0+n], d[sp_lstr[0+n]])

    return d

#===========================================================================
#
#       Convert '=' separated status string into a python dictionary
#
#===========================================================================
def equal_dict( str ):

    d = {}

    lstr = str.split('\r\n')
#    print lstr
    length = len(lstr)
#    print length
        
    for n in range(0, length, 1):
        y = lstr[n].split('=')
        x = { y[0]: y[1] }
#        print x
        d.update(x)
#   print d

    return d

def equal_test():
    str = \
    "MAC0=00:27:22:da:00:22\n" + \
    "MAC1=02:27:22:da:00:22\n" + \
    "SSID=0xaf01\n" + \
    "SVID=0x0777\n" + \
    "HWREV=0x000b\n" + \
    "CCODE=840\n"

    print str
    d = equal_dict( str )
    return d
    
    
#===========================================================================
#
#       Convert command line argumnets NAME=arg into a python dictionary
#
#===========================================================================
import sys
def arg_dict():
    d = {}
    n = 1

    while n < len(sys.argv):
        print sys.argv[n]
        y = sys.argv[n].split('=')
#        print y
        x = { y[0]: y[1] }
#        print x
        d.update(x)
        n = n + 1
    return d
    
#===========================================================================
#
#       test af status dictionary
#
#===========================================================================
def af_test():
    csv_str = \
    "status,master-operational,rxpower0,-48,rxpower1,-49,rxcapacity,386191360,txmodrate,6x,gpspulse,none,dpstat,1000Mbps-Full,miles,0.010,feet,55,rssi0,58,rssi1,59,temp0,49,temp1,50,rrxpower0,-51,rrxpower1,-45,txcapacity,386184960,rtxmodrate,6x,rpowerout,33,powerout,30,rxgain,high,txfrequency,24.1GHz,rxfrequency,24.1GHz,duplex,half,modcontrol,automatic,speed,6x,gps,off,gpspulse,none,linkname,UBNT............................,key,0000:0000:0000:0000:0000:0000:0000:0000,baseline,-82,fade,0"
    
    af = af_status_dict( csv_str )
    
    print af
    return af

#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    d = equal_test()
    print "equal_test() DONE"
    write_dict_file(d, "equal_test")
    d = af_test()
    write_dict_file(d, "af_test")
    
    eqt = read_dict_file("equal_test")
    aft = read_dict_file("af_test")
    print "eqt ", eqt
    print "aft " ,aft
    
    
#    print arg_dict()
    
