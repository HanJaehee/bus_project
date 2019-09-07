"""
버스 도착 정보 조회 서비스
doc : GB208
stationId로 해당 노선내 버스들 전부 추출
"""
#-*- encoding: utf-8 -*-
import urllib.request
import xml.etree.ElementTree as elemTree

def getrouteId(stationId):
    serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
    #stationId = '207000085'

    url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=%s&stationId=%s'%(serviceKey, stationId)

    response = urllib.request.urlopen(url)

    data=response.read()
    print(data.decode('utf-8'))
    tree = elemTree.fromstring(data.decode('utf-8'))
    #파일 일시 -> parse , string 형태일시 fromstring
    tree = tree.find('msgBody')

    for data in tree.iter('busArrivalList'):
        #result.append(data.text)
        routeId = data.find('routeId').text
        staOrder = data.find('staOrder').text
        print(routeId, staOrder)


getrouteId(207000085)