from testlib.util.odometer import Odometer

from ConfigParser import ConfigParser
from Tkinter import *
#from version import version_info
#from release_tag import release_tag

from ttk import Separator, Style


class ConfigFrame(Frame):
    def __init__(self, parent, cfg ):
        Frame.__init__(self, parent, padx=3, pady=3,)
        self.cfg = cfg
        self.op_id = StringVar()
        self.op_id.set("")
        
        self.title = Label(self, text='airFiber Test Station'); self.title.grid(row=0, column=0, columnspan=2)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky="nsew")

        Label(self, text='Station ID: ').grid(row=2, column=0, sticky='w')
        self.desc = Label(self, text=cfg.desc()); self.desc.grid(row=2, column=1, sticky='w')
        
        Label(self, text='Operator ID: ').grid(row=3, column=0, sticky='w')
        Label(self, textvariable=self.op_id).grid(row=3, column=1, sticky='w')

        Label(self, text='Odometer: ').grid(row=4, column=0, sticky='w')
        Label(self, textvariable=cfg.odovalue).grid(row=4, column=1, sticky='w')

        Label(self, text='SW version:').grid(row=5, column=0, sticky='w')
#        Label(self, text=release_tag + ' rev %(revno)s' % version_info).grid(row=5, column=1, sticky='w')
#        Label(self, text='%s  rev %(revno)s' % (release_tag, version_info)).grid(row=3, column=1, sticky='w')

#       remove build date as per Greg
#        Label(self, text='build date:').grid(row=6, column=0, sticky='w')
#        Label(self, text='%(date)s' % version_info).grid(row=6, column=1)
        


        self.grid()

    def SetOperator(self, op_id):
        self.op_id.set( op_id )
        self.update()

#===========================================================================
#       Airfiber board configuration
#===========================================================================
class test_station_cfg(ConfigParser):

    def __init__(self, board_file='testconfig.ini'):
        ConfigParser.__init__(self)
        self.read(board_file)
        self.Odo = Odometer()
        self.odovalue = StringVar()
        self.odovalue.set(self.get_odometer())

        

    def print_cfg(self):
        print 'version = ' + self.get('TS', 'config_version')
        print 'date    = ' + self.get('TS', 'config_date')
        print 'desc    = ' + self.get('TS', 'test_station_id')
        print 'db      = ' + self.get('TS', 'test_db_dir') + self.get('TS', 'test_db_file')
        print 'com     = ' + self.get('TS', 'com_port')
        print 'odometer= ' + self.get_odometer()

    def com_port(self):
        return self.get('TS', 'com_port')

    def test_database_path(self):
        return self.get('TS', 'test_db_dir') + self.get('TS', 'test_db_file')

    def date(self):
        return self.get('TS', 'config_date')

    def desc(self):
        return self.get('TS', 'test_station_id')

    def version(self):
        return self.get('TS', 'config_version')

    def get_odometer(self):
        return self.Odo.get_count()

    def bump_odometer(self):
        self.Odo.bump_count()
        self.odovalue.set(self.get_odometer())
        

#===========================================================================
#       test entry
#===========================================================================
def test():
    tkroot = Tk()
    s = Style()

    s.configure('Title.TLabel', font="ariel 20 bold")
    s.configure('TButton', font="ariel 14 bold")

    tkroot.option_add("*TButton.Font", "ariel 12 bold")
    tkroot.option_add("*Label.Font", "Helvetica 12 bold")

#    tkroot.tk.call('wm', 'iconbitmap', tkroot._w, '-default', './bmp/scope.ico')


    tkroot.title('test_station.ini Test')
    cfg = test_station_cfg()
    cfg.print_cfg()
    frame = ConfigFrame(tkroot, cfg)
    frame.grid()

    tkroot.mainloop()
    
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()