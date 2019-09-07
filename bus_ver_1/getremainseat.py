#-*- codig:utf-8 -*-
"""
버스도착정보조회서비스
doc: GB208
"""
import urllib.request
import xml.etree.ElementTree as et
import sqlite3
import time, sys
from datetime import datetime

def getbusArrival(serviceKey, stationId):
    #해당 정류소에서 조회시, 버스 두개가 조회되는데 일단은 한개 정보만 수집
    url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=%s&stationId=%s'%(serviceKey, stationId)
    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)
    conn = sqlite3.connect('bus.db')
    curs = conn.cursor()
    now = time.localtime()

    for data in tree.iter('busArrivalList'):
        remainSeat = data.findtext('remainSeatCnt1')
        if remainSeat == '-1':
            continue
        routeId = data.findtext('routeId')
        busnum = getbusnum(serviceKey, routeId)
        locationNo = data.findtext('locationNo1')
        nowtime = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        curs.execute("insert into bus_%s(date, remainSeat, locationNo) values ('%s', %s, %s)"%(busnum, nowtime,remainSeat, locationNo))

    conn.commit()
    conn.close()

def getbusnum(serviceKey, routeId):
    #임시로 API를 쓰긴했는데, 이제 db로 조회
    url = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=%s&routeId=%s'%(serviceKey, routeId)

    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)

    for data in tree.iter('routeName'):
        return data.text

if __name__ == '__main__':
    serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
    station = '08171'
    conn = sqlite3.connect('station.db')
    curs = conn.cursor()
    curs.execute('select stationId from stationId where station_num = "%s"'%(station))
    result = curs.fetchall()
    stationId = result[0][0]
    conn.close()
    try:
        while(True):
            getbusArrival(serviceKey, stationId)
            now = time.localtime()
            print("Success getData Time: %04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
            time.sleep(300)
    except Exception as e:
        now = datetime.now()
        with open("log.txt", "wb") as f:
            f.write("Error : %s\nTime : %s\n"%(e, now))

