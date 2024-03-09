import pymysql
import dotenv
from dotenv import load_dotenv
import os 

class con():
    def __init__(self):
        self.conn = None
        self.cur = None
    
    def connectDB(self):
        load_dotenv()
        host = os.getenv("host")
        user = os.getenv("user")
        password = os.getenv("password")
        db = os.getenv("db")


        self.conn = pymysql.connect(host = host, user=user ,password=password ,db=db,charset="utf8")
        self.cur = self.conn.cursor()
        return self.conn,self.cur

class maplecon(con):
    def insertMapleocid(self,args:list):
        self.conn, self.cur = self.connectDB()
        ocid = args[0]
        nickname = args[1]
        sql = f"INSERT INTO mapleocid VALUES('{ocid}','{nickname}')"
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def findOcid(self,nickname):
        self.conn, self.cur = self.connectDB()
        self.cur.execute("SELECT * FROM mapleocid")
        while (True):
            row = self.cur.fetchone()
            if row ==None:
                break
            if row[1] == nickname:
                self.cur.close()
                self.conn.close()
                return row[0]
        self.cur.close()
        self.conn.close()
        return None
    
    def insertbasic(self,*args):
        self.conn, self.cur = self.connectDB()
        level = args[0]
        data = args[1]
        guildName = args[2]
        image = args[3]
        ocid = args[4]
        C_class = args[5]
        unionLv = args[6]
        dojang = args[7]
        sql = f"INSERT INTO maplebasic VALUES('{level}','{data}','{guildName}','{image}','{ocid}','{C_class}','{unionLv}','{dojang}')"
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def findBasic(self,ocid):
        self.conn, self.cur = self.connectDB()
        self.cur.execute("SELECT * FROM maplebasic")
        while (True):
            row = self.cur.fetchone()
            if row == None:
                break
            if row[4] == ocid:
                self.cur.close()
                self.conn.close()
                return row[:8]
        self.cur.close()
        self.conn.close()
        print(f"메이플 기본정보 조회 실패{ocid}")
        return None
    
    def updateBasic(self,*args):
        self.conn, self.cur = self.connectDB()
        level = args[0]
        data = args[1]
        guildName = args[2]
        image = args[3]
        ocid = args[4]
        C_class = args[5]
        unionLv = args[6]
        dojang = args[7]
        sql = f"UPDATE maplebasic SET level = '{level}', date = '{data}', guildName = '{guildName}', image = '{image}', class = '{C_class}', unionLv = '{unionLv}', dojang = '{dojang}' WHERE ocid = '{ocid}'"
        self.cur.execute(sql)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

