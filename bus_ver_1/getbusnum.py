#-*- coding: utf-8 -*-
"""
버스 노선 조회 서비스
gb202.doc 
"""

import urllib.request
import xml.etree.ElementTree as et

serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'

def getbusnum(servicekey, routeId):
    url = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=%s&routeId=%s'%(servicekey, routeId)

    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)

    for data in tree.iter('routeName'):
        print(data.tag, data.text)

getbusnum(serviceKey,236000176 )
"""

def getbusnum(serviceKey, routeId_list): #routeId로 노선번호 따옴, 버스 노선 조회 서비스
    name_dict = {}
    name_list = []
    for routeId in routeId_list:
        url = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=%s&routeId=%s'%(serviceKey, routeId)
        response = urllib.request.urlopen(url)
        data = response.read()
        tree = et.fromstring(data)
        for routeName in tree.iter('routeName'):
            name_list.append(routeName.text)
            name_dict[routeId] = routeName.text
    return name_list, name_dict
"""