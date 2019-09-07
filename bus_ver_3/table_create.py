# -*- coding:utf-8 -*-
import pymysql
import urllib.request
import xml.etree.ElementTree as et

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
    
class create_table:
    def __init__(self, stationNum):
        self.serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
        self.stationNum = stationNum

    def getstationId(self):
        # 정류소 조회 서비스, 정류소 번호(08-171, '-'빼고)로 해당 정류소 StationId 가져옴
        # doc : GB203, No2.정류소명/번호목록조회
        url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=%s&keyword=%s'%(self.serviceKey, stationNum)
        response = urllib.request.urlopen(url)
        data = response.read()
        tree = et.fromstring(data)

        for data in tree.iter('busStationList'):
            region = data.findtext("reginName") #지역명은 일단은 의정부로 헀고, 추가시 지역명도 db에 포함
            if region == "의정부":
                stationId = data.findtext("stationId")
        self.stationId = stationId
        print("[+] Success getstationId()")
    
    def getrouteId(self):
        # 해당 정류소의 모든 버스의 routeId, routeName, staOrder를 station_정류소번호 table에 저장
        # DB : station_info // doc : GB203, No1.정류소경유노선목록조회
        url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=%s&stationId=%s'%(self.serviceKey, self.stationId)
        response = urllib.request.urlopen(url)
        data =response.read()
        tree = et.fromstring(data)
        routeId_list=[]
        curs = dbcontrol('station_info')

        curs.execute('create table station_%s(routeId INT, routeName char(4), staOrder INT)'%(self.stationNum))
        curs.execute('insert into stationId(station_num, stationId) values("%s", %s)'%(self.stationNum, self.stationId))
        #ex) create station_08171, insert into ('3500', 34234234234)
        for data in tree.iter('busRouteList'):
            types = data.findtext("routeTypeName")
            if types == "직행좌석형시내버스":
                routeId = data.findtext('routeId')
                routeId_list.append(routeId)
                curs.execute('insert into station_%s(routeId, routeName, staOrder) value (%s, "%s", %s)' %(self.stationNum, routeId, data.findtext('routeName'), data.findtext('staOrder')))
        curs.commit()
        curs.close()
        print("[+] Success getrouteId()")
        return routeId_list
    
    def createbusinfo(self):
        # routeId_list로 버스마다 경유하는 정류장들의 정보를 담은 테이블 생성
        # DB : bus_station_info // doc : GB202, No2.경유정류소목록조회
        routeId_list = self.getrouteId()
        curs = dbcontrol('bus_station_info')
        curs2 = dbcontrol('station_info')
        for routeId in routeId_list:
            url = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/station?serviceKey=%s&routeId=%s"%(self.serviceKey, routeId)
            response = urllib.request.urlopen(url)
            data = response.read()
            tree = et.fromstring(data)
            curs2.execute('select routeName from station_%s where routeId=%s' %(self.stationNum, routeId))
            routeName = curs2.fetchall()
            curs.execute('create table bus_%s(stationName varchar(30), routeId INT, stationId INT, x varchar(20), y varchar(20), stationSeq INT)'%(routeName))

            for data in tree.iter('busRouteStationList'):
                stationId = data.findtext("stationId")
                stationName = data.findtext("stationName")
                station_x = data.findtext("x")
                station_y = data.findtext("y")
                stationSeq = data.findtext("stationSeq")
                curs.execute("insert into bus_%s(stationName, routeID, stationId, x, y, stationSeq) values ('%s', %s, %s, '%s', '%s', %s)"%(busnum, stationName, routeId, stationId, station_x, station_y, stationSeq))
        curs.commit()
        curs.close()
        print("[+] Success createbusinfo")

    def createbusremain(self):
        # 잔여좌석조회할 버스별 테이블 생성
        # DB: bus_remain
        curs = dbcontrol('station_info')
        curs2 = dbcontrol('bus_remain')
        curs.execute('select routeName from station_%s'%(self.stationNum))
        name_list = curs.fetchall()
        for name in name_list:
            curs2.execute('create table bus_%s(date datetime, remainSeat INT, locationNo INT)' %(name[0]))
        curs.commit()
        curs2.commit()
        curs.close()
        curs2.close()
