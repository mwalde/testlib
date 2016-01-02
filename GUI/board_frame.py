from ConfigParser import ConfigParser
from Tkinter import *
from ttk import Combobox, Separator
from time import sleep


class BoardFrame(LabelFrame):
    ssid2str = {'0XAF01':'AF24','0XAF02':'AF5U', '0XAF03':'AF5'}
    
    def __init__(self, parent ):
        LabelFrame.__init__(self, parent, text='Board Configuration', padx=3, pady=3,)
        self.cfg = None
        self.version = StringVar()
        self.date = StringVar()
        self.desc = StringVar()
        self.hwrev = StringVar()
        self.ssid = StringVar()
        self.svid = StringVar()
        self.ccode = StringVar()
        self.ccstr = StringVar()
        self.ssidstr = StringVar()

        self.cc_str2code = { 'United States':'840','unlocked':'0' }
        self.cc_code2str = { '840':'United States','0':'unlocked' }
        
        Label(self, text='Hardware Rev:', anchor=W).grid(column=0, row=3, sticky=W)
        Label(self, textvariable=self.hwrev, anchor=E ).grid(column=1, row=3, sticky=E)

        Label(self, text='Product:', anchor=W).grid(column=0, row=4, sticky=W)
        Label(self, textvariable=self.ssidstr, anchor=E ).grid(column=1, row=4, sticky=E)

        Label(self, text='Country Code:', anchor=W).grid(column=0, row=5, sticky=W)

        Label(self, textvariable=self.ccode, anchor=E ).grid(column=1, row=5, sticky=E)
        Label(self, textvariable=self.ccstr, anchor=E ).grid(column=2, row=5, sticky=E)

        self.grid()
        self.refresh()

    def refresh(self, cfg=None):
        if cfg:
            self.cfg = cfg
        if self.cfg:
            print self.cfg.hwrev()
#            self.hwrev.set(self.cfg.hwrev())
#            self.ccode.set(self.cfg.ccode())
            self.ccstr.set(self.cc_code2str.get(self.cfg.ccode(), self.cfg.ccode()))
            
            self.ssid.set(self.cfg.ssid())
            self.svid.set(self.cfg.svid())
            self.date.set(self.cfg.date())
            self.desc.set(self.cfg.desc())
            self.version.set(self.cfg.version())
            self.update()

    def set_ccode( self, ccode ):
        self.ccode.set( ccode )
        self.update()
    
    def set_hwrev( self, hwrev ):
        self.hwrev.set( hwrev )
        self.update()
    
    def set_ssid( self, ssid ):
        self.ssid.set( ssid )
        self.ssidstr.set( self.ssid2str.get(ssid.upper(), ssid)  )
        self.update()
    
    def ccSelect(self,e):
        new_cc = self.cc_str2code[self.ccstr.get()]
        print new_cc
        self.cfg.set_ccode( new_cc )
        self.refresh()

    def hwSelect(self,e):
        new_hw = self.cfg.set_hwrev( new_hw )
        self.refresh()

    def state_disable(self):
        print "hw state: %s" % self.hw.state()
        self.hw.state(['disabled'])
        self.cc.state(['disabled'])
        self.update()
        
    def state_normal(self):
        print "hw state:"
        print self.hw.state()
        self.cc.configure(state='normal')
        self.cc.state(['readonly'])
        self.hw.configure(state='normal')
        self.hw.state(['readonly'])
#        print "hw state: %s" % self.hw.state()
        print "hw state:"
        print self.hw.state()
        self.update()
 
        
