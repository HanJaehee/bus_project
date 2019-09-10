import urllib.request
import xml.etree.ElementTree as et
import pymysql

con = pymysql.connect(host="localhost", user="wogml", password="wogml23", db="bus_station_info", charset="utf8")
con2 = pymysql.connect(host="localhost", user="wogml", password="wogml23", db="bus_seat", charset="utf8")
cur2 = con2.cursor()
cur = con.cursor()

for num in [3100, 3200, 3500, 3600]:
    cur.execute("select stationSeq from bus_%s where stationName='%s'"%(num, "신동초.신동아파밀리에아파트앞"))
    stationSeq = cur.fetchall()
    cur2.execute("select locationNo from bus_%s where ")
