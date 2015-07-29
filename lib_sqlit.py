
#coding=utf-8
#!/usr/bin/python

'''
Created on 2015-07-16
@author: zalzhou
Desc: 
'''

import os
import sys
import time
import traceback
import sqlite3
import StringIO

class ParseSqlit():
    def __init__(self,db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def Query(self,md5):
        self.cur.execute("SELECT * FROM rst WHERE md5=%s",md5)
        row = self.cur.fetchone()
        while row:
            return row

    def QueryAll(self):
        self.cur.execute("SELECT * FROM rst")
        data = self.cur.fetchall()
        return data

    def Add(self,md5):
        try:
            self.cur.execute("INSERT INTO rst VALUES(%s,%s,%s)",\
                (md5[0].strip(),md5[1].strip(),md5[2].strip()))
            self.con.commit()
        except:
            traceback.print_exc()

    def Delete(self,md5):
        if self.Query(md5):
            self.cur.execute("DELETE From rst where md5=%s",md5)
            self.con.commit()
            return 1
        else:  
            return 0

    def __unit__(self):
        self.cur.close
        self.con.close

class DumpSqlit():
    def __init__(self,db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
    
    def DumpTable(self):
        # Create table
        self.cur.execute('''create table rst\
                (md5 vchar,rsttype tinyint,\
                rstproc tinyint,rstfile tinyint,rstreg tinyint,\
                reserve1 int,reserve2 vchar)''')

        # Insert a row of data
        self.cur.execute("""insert into rst\
                values ('md5',1,0,0,0,-1,'null')""")

        # Save (commit) the changes
        self.con.commit()
        
        # We can also close the cursor if we are done with it
        self.con.close()

    def __unit__(self):
        self.cur.close
        self.con.close

if __name__ == '__main__':
    curPath = os.path.abspath(os.path.curdir)

    #保存sqlit文件
    tableName = "sqlit"
    dumpSqlit = DumpSqlit("%s\\%s.db"%(curPath,tableName))
    dumpSqlit.DumpTable()

    #解析sqlit文件
    parseSqlit = ParseSqlit("%s\\sqlit.db"%curPath)
    print parseSqlit.QueryAll()    
