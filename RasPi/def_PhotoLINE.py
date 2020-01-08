#coding:UTF-8
import datetime
from time import sleep
import requests
import subprocess
import os

def check_the_date():
    dates=datetime.datetime.now()
    exept_microsec=dates.strftime("%Y-%m-%d-%H時%M分")
    fname='Week2_'+exept_microsec+'.jpg'

    return fname

def take_the_picture(fname):
    subprocess.getoutput('raspistill -w 400 -h 500 -n -o ../../%s' % fname)

def get_Serial():# Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line[0:6]=='Serial':
          cpuserial = line[18:26]
      f.close()
    except:
      cpuserial = "ERROR000000000"

    return cpuserial

def send_message(fname):
    url = "https://notify-api.line.me/api/notify"   #line notifyでラズパイからlineに画像を送信
    token = '2Rm15NEZNBO8A8kLZHAmKXBAk4fnwOnxQMJCknwdw4p'   #lineのtoken
    headers = {"Authorization" : "Bearer "+ token}
    RasPi_SerialNumber=get_Serial()
    RasPi_Number='[picamera_%s]' % RasPi_SerialNumber
    message =  RasPi_Number+ fname + '\n' + 'ラボ_ゼニゴケ観察'
    payload = {"message" :  message}
    files = {"imageFile": open("../../%s" % fname, "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。
    r = requests.post(url ,headers = headers ,params=payload, files=files)
    os.remove("/home/pi/Desktop/%s" % fname)

def main():
    fname=check_the_date()
    take_the_picture(fname)
    send_message(fname)

if __name__ == '__main__':
    main()
