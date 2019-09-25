from table_create import * 

tq = create_table("40115")
tq1 = create_table("08171")
tq2 = create_table("11105")

for i in [tq, tq1, tq2]:
    i.createbusinfo()
    i.createbusremain()

#08-171, 40-115, 11-105
