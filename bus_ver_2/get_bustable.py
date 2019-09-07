#-*- encoding: utf-8 -*-
"""
3500번 버스의 station table 생성
"""

import urllib.request
import xml.etree.ElementTree as et
import sqlite3
import getbusnum

def get_bustable(routeId):
    serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
    url = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/station?serviceKey=%s&routeId=%s"%(serviceKey, routeId)

    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)
    #print(data.decode('utf8'))
    conn = sqlite3.connect('station_list.db')
    curs = conn.cursor()
    busnum = getbusnum.get_busnum(serviceKey, routeId)
    curs.execute('create table bus_%s(stationName TEXT, routeId INTEGER, stationId INTEGER, x TEXT, y TEXT, stationSeq INTEGER)'%(busnum))
    
    for data in tree.iter('busRouteStationList'):
        stationId = data.findtext("stationId")
        stationName = data.findtext("stationName")
        station_x = data.findtext("x")
        station_y = data.findtext("y")
        stationSeq = data.findtext("stationSeq")
        print(stationId, stationName)
        curs.execute("insert into bus_%s(stationName, routeID, stationId, x, y, stationSeq) values ('%s', %s, %s, '%s', '%s', %s)"%(busnum, stationName, routeId, stationId, station_x, station_y, stationSeq))

    conn.commit()
    conn.close()

get_bustable(234001426)