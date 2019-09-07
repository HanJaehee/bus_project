import xml.etree.ElementTree as elemTree

bus_num = 3500
tree = elemTree.parse("test.xml")
for data in tree.iter('stationId'):
    print(data.text)
"""
#point = tree.find('./busStationList[@districtCd="2"]')

for data in root.iter("stationId"):
    print(data.text)
"""