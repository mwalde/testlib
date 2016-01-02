from time import *
#from testlib.equip.equip import Equip
from ConfigParser import ConfigParser
from Tkinter import *
import tkFont
from ttk import *
import tkMessageBox
from testlib.GUI.progress import ProgressFrame
from testlib.GUI.board_frame import BoardFrame
from testlib.GUI.config_frame import ConfigFrame
from testlib.GUI.entry_frame import EntryWindow, PromptWindow, InfoWindow
from testlib.util.PartNumber import PartNumber

class   GUI( Tk ):

    def __init__( self, title, odo_name, icon = None ):
        Tk.__init__(self)
    #    tkroot.geometry("1000x500+450+350")
        s = Style()

        s.configure('Title.TLabel', font="ariel 20 bold")
        s.configure('TButton', font="ariel 14 bold")
    #    s.configure('TLabel',font="ariel 10 normal")

        self.option_add("*TButton.Font", "ariel 12 bold")
        self.option_add("*Label.Font", "Helvetica 12 bold")

        self.title(title)
        self.tk.call('wm', 'iconbitmap', self._w, '-default', 'c:\Windows\System32\PerfCenterCpl.ico')

        # init the test  ConfigFrame
        self.cfgframe = ConfigFrame(self, title, odo_name  )
        self.cfgframe.grid(padx=3, pady=3)

        # init Progress Bar
        max = 60 * 12
        self.bar = ProgressFrame(self, max)

        # init board.conf configuration
        self.boardframe = BoardFrame(self)
        self.boardframe.grid(padx=5, pady=5)
#
        # Center the Window
        self.update_idletasks()
        xp = (self.winfo_screenwidth() / 2) - (self.winfo_width() / 2) - 8
        yp = (self.winfo_screenheight() / 4) - (self.winfo_height() / 2) - 20
        self.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(), self.winfo_height(), xp, yp))

        self.update()

    #====================================================================
    #     Progress bar update routines           
    #====================================================================
    basetime = 0.0

    def elapsedTime( self, flag ):
        if flag == 0:
            self.basetime = clock()
        now = clock()
        return (now - self.basetime)

    def updProgressBar( self, msg=''):
        elapsed = self.elapsedTime(1)
        self.bar.settime( elapsed )
        if msg != '':
            self.bar.activity.set(msg)
        self.bar.update()

    def closeProgressBar( self ):
        self.bar.config( text='Test Progress ')
        self.bar.settime(0)
        self.elapsedTime(0)
        self.bar.activity.set(" ")
        self.bar.update()

    def setProgressBarTitle( self, title ):
        self.bar.config( text='Test Progress ' + title)
        self.bar.update()
        
    def completeProgressBar( self ):
        elapsed = self.elapsedTime(1)
        self.bar.settimecomplete( elapsed )
        self.bar.activity.set("Test Complete")
        self.bar.update()
        
    #====================================================================
    #     bump odometer count          
    #====================================================================
    def BumpOdometer( self ):
        self.cfgframe.BumpOdometer()
    
    def openOdometer( self, odo_name):
        self.cfgframe.openOdometer( odo_name )
        
        
    #====================================================================
    #     Prompt Window           
    #====================================================================
    def Prompt_Window( self, title, question , yestxt = "Yes", notxt = 'No' ):
        pw = PromptWindow( self, title, question , yestxt = yestxt, notxt = notxt);
        return pw.answer.get()


    #====================================================================
    #     INFO Window           
    #====================================================================
    def Info_Window( self, title, info_text ):
        pw = InfoWindow( self, title, info_text);
        return pw.answer.get()


    #====================================================================
    #     Scan or Enter Operator ID           
    #====================================================================
    def EnterOperatorID( self ):
        operator_id = ''
        while len(operator_id) == 0:
            pw = EntryWindow( self, "Scan or Enter Operator ID ", 'Scan or Enter Operator ID','')
            operator_id = pw.answer.get()
            
        self.cfgframe.SetOperator(operator_id)
        return operator_id
    #====================================================================
    #     scan part number
    #
    #   return 
    #       PartNumber:  13-00218-XX CCC
    #       HWREV:       XX
    #       CCODE:       CCC         
    #====================================================================
    def scan_part_number( self ):
        default_pn  = '13-02042-'    #'13-00218-'
        default_field1 = '13'
        default_field2 = '00218'
        raw_input = ''
        
        while True:
            pw = EntryWindow( self, "Scan Part Number barcode ", 'Enter UUT Part Number', '')
            raw_input = pw.answer.get()
            if raw_input == '':
                print "Null imput"
                continue
                
            valid, pn, hwrev, ssid, ccode = PartNumber( raw_input )
            if valid == False:
                continue
                
            print "PartNumber: %s" % pn
            print "HWREV       %s" % hwrev
            print "CCODE       %s" % ccode
            print "SSID        %s" % ssid
            self.boardframe.set_ccode(ccode)
            self.boardframe.set_hwrev(hwrev)
            self.boardframe.set_ssid(ssid)
            break
            
        return pn, hwrev, ccode, ssid


    def InputWindow( self, title, prompt ):
        pw = EntryWindow( self, title, prompt );
        return rw.answer.get()
    
    def set_ccode(self, ccode):
        self.boardframe.set_ccode(ccode)
        
    def set_hwrev( self, hwrev):
        self.boardframe.set_hwrev(hwrev)
        
    def set_ssid( self, ssid ):
        self.boardframe.set_ssid(ssid)
        
    #====================================================================
    #     get MAC address and generate MAC0 and MAC1 addresses           
    #====================================================================
    def input_mac( self ):
        default_mac = '002722DA0000'
        rawmac = default_mac

        while rawmac == default_mac or len(rawmac) != 12 or rawmac.isalnum() == False:
            pw = EntryWindow( self, "Scan Serial Number ", 'Enter UUT serial number', default_mac)
            rawmac = pw.answer.get()

        rawmac = rawmac.upper()

        print rawmac

        mac0 = \
            rawmac[0:2] + ":" +\
            rawmac[2:4] + ":" +\
            rawmac[4:6] + ":" +\
            rawmac[6:8] + ":" +\
            rawmac[8:10] + ":" + \
            rawmac[10:12]

        hex = int(rawmac[0:2],16)
        hex = hex | 0x02
        mac1 = \
            '%02X:' % hex +\
            rawmac[2:4] + ":" +\
            rawmac[4:6] + ":" +\
            rawmac[6:8] + ":" +\
            rawmac[8:10] + ":" + \
            rawmac[10:12]
        return mac0,mac1

    
    
    
