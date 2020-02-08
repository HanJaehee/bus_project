from db_control import *
from datetime import datetime
import calendar

class Data:
    def __init__(self):
        self.db = dbcontrol('bus')
        result = self.db.execute('select areaid, routeName, routeId from bus_info where areaid=29')

        self.bus = '29_3500'
        self.year = 2019

    def execute(self, date1, date2):
        self.db.execute("select * from %s where date > '%s' and date < '%s'"%(self.bus, date1, date2))
        return self.db.fetchall()

    def getMonthAvg(self, month):
        date1 = '%d-%02d-%02d %02d:%02d:%02d'%(self.year, month, 1, 0, 0, 0)
        date2 = '%d-%02d-%02d %02d:%02d:%02d'%(self.year, month, calendar.monthrange(self.year, month)[1], 23, 59, 59)
        result = self.execute(date1, date2)
        
        avg = 0
        for i in result:
            avg += int(i[2])
        return "%0.1f" %(avg/len(result))

    def getDayAvg(self, month):
        avg_dict = {}
        for day in range(1, calendar.monthrange(self.year, month)[1]+1):
            date1 = '%d-%02d-%02d %02d:%02d:%02d'%(self.year, month, day, 0, 0, 0)
            date2 = '%d-%02d-%02d %02d:%02d:%02d'%(self.year, month, day, 23, 59, 59)
            result = self.execute(date1, date2)
            
            avg = 0
            for i in result:
                avg += int(i[2])
            try:
                avg_dict[date1[:10]] = avg/len(result)
                #print('%s : %3f' %(date1[:10], avg/len(result)))
            except ZeroDivisionError:
                pass
                #print('%s : No Data' %(date1[:10]))
        return avg_dict
    #자기소개에 추천시스템 추상적 요소 추가
    def getTimeAvg(self, month, day):
        date1 = '%d-%02d-%02d %02d:%02d:%02d'%(self.year, month, day, 0, 0, 0)
        date2 = '%d-%02d-%02d %02d:%02d:%02d'%(self.year, month, day, 23, 59, 59)
        result = self.execute(date1, date2)

        avg_list = [0]*24
        avg_count = [0]*24
        avg_dict = {}
        for i in result:
            index = int(i[0].strftime("%H"))
            avg_list[index] += int(i[2])
            avg_count[index] += 1
        for i in range(0, 24):
            if avg_count[i] == 0:
                continue
            avg_dict['%d-%02d-%02d %02d'%(self.year, month, day, i)] = avg_list[i]/avg_count[i]
        return avg_dict

if __name__ == "__main__":
    a = Data()
    print(a.getMonthAvg(12))
    result = a.getDayAvg(11)
    print(result.keys())
    result = a.getTimeAvg(12,7)
    print(result.keys())
    #월 입력해서 달 입력. calendar.monthrange(year, month)[1]

# 버스별 추가 line 7
# 시간별 추가 line 12
