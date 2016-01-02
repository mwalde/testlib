from Tkinter import *
import os
from ttk import Separator, Style
from testlib.util.odometer import Odometer

class ConfigFrame(Frame):
    def __init__(self, parent, title, odo_name="" ):
        Frame.__init__(self, parent)
        self.op_id = StringVar()
        self.op_id.set("")
        self.odo = StringVar()
        self.odo.set("")
        self.description = StringVar()
        self.description.set("")
        self.swVer = StringVar()
        self.swVer.set("0.0.0")
        self.openOdometer(odo_name)
       
        
        self.title = Label(self, text=title); self.title.grid(row=0, column=0, columnspan=2)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky="nsew")

        Label(self, text='Station ID: ').grid(row=2, column=0, sticky='w')
        self.desc = Label(self, textvariable=self.description); self.desc.grid(row=2, column=1, sticky='w')
        
        Label(self, text='Operator ID: ').grid(row=3, column=0, sticky='w')
        Label(self, textvariable=self.op_id).grid(row=3, column=1, sticky='w')

        Label(self, text='Odometer: ').grid(row=4, column=0, sticky='w')
        Label(self, textvariable=self.odo).grid(row=4, column=1, sticky='w')

        Label(self, text='Test Ver:').grid(row=5, column=0, sticky='w')
        Label(self, textvariable=self.swVer).grid(row=5, column=1, sticky='w')
#        Label(self, text='%s  rev %(revno)s' % (release_tag, version_info)).grid(row=3, column=1, sticky='w')

#       remove build date as per Greg
#        Label(self, text='build date:').grid(row=6, column=0, sticky='w')
#        Label(self, text='%(date)s' % version_info).grid(row=6, column=1)
      
        self.grid()

    def openOdometer( self, odo_name ):
        self.odometer = Odometer(os.getenv("AF_DIR",'c:/airfiber') + "\odometer\odometer" + odo_name +".ini")
        self.SetOdometer( self.odometer.get_count() )


    def SetDescription(self, id_str):
        self.description.set(id_str)
        self.update()

    def SetOperator(self, op_id):
        self.op_id.set( op_id )
        self.update()

    def SetOdometer(self, odo):
        self.odo.set( odo )
        self.update()

    def BumpOdometer(self):
        self.odometer.bump_count()
        self.SetOdometer( self.odometer.get_count() )

    def SetswVer(self, swVer):
        self.swVer.set( swVer )
        self.update()
