from time import ctime
import os
import ntplib

c = ntplib.NTPClient()
response = c.request('ntp.nict.jp', version=3)

print(response.offset)
#-0.143156766891
print(response.version)
#3
now=ctime(response.tx_time)
print(now)
# 'Sun May 17 09:32:48 2009'
print(ntplib.leap_to_text(response.leap))
# 'no warning'
print(response.root_delay)
# 0.0046844482421875
print(ntplib.ref_id_to_text(response.ref_id))
# 193.190.230.66

now_year = now[20:24]
print(now_year)

now_day = now[8:10]
print(now_day)

now_month = now[4:7]
if now_month=="Jan":
    now_month=1
if now_month=="Feb":
    now_month=2
if now_month=="Mar":
    now_month=3
if now_month=="Apr":
    now_month=4
if now_month=="May":
    now_month=5
if now_month=="Jun":
    now_month=6
if now_month=="Jul":
    now_month=7
if now_month=="Aug":
    now_month=8
if now_month=="Sep":
    now_month=9
if now_month=="Oct":
    now_month=10
if now_month=="Nov":
    now_month=11
if now_month=="Dec":
    now_month=12
print(now_month)

now_time = now[11:19]
print(now_time)

os.system("sudo date -s"+" "+"'"+str(now_year)+"-"+str(now_month)+"-"+str(now_day)+" "+str(now_time)+"'")
