from Tkinter import *
from ttk import Style, Separator, Label, Button
                
class StatusWindow:
    def __init__(self, parent, title, passfail, failtext=""):
        status_window = Toplevel(parent)
        status_window.title(title)
        status_window.lift(parent)
        status_frame = StatusFrame( status_window, passfail, failtext)
        status_window.destroy()
        
class StatusFrame(Frame):
    def __init__(self, parent, passfail, failtext):
        Frame.__init__(self, parent)
        self.status = StringVar()
        self.status_text = StringVar()

        self.statuslbl = Label(self, textvariable=self.status, style='Title.TLabel'); self.statuslbl.grid(column=0, row=1, columnspan=2, padx=100, pady=10)

        self.bar = Separator(self, orient=HORIZONTAL); self.bar.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.ok = Button(self, text='OK',  command=self.OkBut, width=10); self.ok.grid(column=0, columnspan=2, row=4, padx=5, pady=5)

        if passfail == 'PASS':
            self.TestPassed()
        elif passfail == 'FAIL':
            self.TestFailed(failtext)
        else:
            self.status.set('What?????')
            
        self.grid()

        # Center the Window
        parent.update_idletasks()
        
        xp = (parent.winfo_screenwidth() / 2) - (self.winfo_width() / 2) - 8
        yp = (parent.winfo_screenheight() / 2) - (self.winfo_height() / 2) - 20
        parent.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(), self.winfo_height(), xp, yp))

        parent.mainloop()

    def OkBut(self):
        self.quit()

    def StatusText(self, text ):
        self.status_text.set(text)
        

    def TestInProgress(self):
        self.status.set('Test In Progress')
        self.statuslbl.configure(foreground='black')
        
    def TestPassed(self):         
        self.status.set('Test PASSED')
        self.configure(background='green')
        self.statuslbl.configure(background='green',foreground='yellow')
        
    def TestFailed(self, text):         
        self.status.set('Test FAIL')
        self.configure(background='red')
        self.statuslbl.configure(background='red',foreground='yellow')
        self.text = Text( self, relief=SUNKEN, width=110, height=16); self.text.grid(column=0, row=3, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.text.insert(INSERT,text)

    

#===========================================================================
#       test entry
#===========================================================================
def test():
    tkroot = Tk()

    s = Style()

    s.configure('Title.TLabel', font="ariel 20 bold")
    s.configure('TButton', font="ariel 14 bold")
    tkroot.option_add("*TButton.Font", "ariel 12 bold")
    tkroot.option_add("*Label.Font", "Helvetica 10")

    fail_str = "LogFinalTestStatus RT_Final='FAIL'\n+++OUT OF RANGE+++ F1_TX0_IQOffset == -16.2532762607\n+++OUT OF RANGE+++ F1_TX1_PwrDac == 28\n+++OUT OF RANGE+++ F1_TX1_DataEvm == -31.6506357937\n+++OUT OF RANGE+++ F1_TX1_IQOffset == -2.30501317739\n+++OUT OF RANGE+++ F2_TX0_IQOffset == -15.214029339\n+++OUT OF RANGE+++ F2_TX1_DataEvm == -30.5567960708\n+++OUT OF RANGE+++ F2_TX1_IQOffset == -12.6593769606"

    StatusWindow( tkroot, "Test Status -- 00:27:22:DA:00:01", "PASS\n".rstrip() )
    StatusWindow( tkroot, "Test Status -- 00:27:22:DA:00:01", "FAIL\n".rstrip(), fail_str )
    


#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()