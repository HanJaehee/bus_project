#-*- coding:utf-8 -*-
from db_control import *
import urllib.request
import xml.etree.ElementTree as et
from list import *

class create_table: # ex . ('31', '8156', '233000258', '서울,의왕,화성')
    def __init__(self):
        self.serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'

    def createBusInfo(self):
        # info_list로 버스마다 경유하는 정류장들의 정보를 담은 테이블 생성
        # DB : busStationInfo // doc : GB202, No2.경유정류소목록조회
        curs = dbcontrol('bus')
        curs.execute('select * from bus_info')
        info_list = curs.fetchall()
        curs2 = dbcontrol('busStationInfo')

        for info in info_list:
            url = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/station?serviceKey=%s&routeId=%s"%(self.serviceKey, info[2])
            response = urllib.request.urlopen(url)
            result = response.read()
            tree = et.fromstring(result)
            routeName = info[1]
            
            #if "-" in routeName:
            #    routeName = routeName.replace("-", "\-")
            curs2.execute('create table `%s_%s`(stationName varchar(40), mobileNo INT, stationId INT, stationSeq INT, regionName varchar(10), districtCd INT, centerYn varchar(5), turnYn varchar(5),x varchar(20), y varchar(20))'%(info[0], routeName))
        
            for data in tree.iter('busRouteStationList'):
                stationId = data.findtext("stationId")
                mobileNo = data.findtext("mobileNo")
                regionName = data.findtext("regionName")
                turnYn = data.findtext("turnYn")
                centerYn = data.findtext("centerYn")
                districtCd = data.findtext("districtCd")
                stationName = data.findtext("stationName")
                station_x = data.findtext("x")
                station_y = data.findtext("y")
                stationSeq = data.findtext("stationSeq")

                if mobileNo == None:
                    curs2.execute("insert into `%s_%s`(stationName, stationId, stationSeq, regionName, districtCd , centerYn, turnYn, x, y) values ('%s', %s, %s, '%s', %s, '%s', '%s', '%s', '%s')"%(info[0], routeName, stationName, stationId, stationSeq ,regionName, districtCd , centerYn, turnYn, station_x, station_y))
                else:
                    curs2.execute("insert into `%s_%s`(stationName, mobileNo, stationId, stationSeq, regionName, districtCd , centerYn, turnYn, x, y) values ('%s', %s, %s, %s, '%s', %s, '%s', '%s', '%s', '%s')"%(info[0], routeName, stationName, mobileNo, stationId, stationSeq ,regionName, districtCd , centerYn, turnYn, station_x, station_y))
            print("name : %s" %(routeName))
        curs2.close()
        curs.close()
        print("[+] Success createbusinfo")

a = create_table()
a.createBusInfo()