#-*- coding:utf-8 -*-
import urllib.request
import xml.etree.ElementTree as et
import time, sys
from datetime import datetime
from db_control import *

class getdata:
    def __init__(self, stationNum):
        self.serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
        self.stationNum=stationNum
        curs = dbcontrol('station_info')
        curs.execute('select stationId from stationId where station_num="%s"'%(self.stationNum))
        result = curs.fetchall()
        self.stationId = result[0][0]
        curs.close()

    def remainSeat(self):
        url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=%s&stationId=%s'%(self.serviceKey, self.stationId)
        response = urllib.request.urlopen(url)
        data = response.read()
        tree = et.fromstring(data)
        curs = dbcontrol('bus_seat')
        
        for data in tree.iter('busArrivalList'):
            remainSeat = data.findtext('remainSeatCnt1')
            if remainSeat == '-1':
                continue
            routeId = data.findtext('routeId')
            routeName = self.getrouteName(routeId)
            locationNo = data.findtext('locationNo1')
            now = time.localtime()
            nowtime = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            curs.execute("insert into bus_%s(date, remainSeat, locationNo) values ('%s', %s, %s)"%(routeName, nowtime,remainSeat, locationNo))
        
        curs.commit()
        curs.close()

    def getrouteName(self, routeId):
        curs = dbcontrol('station_info')
        curs.execute('select routeName from station_%s where routeId=%s'%(self.stationNum, routeId))
        result = curs.fetchall()
        routeName = result[0][0]
        return routeName

    
    