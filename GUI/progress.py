from Tkinter import *
from time import sleep,strftime,clock
import ttk as ttk

class ProgressFrame(LabelFrame):
    def __init__(self, parent, maxseconds):
        LabelFrame.__init__(self, parent, text='Progress', padx=3, pady=3,)
        self.parent = parent
        self.maximum = maxseconds
        self.value = 0

        self.elapsed = StringVar()
        self.remaining = StringVar()
        self.activity = StringVar()

        self.act = Label(self, textvariable=self.activity); self.act.grid(row=0, column=0, columnspan=2)

        self.bar = ttk.Progressbar(self, orient="horizontal", length=325, mode="determinate")
        self.bar["maximum"] = maxseconds
        self.bar.grid(row=1, column=0, columnspan=2)
        self.elp = Label(self, textvariable=self.elapsed); self.elp.grid(row=2, column=0)
        self.rem = Label(self, textvariable=self.remaining); self.rem.grid(row=2, column=1)
        self.grid()

    def settime(self, seconds):
        self.value = seconds
        self.bar['value'] = seconds
        if seconds > self.maximum:
            leftover = 0
        else:
            leftover = self.maximum - seconds
        self.elapsed.set('Elapsed: %2d:%02d' % (seconds/60,seconds%60))
        self.remaining.set('Remaining: %2d:%02d' % ( leftover/60, leftover%60))
        self.update()
       
    def settimecomplete(self, seconds):
        self.value = seconds
        self.bar['value'] = self.maximum
        self.elapsed.set('Elapsed: %2d:%02d' % (seconds/60,seconds%60))
        self.remaining.set('')
        self.update()
 
    def setMaxSeconds( self, maxseconds):
        self.maximum = maxseconds
        self.bar["maximum"] = maxseconds

           
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
        self.settime( elapsed )
        if msg != '':
            self.activity.set(msg)
        self.update()

    def closeProgressBar( self ):
        self.config( text='Progress ')
        self.settime(0)
        self.elapsedTime(0)
        self.activity.set(" ")
        self.update()

    def setProgressBarTitle( self, title ):
        self.config( text='Test Progress ' + title)
        self.update()
        
    def completeProgressBar( self, msg ):
        elapsed = self.elapsedTime(1)
        self.settimecomplete( elapsed )
        self.activity.set(msg)
        self.update()
   
    def progressStart( self ):
        self.closeProgressBar()
        
#===========================================================================
#       test entry
#===========================================================================

def test():
    global tkroot
    tkroot = Tk()
    tkroot.title('Progress Bar Test')
    max = 6 * 60 

    
    frame = ProgressFrame(tkroot, max)
    frame.activity.set('what activity??')
    frame.settime(120)

    cur = 0
    while cur <= max:
        str = 'Activity #%d' % cur
        print str
        frame.activity.set(str)
        frame.settime(cur)
        frame.grid()
        cur = cur + 10
        sleep(1)
        
    
#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':
    test()