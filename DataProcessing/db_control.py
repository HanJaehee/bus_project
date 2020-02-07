import pymysql

class dbcontrol:
    def __init__(self, dbName):
        self.conn=pymysql.connect(host='localhost', user='wogml', password='wogml23', db=dbName, charset='utf8')
        self.curs =self.conn.cursor()
    def execute(self, str):
        self.curs.execute(str)
    def commit(self):
        self.conn.commit()
    def close(self):
        self.conn.close()
    def fetchall(self):
        result = self.curs.fetchall()
        return result
