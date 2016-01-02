
# test station log
import logging
import logging.config
import os


#logName = None

def tslog( _logName='test_station', anchor='.' ):
    global logName
    logName = _logName
    logfile = anchor + '\\logfiles\\' + logName + '.log'
    print logfile
    fileHandler = logging.handlers.RotatingFileHandler(logfile, mode='a', maxBytes=10000, backupCount=5)
    logger = logging.getLogger(logName)
    logger.setLevel(logging.INFO)
    logger.addHandler(fileHandler)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)

def error( msg ):
    logger = logging.getLogger(logName)
    logger.error( msg )
    
def info( msg ):
    logger = logging.getLogger(logName)
    logger.info( msg )

def warning( msg ):
    logger = logging.getLogger(logName)
    logger.warning( msg )

def critical( msg ):
    logger = logging.getLogger(logName)
    logger.critical( msg )

    
#====================================================================
#                 Main entry point
#====================================================================
if __name__ == '__main__':
    tslog()
    error("This is an error message")
    info("This is an info message")
    warning("This is an warning message")
    critical("This is an critical message")
   