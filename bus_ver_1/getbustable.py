#-*- coding:utf-8 -*-
"""
정류소 조회 서비스
doc : GB203
버스정류장테이블과 버스테이블 생성
"""
import urllib.request
import xml.etree.ElementTree as et
import sqlite3

def getStationId(serviceKey, station):
    #정류소 조회 서비스, 정류소 번호(08-171, '-'빼고)로 해당 정류소 StationId 가져옴
    url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=%s&keyword=%s'%(serviceKey, station)
    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)
    #station_list = [] 지역별로 같은 정류장 번호는 없으므로 list x

    for data in tree.iter('busStationList'):
        region = data.findtext("regionName")
        if region == "의정부":
            stationId = data.findtext("stationId")

    return stationId

def getrouteId(serviceKey,stationId,station):
    """
    해당 정류소의 모든 버스의 routeId, routeName, staOrder를 station_정류소번호 table에 저장
    """
    url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=%s&stationId=%s'%(serviceKey, stationId)
    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)
    conn = sqlite3.connect('station.db')
    curs = conn.cursor()
    routeId_list = []

    curs.execute('create table station_%s(routeId integer, routeName text, staOrder integer)'%(station))
    curs.execute('insert into stationId(station_num, stationId) values("%s",%s)'%(station, stationId))
    #정류장 번호와 stationId DB에 저장
    for data in tree.iter('busRouteList'):
        types = data.findtext("routeTypeName")
        if types == "직행좌석형시내버스":
            routeId = data.findtext('routeId')
            routeId_list.append(routeId)
            curs.execute('insert into station_%s(routeId, routeName, staOrder) values (%s,"%s",%s)' %(station, routeId, data.findtext('routeName'), data.findtext('staOrder')))
    conn.commit()
    conn.close()
    return routeId_list

def createbustable(station):
    #MariaDB로 바꺼야댐
    conn_bus = sqlite3.connect('bus.db')
    conn_stat = sqlite3.connect('station.db')
    curs_bus = conn_bus.cursor()
    curs_stat = conn_stat.cursor()
    curs_stat.execute('select routeName from station_%s'%(station))
    name_list = curs_stat.fetchall()
    for name in name_list:
        curs_bus.execute('create table bus_%s(date datetime, remainSeat integer, locationNo integer)'%(name[0]))
    conn_bus.commit()
    conn_stat.commit()
    conn_bus.close()
    conn_stat.close()

if __name__ == '__main__':
    serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
    stationNum = '08171' #신동초등학교
    """
    정류소번호(=stationNum)로 getStationId함수로 stationId 얻은후,
    해당 정류소를 지나가는 버스들의 routId를 getrouteId station.db에 저장
    그리고 createbustable로 station.db내의 station_num테이블에서 routeName(버스번호)를 가져와
    bus.db에 각 버스 번호 table 생성(여기에 시간, 잔여좌석, localtionNo저장)
    """
    stationId = getStationId(serviceKey, stationNum)
    routeId_list = getrouteId(serviceKey, stationId,stationNum)
    createbustable(stationNum)
