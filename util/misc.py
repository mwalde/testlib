import sys
from time import sleep
from testlib.equip.equip import Equip


#====================================================================
#                   Capacity 
#====================================================================
def testCapacity95( radio, timeout=1 ):
    cnt = 0
    cap95 = 32000000 * .95
    for sec in range(0, timeout, 1):
    
        cap = radio.readCapacity()
        print cap
        if cap == 0:
		    radio.write_wait('mwl 60000018 40000')  # open the window

        if cap >= cap95:
            radio.write_wait('mwl 60000018 1e7d3')
            return cap
        if cap > 0 and cap <= cap95:
            cnt += 1
            # shrink the receiver window
            radio.write_wait('mwl 60000018 1e7d3')
        else:
            cnt = 0
            cap= radio.readCapacity()
            print cap
        if cnt > 1:
            radio.write_wait('mwl 60000018 1e7d3')
            return cap
#        sleep(2)
    radio.write_wait('mwl 60000018 1e7d3')
    return None;

def testCapacity( radio, timeout=1, match=32000000): 
    print "match -> %d" % match
    nzcnt = 0
    matchcnt = 0
    for sec in range(0, timeout, 1):
        cap = radio.readCapacity()
        print cap
		
        if cap == 0:
		    radio.write_wait('mwl 60000018 40000')  # open the window

        if cap >= match:
            matchcnt += 1
        elif cap > 0:
            # shrink the receiver window
            radio.write_wait('mwl 60000018 1e7d3')
        
        if matchcnt > 1:
            radio.write_wait('mwl 60000018 1e7d3')
            return cap
        if cap > 0:
            nzcnt += 1
        else:
            nzcnt = 0
            cap= radio.readCapacity()
            print cap
        if nzcnt > 10:
            radio.write_wait('mwl 60000018 1e7d3')
            return cap
#        sleep(2)
#    raw_input("Why no Capacity??")
    radio.write_wait('mwl 60000018 1e7d3')
    return None;

#====================================================================
#                   Pause 
#====================================================================
def Pause():
    raw_input('Pause: Press return to continue')
    
#====================================================================
#                   Select Channel
#====================================================================

def selectTX( swt, chan ):
    selectChannel( swt, chan )

def selectRX( swt, chan ):
    selectChannel( swt, chan )

        
def selectChannel( swt, chan ):
    print "selectChannel( swt, %d)" % chan
    if chan:
#        swt.SwitchOff0()     # Channel 1
        swt.SwitchOff( 0 )     # Channel 1
    else:
#        swt.SwitchOn0()     # Channel 0
        swt.SwitchOn( 0 )     # Channel 0
        
def select5GHz( swt ):
#    swt.SwitchOff9()
    swt.SwitchOff( 9 )
    
def select24GHz( swt ):
#    swt.SwitchOn9()
    swt.SwitchOn( 9 )
    
    
