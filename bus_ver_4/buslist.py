#bus_info 에 버스정보 넣는다.
from list import *
import pymysql
import urllib.request
import xml.etree.ElementTree as et
from db_control import *

bus_list=[]
key = "CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D"
db = dbcontrol('bus')
for num in area_bus:
    len_num = len(num)
    areaId = area_id[num[0]]
    for i in range(1, len_num):
        keyword=num[i]
        bus_num = areaId+"_"+keyword
        bus_list.append(bus_num)
        url = "http://openapi.gbis.go.kr/ws/rest/busrouteservice/area?serviceKey=%s&areaId=%s&keyword=%s"%(key, areaId, keyword)
        response = urllib.request.urlopen(url)
        data = response.read()
        tree = et.fromstring(data)
        temp = []
        for data in tree.iter('busRouteList'):
            regionName = data.findtext('regionName')
            routeId = data.findtext('routeId')
            routeName = data.findtext('routeName')
            #rint("regionName=%s\nrouteId=%s\nrouteName=%s"%(regionName, routeId, routeName))
            temp.append([routeName, routeId, regionName])
            print(temp)
        db.execute("insert into `bus_info`(areaId, routeName, routeId, regionName) values('%s','%s','%s','%s')"%(areaId, temp[0][0], temp[0][1], temp[0][2]))
        del temp

#create table bus_info(areaId varchar(3), routeName varchar(8), routeId varchar(10), regionName varchar(20));

for bus in bus_list:
    db.execute("create table `%s`(date datetime, plateType varchar(2), remainSeat varchar(3), stationSeq varchar(3))"%(bus))
print(bus_list)
db.commit()
db.close()
