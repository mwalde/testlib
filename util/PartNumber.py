#====================================================================
#     scan part number
#
#   return               pn   hw  cc
#       PartNumber:  113-00218-XX CCC RF
#       HWREV:       XX
#       CCODE:       CCC         
#====================================================================

def PartNumber( input ):
   
    ubiquiti_id = ''
    partNumber = ''
    hwrev = ''
    ccode = ''
    ssid  = ''
    valid_pn = False
    
    pnfields = input.split('-')
    if len(pnfields) < 3:
        return valid_pn, partNumber, hwrev, ssid, ccode
    
    print pnfields
    ubiquiti_id = pnfields[0]
    partNumber = pnfields[1]
    xxccc = pnfields[2]
    subfields = xxccc.split(' ')
    hwrev = subfields[0]
    if len(subfields) == 2:
        ccode = subfields[1]
    else:
        ccode = "000"
    
#    ubiquiti_id = input[0:3]
#    partNumber = input[4:9]
#    hwrev = input[10:12]
#    ccode = input[13:16]
    if ccode == '':
        ccode = '000'

    if ubiquiti_id == '113' or ubiquiti_id == '13':
        valid_pn = True
    if partNumber == '02042':
        ssid = '0xAF02'
    if partNumber == '02089':
        ssid = '0xAF03'
    if partNumber == '00218':
        ssid = '0xAF01'
    if partNumber == '00362':
        ssid = '0xAF06'
    if partNumber == '02044':
        ssid = '0xAF05'
    if partNumber == '02048':
        ssid = '0xAF04'
    if partNumber == '02195':
        ssid = '0xAF07'
    if partNumber == '02204':
        ssid = '0xAF08'

        
    print "ubiquiti_id = %s" % ubiquiti_id
    print "PartNumber  = %s" % partNumber
    print "     hwrev  = %s" % hwrev
    print "     ccode  = %s" % ccode
    print "      ssid  = %s" % ssid
 
    if ssid == '':
        valid_pn = False
    
    return valid_pn, partNumber, hwrev, ssid, ccode
    
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    input = '113-02042-04 840'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input
        
    input = '13-02042-04 840'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input

    input = '113-02042-04'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input

    input = '111-02042-04 840'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input
        
        
    input = '113-02089-04 840'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input
        
    input = '113-00218-04 840'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input
        
    input = '113'
    valid, pn, hrev, ssid, ccode = PartNumber( input )
    if valid:
        print "valid %s  %s  %s  %s" % (pn,hrev,ssid,ccode)
    else:
        print "invalid %s" % input
        
       
        