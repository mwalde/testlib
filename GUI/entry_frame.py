from Tkinter import *
from ttk import Style, Separator, Label, Button                   
class EntryWindow:
    def __init__(self, parent, question, title, default_text ):
        entry_window = Toplevel(parent)
        entry_window.title(title)
        entry_window.lift(parent)
        entry_frame = EntryFrame( entry_window, question, default_text )
        self.answer = entry_frame.answer
        entry_window.destroy()
        
class EntryFrame(Frame):
    def __init__(self, parent, question, default_text ):
        Frame.__init__(self, parent )
        self.answer = StringVar()
        self.answer.set(default_text)
        
        self.question = Label(self, text=question, style='Title.TLabel' ); self.question.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.entry = Entry( self, width=25, textvariable=self.answer ); self.entry.grid(column=0, row=1, padx=10)
        self.entry.select_range(0,END)
        self.entry.icursor(END)
        self.entry.bind('<Return>', func=lambda e: self.quit())
        self.entry.focus_force()
        
        self.bar = Separator(self, orient=HORIZONTAL); self.bar.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.ok = Button(self, text='OK',  command=self.OkBut); self.ok.grid(column=0, row=3, padx=5, pady=5, sticky='e')

        self.grid()

        # Center the Window
        parent.update_idletasks()
        xp = (parent.winfo_screenwidth() / 2) - (self.winfo_width() / 2) - 8
        yp = (parent.winfo_screenheight() / 2) - (self.winfo_height() / 2) - 20
        parent.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(), self.winfo_height(), xp, yp))
        
        self.update()
        parent.mainloop()

    def OkBut(self):
        self.quit()
   
class InfoWindow:
    def __init__(self, parent, title, question ):
        info_window = Toplevel(parent)
        info_window.title(title)
        info_window.lift(parent)
        info_frame = InfoFrame( info_window, question )
        self.answer = info_frame.answer
        info_window.destroy()
        
class InfoFrame(Frame):
    def __init__(self, parent, question ):
        Frame.__init__(self, parent )
        self.answer = StringVar()
        self.question = Label(self, text=question, style='Title.TLabel' ); self.question.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.configure(background='yellow')        
        self.question.configure(background='yellow')        
        
        self.bar = Separator(self, orient=HORIZONTAL); self.bar.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.ok = Button(self, text='OK',  command=self.OkBut); self.ok.grid(column=0, row=3, padx=5, pady=5)

        self.grid()

        # Center the Window
        parent.update_idletasks()
        xp = (parent.winfo_screenwidth() / 2) - (self.winfo_width() / 2) - 8
        yp = (parent.winfo_screenheight() / 2) - (self.winfo_height() / 2) - 20
        parent.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(), self.winfo_height(), xp, yp))
        
        self.update()
        parent.mainloop()

    def OkBut(self):
        self.quit()

   
class PromptWindow:
    titletxt = "Default"
    def __init__(self, parent, title, question , yestxt = "Yes", notxt = 'No' ):
        self.titletxt = title
        prompt_window = Toplevel(parent)
        prompt_window.title(title)
        prompt_window.lift(parent)
        prompt_frame = PromptFrame(prompt_window, question, title=title, yestxt = yestxt, notxt = notxt  )
        self.answer = prompt_frame.answer
        prompt_window.destroy()
        
class PromptFrame(Frame):
    def __init__(self, parent, question, yestxt = "Yes", notxt = 'No', title = 'Default' ):
        Frame.__init__(self, parent )
        self.answer = StringVar()
#        yestxt = "Start Test"
#        notxt  = "Exit Test"
        self.title = Label(self, text=title, style='Title.TLabel' ); 
        self.title.grid(column=0, row=0, padx=10, pady=10)
        self.question = Label(self, text=question, style='Title.TLabel' ); 
        self.question.grid(column=0, row=1, padx=10, pady=10, sticky='w')
#        self.entry = Entry( self, width=25, textvariable=self.answer ); self.entry.grid(column=0, row=1, padx=10)
#        self.entry.select_range(0,END)
#        self.entry.icursor(END)
#        self.entry.bind('<Return>', func=lambda e: self.quit())
#        self.entry.focus_force()
        
        self.bar = Separator(self, orient=HORIZONTAL); self.bar.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.ok = Button(self, text=yestxt, style ='TButton', command=self.ButtonYes); 
        self.ok.grid(column=0, row=2, padx=5, pady=5, sticky='w')
        self.no = Button(self, text=notxt,  style = 'TButton', command=self.ButtonNo); 
        self.no.grid(column=0, row=2, padx=5, pady=5, sticky='e')
        self.ok.bind('<Return>', func=lambda e: self.ButtonYes())
        self.ok.focus_force()

        self.grid()

        # Center the Window
        parent.update_idletasks()
        xp = (parent.winfo_screenwidth() / 2) - (self.winfo_width() / 2) - 8
        yp = (parent.winfo_screenheight() / 2) - (self.winfo_height() / 2) - 20
        parent.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(), self.winfo_height(), xp, yp))
        
        self.update()
        parent.mainloop()

    def OkBut(self):
        self.answer.set("OK")
        self.quit()

    def ButtonYes(self):
        self.answer.set(True)
        self.quit()
   
    def ButtonNo(self):
        self.answer.set(False)
        self.quit()
   

#===========================================================================
#       test entry
#===========================================================================
def test():
    global ButtonFont,TitleFont
    root = Tk()
    s = Style()

    s.configure('Title.TLabel', font="ariel 20 bold")
    s.configure('TButton', font="ariel 14 bold")

#    pw = EntryWindow( root, "Scan UUT barcode ", 'Enter UUT serial number', '002722DA0000')
#    print pw.answer.get()
#    pw = PromptWindow( root,"**** Ready UUT for test ****",
#                       "1) Place board in test fixture\n" + \
#                       "2) Connect the cables\n\n",
#                       yestxt = "Start Test", notxt = "Exit Program")
#    print pw.answer.get()

    pw = InfoWindow( None, 'Ready board %s for test' % '0123456789AB',
                   "1) Place board in test fixture\n2) Connect the cables\nOK when ready")
                   
                   
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()
