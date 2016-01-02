from Tkinter import *

from PIL import Image, ImageTk
import tkFont
from ttk import *
                   
class PictureWindow:
    def __init__(self, parent, question, picture_file, title, class_="PictureWindow"):
        picture_window = Toplevel(parent)
        picture_window.title(title)
#        picture_window.option_add("*Label.Font", "helvetica 20 bold")
#        picture_window.option_add("*Button.Font", "helvetica 12 bold")
        picture_window.lift(parent)
        picture_frame = PictureFrame( picture_window, question, picture_file )
        self.answer = picture_frame.answer
        picture_window.destroy()
        
class PictureFrame(Frame):
    def __init__(self, parent, question, picture_file):
        Frame.__init__(self, parent) #, padx=3, pady=3,)

        image1 = ImageTk.PhotoImage(Image.open(picture_file))
        self.pic = Label(self, image=image1, relief=RIDGE); self.pic.grid(column=0, row=1, columnspan=2, padx=5, pady=5)

        self.question = Label(self, text=question, style='Title.TLabel' ); self.question.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

        self.bar = Separator(self, orient=HORIZONTAL); self.bar.grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.yes = Button(self, text='Yes',  command=self.YesBut); self.yes.grid(column=0, row=3, padx=5, pady=5)
#        self.yes.focus_force()pic
        self.no  = Button(self, text='No',  command=self.NoBut); self.no.grid(column=1, row=3, padx=5, pady=5)
        self.grid()
        self.answer = None

        # Center the Window
        parent.update_idletasks()
        
        xp = (parent.winfo_screenwidth() / 2) - (self.winfo_width() / 2) - 8
        yp = (parent.winfo_screenheight() / 2) - (self.winfo_height() / 2) - 20
        parent.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(), self.winfo_height(), xp, yp))

        parent.mainloop()

    def YesBut(self):
        self.quit()
        self.answer='yes'

    def NoBut(self):
        self.quit()
        self.answer= 'no'
    

#===========================================================================
#       test entry
#===========================================================================
def test():
    global ButtonFont,TitleFont
    tkroot = Tk()

    s = Style()

    s.configure('Title.TLabel', font="ariel 20 bold")
    s.configure('TButton', font="ariel 14 bold")
    tkroot.option_add("*TButton.Font", "ariel 12 bold")
    tkroot.option_add("*Label.Font", "Helvetica 10")

    pw = PictureWindow( tkroot, "Do the LED's Match?", '../bmp/LED State 1.bmp', 'RT_LED1')
    print pw.answer


#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()