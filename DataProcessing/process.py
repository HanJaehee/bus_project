from db_control import *
from datetime import datetime

db = dbcontrol('bus')
db.execute("select * from 29_3500 where date > '2019-12-01' and date < '2020-01-01'")
result = db.fetchall()

avg_remainSeat = 0
for i in result:
    if i[0].strftime('%H') == '00':
        avg_remainSeat += int(i[2])
print("%0.1f" %(avg_remainSeat/len(result)))
#print(a.strftime('%m-%d, %H:%M'))