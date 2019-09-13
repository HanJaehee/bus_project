from get_remainseat import *
import time

tq = getdata('08171')
tq2 = getdata('40115')
#try:
while(True):
    #tq.remainSeat()
    tq2.remainSeat()
    now = time.localtime()
    print("[+] Success getData Time: %04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
    time.sleep(300)
"""
except Exception as e:
    now = datetime.now()
    print(e)
"""