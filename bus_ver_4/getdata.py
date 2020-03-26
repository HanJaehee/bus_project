#-*- coding:utf-8 -*-
"""
    잔여좌석 넣는다.
"""
import urllib.request
import xml.etree.ElementTree as et
import time, sys
from datetime import datetime
from db_control import *

class bus:
    def __init__(self):
        self.serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
        """
        curs.execute('select stationId from stationId where station_num="%s"'%(self.stationNum))
        result = curs.fetchall()
        self.stationId = result[0][0]
        #print(self.stationId)
        curs.close()
        """

    def remainSeat(self):#잔여좌석 가져온닷
        db = dbcontrol('bus')
        db.execute('select areaid, routeName, routeId from bus_info where areaid=29 or areaid=18 or areaid=25')
        #일단은 포천,의정부, G1300
        bus_list = db.fetchall()

        for bus in bus_list:
            areaid = bus[0]
            routeName = bus[1]
            routeId = bus[2]
            url = 'http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=%s&routeId=%s'%(self.serviceKey, routeId)
            response = urllib.request.urlopen(url)
            data = response.read()
            tree = et.fromstring(data)
            
            for data in tree.iter('comMsgHeader'):
                returnCode = data.findtext('returnCode')
            
            if returnCode == '22':
                return 2

            for data in tree.iter('busLocationList'):
                remainSeat = data.findtext('remainSeatCnt')
                stationSeq = data.findtext('stationSeq')
                plateType = data.findtext('plateType') # 3 = 일반 대형버스 , 4 = 2층버스
                now = time.localtime()
                nowtime = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                db.execute("insert into `%s_%s`(date, plateType, remainSeat, stationSeq) values ('%s', %s, %s, %s)"%(areaid, routeName, nowtime, plateType, remainSeat, stationSeq))
            
        db.commit()
        db.close()

test = bus()
count = 0

while(True):
    now = datetime.now()
    if(now.hour > 0 and now.hour <5 ):
        print("sleep..")
        with open("log", "a") as f:
            text = "Sleep in " + str(now) + "\n"
            f.write(text)
        count=0
        time.sleep(3600*5)

    with open("log", "a") as f:
        text = "[+] Success time : " + str(now) + "  count : " + str(count) + "\n"
        f.write(text)

    tmp = test.remainSeat()
    if tmp == 2:
        with open("log", "a") as f:
            text = "[+] Limited : " + str(now) + "  count : " + str(count) + "\n"
            f.write(text)

    count += 1
    time.sleep(600)


    
