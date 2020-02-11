from db_control import *
from datetime import datetime
from list import *
import calendar

class Data:
    def __init__(self):
        self.db = dbcontrol('bus')
        self.busList = self.db.execute('select * from bus_info')
        self.year = 2019
    
    def getRow(self):
        cur = dbcontrol('busStationInfo')
        print(len(self.busList))
        #for i in busList:
            #cur.execute('select * from ')

    def execute(self, bus, date1, date2):
        return self.db.execute("select * from `%s` where date > '%s' and date < '%s'"%(bus, date1, date2))

    def createBusDB(self):
        cur_time = dbcontrol('TimeAvg')
        cur_day = dbcontrol('DayAvg')
        cur_month = dbcontrol('MonthAvg')

        for data in self.busList:
            routeName = data[0] + "_" + data[1]
            #cur_time.execute("create table `%s`(date datetime, remainSeat FLOAT, stationSeq INT) " %(routeName))
            #cur_day.execute("create table `%s`(date datetime, remainSeat FLOAT, stationSeq INT) " %(routeName))
            cur_month.execute("create table `%s`(date date, remainSeat FLOAT, stationSeq INT) " %(routeName)) #시간 안넣으려면 date 쓰자

        cur_time.close()
        cur_day.close()
        cur_month.close()

    def getMonthAvg(self, month):
        cur_month = dbcontrol('MonthAvg')
        cur = dbcontrol('busStationInfo')
        date1 = datetime(self.year, month, 1, 0, 0, 0)
        date2 = datetime(self.year, month, calendar.monthrange(self.year, month)[1], 23, 59, 59)
        print(date1)
        for data in self.busList:
            routeName = data[0] + '_' + data[1]
            #print(routeName)
            result = self.execute(routeName ,date1.strftime("%Y-%m-%d %H:%M:%S"), date2.strftime("%Y-%m-%d %H:%M:%S"))

            stationSeq_len = len(cur.execute('select * from `%s`' %(routeName)))
            avg = [0]*(stationSeq_len+1)
            avg_count = avg[:]

            #print(stationSeq_len)
            for data in result:
                try:
                    avg[int(data[3])-1] += int(data[2]) # 실제 stationSeq보다 -1 된거 인지
                    avg_count[int(data[3])-1] += 1
                except IndexError:
                    print("%s : %s <- Seq : %d" %(routeName, data[3], stationSeq_len))
            for i in range(stationSeq_len):
                if avg_count[i] == 0:
                    continue
                avg[i] /= avg_count[i]
            i=0
            for remainSeat in avg:
                if avg == 0:
                    continue
                #print(date1.strftime("%Y-%m-%d"))
                cur_month.execute("insert into `%s`(date, remainSeat, stationSeq) values ('%s', %0.1f, %d)" %(routeName, date1.strftime("%Y-%m-%d"), remainSeat, i))
                i+=1
        
        cur.close()
        cur_month.close()

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
    #a.getBusList()
    a.createBusDB()
    #a.getRow()
    a.getMonthAvg(12)
    """
    print(a.getMonthAvg(12))
    result = a.getDayAvg(11)
    print(result.keys())
    result = a.getTimeAvg(12,7)
    print(result.keys())
    """
    #월 입력해서 달 입력. calendar.monthrange(year, month)[1]

# 버스별 추가 line 7
# 시간별 추가 line 12
# 시간이 안들어감 , 디비 대용량 삭제방법 강구 해결 : 2020-02-11