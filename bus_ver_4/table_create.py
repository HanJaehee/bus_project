# -*- coding:utf-8 -*-
from db_control import *
import urllib.request
import xml.etree.ElementTree as et
import sys

class create_table:
    def __init__(self, stationNum):
        self.serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
        self.stationNum = stationNum
        #self.stationId = self.getstationId
        #self.routeId_list = self.getrouteId
        #self.createbusinfo
        #self.createbusremain

    def getstationId(self):
        # 정류소 조회 서비스, 정류소 번호(08-171, '-'빼고)로 해당 정류소 StationId 가져옴
        # doc : GB203, No2.정류소명/번호목록조회
        url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=%s&keyword=%s'%(self.serviceKey, self.stationNum)
        response = urllib.request.urlopen(url)
        data = response.read()
        tree = et.fromstring(data)

        for data in tree.iter('busStationList'):
            #region = data.findtext("regionName") #지역명은 일단은 의정부로 헀고, 추가시 지역명도 db에 포함
            stationId = data.findtext("stationId")
        print("[+] Success getstationId()")
        return stationId
    
    def getrouteId(self):
        # 해당 정류소의 모든 버스의 routeId, routeName, staOrder를 station_정류소번호 table에 저장
        # DB : station_info // doc : GB203, No1.정류소경유노선목록조회
        stationId = self.getstationId()
        url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=%s&stationId=%s'%(self.serviceKey, stationId)
        response = urllib.request.urlopen(url)
        data =response.read()
        tree = et.fromstring(data)
        routeId_list=[]
        curs = dbcontrol('station_info')
        #curs.execute('select EXISTS (select * from station_%s) as success'%(self.stationNum)) 안댐
        curs.execute('show tables like "station_%s"'%(self.stationNum))
        result = curs.fetchall()
        if result:
            print("이미 존재하는 정류장임")
            sys.exit(1)
        curs.execute('create table station_%s(routeId INT, routeName char(8), staOrder INT)'%(self.stationNum))
        curs.execute('insert into stationId(station_num, stationId) values("%s", %s)' %(self.stationNum, stationId))
        #ex) create station_08171, insert into ('3500', 34234234234)
        for data in tree.iter('busRouteList'):
            types = data.findtext("routeTypeName")
            if types == "직행좌석형시내버스" or types == "좌석형시내버스":
                routeId = data.findtext('routeId')
                routeId_list.append(routeId)
                routeName = data.findtext('routeName').replace("-", "\\-")
                print(routeName)
                curs.execute('insert into station_%s(routeId, routeName, staOrder) value (%s, "%s", %s)' %(self.stationNum, routeId, routeName, data.findtext('staOrder')))
        curs.commit()
        curs.close()
        print("[+] Success getrouteId()")
        return routeId_list
    
    def createbusinfo(self):
        # routeId_list로 버스마다 경유하는 정류장들의 정보를 담은 테이블 생성
        # DB : bus_station_info // doc : GB202, No2.경유정류소목록조회
        curs = dbcontrol('bus_station_info')
        curs2 = dbcontrol('station_info')
        routeId_list = self.getrouteId()
        for routeId in routeId_list:
            url = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/station?serviceKey=%s&routeId=%s"%(self.serviceKey, routeId)
            response = urllib.request.urlopen(url)
            data = response.read()
            tree = et.fromstring(data)
            curs2.execute('select routeName from station_%s where routeId=%s' %(self.stationNum, routeId))
            routeName = curs2.fetchall()
            #print(routeName)
            
            curs.execute('show tables like "bus_%s"'%(routeName[0][0])) #테이블 존재 유무 확인
            result = curs.fetchall()
            print("name : %s" %(routeName))
            if "-" in routeName:
                routeName = routeName.replace("-", "\\-")
            if not result:
                curs.execute('create table `bus_%s`(stationName varchar(40), routeId INT, stationId INT, x varchar(20), y varchar(20), stationSeq INT)'%(routeName[0][0]))
            
                for data in tree.iter('busRouteStationList'):
                    stationId = data.findtext("stationId")
                    stationName = data.findtext("stationName")
                    station_x = data.findtext("x")
                    station_y = data.findtext("y")
                    stationSeq = data.findtext("stationSeq")
                    curs.execute("insert into `bus_%s`(stationName, routeID, stationId, x, y, stationSeq) values ('%s', %s, %s, '%s', '%s', %s)"%(routeName[0][0], stationName, routeId, stationId, station_x, station_y, stationSeq))
        curs.commit()
        curs.close()
        print("[+] Success createbusinfo")

    def createbusremain(self):
        # 잔여좌석조회할 버스별 테이블 생성
        # DB: bus_remain
        curs = dbcontrol('station_info')
        curs2 = dbcontrol('bus_seat')
        curs.execute('select routeName from station_%s'%(self.stationNum))
        name_list = curs.fetchall()
        for name in name_list:
            curs2.execute('show tables like "bus_%s"' %(name[0]))
            result = curs2.fetchall()
            if not result:
                curs2.execute('create table `bus_%s`(date datetime, remainSeat INT, stationSeq INT)' %(name[0]))
            
        curs.commit()
        curs2.commit()
        curs.close()
        curs2.close()
