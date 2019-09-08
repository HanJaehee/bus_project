#-*- coding:utf-8 -*-
import urllib.request
import xml.etree.ElementTree as et
import time, sys
from datetime import datetime
from db_control import *

class getdata:
    def __init__(self, stationNum):
        self.serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'

    def remainSeat(self, stationId):
        url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=%s&stationId=%s'%(self.serviceKey, stationId)
        response = urllib.request.urlopen(url)
        data = response.read()
        tree = et.fromstring(data)
        conn = dbcontrol
            