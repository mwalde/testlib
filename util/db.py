import sqlite3 as lite
import datetime

#===========================================================================
#
#           db -- test database class
#
#===========================================================================

class Db( ):
    create_new_column = False
    db_debug = False
    table = ''
    con = None
    cur = None
    afkey = 0
    
    def __init__( self, dbfile, tablename ):
        if (dbfile and tablename):
            self.Open( dbfile, tablename )
            
    #====================================================================
    #                   Database Open
    #           dbfile  -   database path and filename
    #           tablename - data base table name
    #
    #====================================================================
    def Open( self, dbfile, tablename ):
#       global con, cur, afkey, table

        if (self.db_debug):
            print "---Db Open( %s ) ---" % dbfile
        self.table = tablename
        self.con = lite.connect( dbfile )
        self.cur = self.con.cursor()
        
        self.cur.execute("insert into %s (DateStamp) values ( '%s' )" % ( self.table, datetime.datetime.now()))
        self.con.commit()
        self.afkey = self.cur.lastrowid
        if (self.db_debug):
            print "The last Id of the inserted row is %d" % self.afkey
       
    #====================================================================
    #                   Database Entry
    #====================================================================
    def Entry( self, entry, column_name ):
        db_entry = "%s='%s'" % (column_name, entry)
        if (self.db_debug):
            print 'update %s set %s where afkey=%d' % (self.table, db_entry, self.afkey)
        try:
            self.cur.execute('update %s set %s where afkey=%d' % (self.table, db_entry, self.afkey))
        except:
            if self.create_new_column:
                if column_name != "":
                    self.cur.execute("alter table %s add column '%s' 'text'" % (self.table, column_name))
                    self.con.commit()
                    self.cur.execute('update %s set %s where afkey=%d' % (self.table,  entry, self.afkey))
            else:
                print "Bad Db Entry. %s  column_name=%s" % (entry,column_name)
                return
        self.con.commit()
        
    #====================================================================
    #                   Database Close
    #====================================================================
    def Close( self ):
        self.cur.close()
        self.con.close()

#===========================================================================
#           db test
#===========================================================================
def test():
    test_db = Db('final_test_24_db', 'FinalTest24')
    test_db.Entry('01:02:03:04:05:06', 'MacAddr')
    test_db.Close()
    
    

#===========================================================================
#           main entry
#===========================================================================
if __name__ == '__main__':

    test()