if __name__== '__main__':
    eq = Equip()
    gui = GUI("airFiber 5GHz Test Station")
    gui.elapsedTime(0)
    opid = gui.EnterOperatorID()
    gui.updProgressBar( "MAC input")
    print opid
    pn, hwrev, ccode = gui.scan_part_number()
    print pn
    mac0, mac1 = gui.input_mac()
    print mac0
    print mac1
    gui.completeProgressBar()
    
    raw_input("Press Enter to proceed")
    
    

def guiSetup():
    global bar, operator_id, bdframe
    cfg.print_cfg()

    cfgframe = ConfigFrame(tkroot, cfg)
    cfgframe.grid(padx=3, pady=3)
    
    bdframe = BoardFrame(tkroot, bd)
    bdframe.grid(padx=3, pady=3)
    
    max = 6 * 60 + 30
    bar = ProgressFrame(tkroot, max)
    
    # Center the Window
    tkroot.update_idletasks()
    xp = (tkroot.winfo_screenwidth() / 2) - (tkroot.winfo_width() / 2) - 8
    yp = (tkroot.winfo_screenheight() / 4) - (tkroot.winfo_height() / 2) - 20
    tkroot.geometry('{0}x{1}+{2}+{3}'.format(tkroot.winfo_width(), tkroot.winfo_height(), xp, yp))

    tkroot.update()

#   get operator ID
    operator_id = ''
    while len(operator_id) == 0:
        pw = EntryWindow( tkroot, "Scan or Enter Operator ID ", 'Scan or Enter Operator ID','')
        operator_id = pw.answer.get()
        
    cfgframe.SetOperator(operator_id)

def updProgressBar( msg=''):
    elapsed = elapsedTime(1)
    bar.settime( elapsed )
    if msg != '':
        bar.activity.set(msg)
    bar.update()

def closeProgressBar():
    bar.config( text='Test Progress ')
    bar.settime(0)
    bar.activity.set(" ")
    bar.update()

def setProgressBarTitle( title ):
    bar.config( text='Test Progress ' + title)
    bar.update()
    
def completeProgressBar():
    bar.activity.set("Test Complete")
    bar.update()
    
