#-*- coding: utf-8 -*-
"""
버스 노선 조회 서비스
gb202.doc 
"""

import urllib.request
import xml.etree.ElementTree as et

def get_busnum(servicekey, routeId):
    url = 'http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=%s&routeId=%s'%(servicekey, routeId)
    response = urllib.request.urlopen(url)
    data = response.read()
    tree = et.fromstring(data)

    for data in tree.iter('routeName'):
        return data.text