from db_control import *
from datetime import datetime
import calendar

def getAvg(date1, date2): # date1부터 date2까지 2020-01-01 형식 
    db = dbcontrol('bus')
    db.execute("select * from 29_3500 where date > '%s' and date < '%s'"%(date1, date2))
    result = db.fetchall()

    avg_remainSeat = 0
    for i in result:
        #if i[0].strftime('%H') == '00':
        avg_remainSeat += int(i[2])
    return "%0.1f" %(avg_remainSeat/len(result))#print(a.strftime('%m-%d, %H:%M'))

if __name__ == "__main__":
    #월 입력해서 달 입력. calendar.monthrange(year, month)[1]
    result = []
    year = 2020
    month = 1 # 달 입력
    
    for day in range(1, calendar.monthrange(year, month)[1]+1):
        date1 = '%d-%02d-%02d %02d:%02d:%02d'%(year, month, day, 0, 0, 0)
        date2 = '%d-%02d-%02d %02d:%02d:%02d'%(year, month, day+1, 23, 59, 59)
        try:
            print('%s : %s' %(date1, getAvg(date1, date2)))
        except ZeroDivisionError:
            print('%s : No Data ' %(date1))
            #result.append(getAvg(date1, date2))

    #print(result)
# 버스별 추가 line 7
# 시간별 추가 line 12
