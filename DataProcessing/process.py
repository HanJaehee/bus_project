from db_control import *
from datetime import datetime
from list import *
import calendar

class Data:
    def __init__(self):
        self.db = dbcontrol('bus')
        self.busList = self.db.execute('select * from bus_info')
        self.year = 2020
    
    def getRow(self):
        cur = dbcontrol('busStationInfo')
        print(len(self.busList))
        #for i in busList:
            #cur.execute('select * from ')

    def execute(self, bus, date1, date2): # Take remainSeat from date1 to date2 in bus of DB bus
        return self.db.execute("select * from `%s` where date > '%s' and date < '%s'"%(bus, date1, date2))

    def createBusDB(self): #초기 db설정
        try:
            cur_time = dbcontrol('TimeAvg')
            cur_day = dbcontrol('DayAvg')
            cur_month = dbcontrol('MonthAvg')
        except pymysql.err.InternalError as e:
            print(e)
            """
            import mysql.connector
            mydb = mysql.connector.connect(
                host = "localhost",
                user = "wogml",
                passwd = "wogml23"
            )
            cur_db = mydb.cursor()
            cur_db.execute("create database")
            """

        for data in self.busList:
            routeName = data[0] + "_" + data[1]
            cur_time.execute("create table `%s`(date datetime, remainSeat FLOAT, stationSeq INT) " %(routeName))
            #cur_day.execute("create table `%s`(date date, remainSeat FLOAT, stationSeq INT) " %(routeName))
            #cur_month.execute("create table `%s`(date date, remainSeat FLOAT, stationSeq INT) " %(routeName)) #시간 안넣으려면 date 쓰자

        cur_time.close()
        cur_day.close()
        cur_month.close()

    def getMonthAvg(self, month): # get Month average remainSeat per bus
        cur_month = dbcontrol('MonthAvg')
        cur = dbcontrol('busStationInfo')
        date1 = datetime(self.year, month, 1, 0, 0, 0)
        date2 = datetime(self.year, month, calendar.monthrange(self.year, month)[1], 23, 59, 59) # from 1 to last day in month
        #print(date1)
        for data in self.busList:
            routeName = data[0] + '_' + data[1]
            #print(routeName)
            result = self.execute(routeName ,date1.strftime("%Y-%m-%d %H:%M:%S"), date2.strftime("%Y-%m-%d %H:%M:%S"))

            stationSeq_len = len(cur.execute('select * from `%s`' %(routeName))) # get stationSeq of routeName in busStationInfo
            avg = [0]*(stationSeq_len+1) # 배열 크기를 느려서 인덱스 그대로 가져감.
            avg_count = avg[:]

            #print(stationSeq_len)
            for data in result:
                try:
                    avg[int(data[3])] += int(data[2]) # 
                    avg_count[int(data[3])] += 1 # data[3] = stationSeq, data[2] = remainSeat
                except IndexError:
                    print("%s : %s <- Seq : %d" %(routeName, data[3], stationSeq_len))
            for i in range(stationSeq_len):
                if avg_count[i] == 0:
                    continue
                avg[i] /= avg_count[i]
            i=1
            for remainSeat in avg:
                if avg == 0:
                    continue
                #print(date1.strftime("%Y-%m-%d"))
                cur_month.execute("insert into `%s`(date, remainSeat, stationSeq) values ('%s', %0.1f, %d)" %(routeName, date1.strftime("%Y-%m-%d"), remainSeat, i))
                i+=1
        
        cur.close()
        cur_month.close()

    def getDayAvg(self, month): # get Day average remainSeat
        #date, remainSeat, stationSeq.
        cur_day = dbcontrol('DayAvg')
        cur = dbcontrol('busStationInfo')

        for data in self.busList:
            routeName = data[0] + '_' + data[1]
            stationSeq_len = len(cur.execute('select * from `%s`' %(routeName))) # get stationSeq of routeName in busStationInfo
            
            for day in range(1, calendar.monthrange(self.year, month)[1]+1): # get remainSeat data in one day.
                print("%s : %d " %(routeName, day))
                avg_list = [0] * (stationSeq_len+1) # 배열 크기 늘려서 인덱스 그대로
                avg_count = avg_list[:]                
                date1 = datetime(self.year, month, day, 0, 0, 0)
                date2 = datetime(self.year, month, day, 23, 59, 59)
                result = self.execute(routeName, date1.strftime("%Y-%m-%d %H:%M:%S"), date2.strftime("%Y-%m-%d %H:%M:%S"))
               
                for data in result:
                    try:
                        avg_list[int(data[3])] += int(data[2])
                        avg_count[int(data[3])] += 1
                    except IndexError:
                        print("%s : %d , stationSeq : %d" %(routeName, int(data[3]), stationSeq_len))

                    #print('%s : No Data' %(date1[:10]))
                print(avg_list)
                i = 1
                for data in avg_list:
                    if avg_count[i] == 0:
                        i+=1
                        continue
                    remainSeat = data/avg_count[i]
                    cur_day.execute("insert into `%s`(date, remainSeat, stationSeq) values('%s', %0.1f, %d)" %(routeName, date1.strftime("%Y-%m-%d"), remainSeat, i))
                    i+=1

        cur_day.close()
        cur.close()

    #자기소개에 추천시스템 추상적 요소 추가
    def getTimeAvg(self, month, day):
        cur_time = dbcontrol('TimeAvg')
        cur = dbcontrol('busStationInfo')

        for data in self.busList:
            routeName = data[0] + '_' + data[1]
            stationSeq_len = len(cur.execute('select * from `%s`' %(routeName)))
            
            date1 = datetime(self.year, month, day, 0, 0, 0)
            date2 = datetime(self.year, month, day, 23, 59, 59)
            result = self.execute(routeName, date1, date2)

            avg_list = []
            avg_count = []
            tmp = list(0 for x in range(24))
            for i in range(stationSeq_len+1):
                avg_list.append(tmp[:])
            for i in range(stationSeq_len+1): # avg_count = avg_list[:] print same result
                avg_count.append(tmp[:])

            for data in result:
                time = int(data[0].strftime("%H"))
                stationSeq = int(data[3])

                try:
                    avg_list[stationSeq][time] += int(data[2]) # remainSeat
                    avg_count[stationSeq][time] += 1
                except IndexError:
                    print("%s : %d" %(routeName, stationSeq_len))
            
            for stationSeq in range(1, stationSeq_len+1):
                for time in range(0,24):
                    if avg_count[stationSeq][time] == 0:
                        continue
                    remainSeat = avg_list[stationSeq][time]/avg_count[stationSeq][time]
                    time = datetime(self.year, month, day, time)
                    cur_time.execute("insert into `%s`(date, remainSeat, stationSeq) values('%s', %0.1f, %d)"%(routeName, time.strftime('%Y-%m-%d %H:%M'), remainSeat, stationSeq))

        cur_time.close()
        cur.close()

        print("Success getTimeAvg [+]")
        #print(avg_list)

        """
        for i in range(0, 24):
            if avg_count[i] == 0:
                continue
            avg_dict['%d-%02d-%02d %02d'%(self.year, month, day, i)] = avg_list[i]/avg_count[i]
        return avg_dict
        """

if __name__ == "__main__":
    a = Data()
    #a.getBusList()
    a.createBusDB()
    #a.getDayAvg(1)
    #a.getRow()
    #a.getMonthAvg(1)
    a.getTimeAvg(1, 4)




#월 입력해서 달 입력. calendar.monthrange(year, month)[1]

# 
#
# 버스별 추가 line 7
# 시간별 추가 line 12
# 시간이 안들어감 , 디비 대용량 삭제방법 강구 해결 : 2020-02-11