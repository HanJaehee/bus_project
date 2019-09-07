import sqlite3

conn = sqlite3.connect('company.db')
curs = conn.cursor()

curs.execute('create table test_table(date text, remainSeat integer)')
curs.execute("insert into test_table('2019-08-24', 32)")
conn.commit()
conn.close()