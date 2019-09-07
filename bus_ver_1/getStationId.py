"""
정류소 조회 서비스
keyword(정류소 번호 '-' 제외한 번호)로 stationId추출
"""
#-*- encoding: utf-8 -*-
import urllib.request
import xml.etree.ElementTree as et

serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
keyword = '08171'
url = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=%s&keyword=%s'%(serviceKey, keyword)

response = urllib.request.urlopen(url)

data=response.read()
tree = et.fromstring(data)


for data in tree.iter('busStationList'):
    region = data.findtext("regionName")
    if region == "의정부":
        stationId = data.findtext("stationId")
        print(region, stationId)
"""
try:
    with open("test.xml", "wb") as f:
        f.write(data)
except:
    print("Error")
print("Success")
"""