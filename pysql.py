import urllib
import pymysql
from ulrlib.request import urlopen

db = pymysql.connect(host='localhost', port=3306, user='wogml',passwd='wogml23', db='test', charset='utf8',autocommit=True)
cursor=db.cursor()
cursor.execute("select version()")

data = cursor.fetchone()
print("Data base version : %s" %(data))
db.close()