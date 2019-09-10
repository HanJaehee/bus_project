import urllib.request
import xml.etree.ElementTree as etree

serviceKey = 'CB%2Bo3%2FmVKJCSotkzZYDb7Ed%2BCi1ONj7Mmsmb5PqxzJ2A3OVmxuPDHzmxHPZOuw2IE%2B93CiUINtOioysJJdkBSQ%3D%3D'
stationId = 207000085
routeId = '236000176'
url = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=%s&stationId=%s'%(serviceKey, stationId)
response = urllib.request.urlopen(url)
data = response.read()
tree = etree.fromstring(data)

for data in tree.iter('busArrivalList'):
    for datas in data.iter("routeId"):
        if data.findtext("routeId") == routeId:
            remainSeat = data.findtext('remainSeatCnt1')
            locationNo = data.findtext('locationNo1')

print("Seat : %s, locationNo : %s" %(remainSeat, locationNo))
