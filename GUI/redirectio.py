import logging
import sys
import threading
from time import sleep
from Queue import Queue
from PyQt4.QtCore import *
from PyQt4.QtGui import *

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

# stdout output wrapper used by redirectio
class stdout_wrapper(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
    #
    #   NOTE: stdout appears to give us lone newline characters
    #         we now filter them out here
        if len(str(text).strip('\n')) == 0:
            return
        tup = (text,True)
        self.queue.put(tup)

# stderr output wrapper used by redirectio
class stderr_wrapper(object):
    def __init__(self,queue):
        self.queue = queue

    def write(self, text):
        tup = (text,False)
        self.queue.put(tup)

# redirects tagged stdout and stderr stream to a common queue
# and generates q_ready events which call and external output_function()
# redirectio.set_output() connects the external output function
# redirectio.start() creates the thread and runs the redirectio instance
class redirectio(QObject):
    q_ready = pyqtSignal(str,bool)

    def __init__(self):
        super(redirectio, self).__init__()
        self.queue = Queue()
        print "redirectio()"
        sys.stdout = stdout_wrapper( self.queue )
        sys.stderr = stderr_wrapper( self.queue )

    @pyqtSlot()
    def run(self):
        logging.debug('start redirectio')
        while True:
            tup = self.queue.get()
            self.q_ready.emit(tup[0], tup[1] )
    
        logging.debug('end  redirectio')
    # set_output sets the output function that will receive q_ready events
    # containing text and stdout/stderr flag
    #  output_function( text, stdout_flag )
    def set_output(self, output_function):
        self.q_ready.connect(output_function)

    def start(self):
        # Create thread that will listen on the other end of the queue, and send the text to the textedit in our application
        self.thread = QThread()
#        self.thread = threading.Thread(name='redirectio')
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()

    def __del__(self):
        self.thread.exit()
        
# python application wrapper
class app_wrapper(QObject):
    def __init__(self, *args, **kwargs ):
        super(app_wrapper, self).__init__()
        self.app = args[0]
        arglist = list(args)
        arglist.remove(self.app)
        self.args = tuple(arglist)
        self.kwargs = kwargs
        
    @pyqtSlot()
    def run(self):
        logging.debug('app_wrapper Starting')
        self.rtncd = self.app(*(self.args), **(self.kwargs))
        logging.debug('app_wrapper Exit')
        self.thread.exit()
        return self.rtncd
        
    def test(self):
        print "%s %s  %s" % (self.app, str(self.args), str(self.kwargs))

    @pyqtSlot()
    def start(self):
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.thread.start()

    def __del__(self):
        logging.debug('app_wrapper __del__')
        self.thread.exit()
        
        
class ioWidget(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self)
        self.setGeometry(1000, 300, 600, 600)
        self.setWindowTitle('Console Output')
        self.layout = QVBoxLayout(self)
        self.textedit = QTextEdit()
        self.layout.addWidget(self.textedit)

    @pyqtSlot(str, bool)
    def append_text(self,text,stdout):
#        if len(str(text).strip('\n')) == 0:
#            return
        endHtml = '</font><br>'
        redHtml = '<font color=red>'
        blkHtml = '<font color=black>'
        self.textedit.moveCursor(QTextCursor.End)
        if stdout:
            #self.textedit.setTextColor(QColor('black'))
            self.textedit.insertHtml( blkHtml + text + endHtml  )
#            self.textedit.insertPlainText( text )
        else:
            #self.textedit.setTextColor(QColor('red'))
            self.textedit.insertHtml( redHtml + "StdErr: " + text + endHtml  )
            #self.textedit.insertPlainText( "StdErr: " + text )


##################################################################################################
# Test code        
def test_app( a1, a2, a3, slave="192.168.1.20", master="172.168.1.20"):
    logging.debug('test_app Starting')
    print "test_app %s, %s, %s, slave=%s, master=%s" % (str(a1), str(a2), str(a3), slave, master)
    for i in range(0,100):
        if i%10 == 0:
            sys.stderr.write("%d\n" % i)
        else:
            print i
        sleep(.5)
        
    logging.debug('test_app Ending')
    return -3
    
      
def test():
    qapp = QApplication(sys.argv)  
    iow = ioWidget( title="stdout / stderr output")
    iow.show()
    io = redirectio()
    io.set_output(iow.append_text)
    io.start()
    print "re directed io"
    #sleep(2)
    
    app = app_wrapper( test_app, 1,2,3,slave="127.168.1.20", master="102.168.1.20")
    app.start()
    app.test()
#    rtncd = app.run()
#    print "return code ", rtncd
#    raw_input("press a key")
    qapp.exec_()
    


if __name__ == '__main__':
    test()

