#S3 Wild, UV, Cisplatin
#S4 Wild TypeS
#S5 WIld types
#S6 Wild Cispra nop1
#Seasonのかわりには、27と165を変更。

#coding: UTF-8
import time
TimeMeasurement = time.time()

print("importing cv2...")
import cv2
print("・cv2                          "+ str(time.time() - TimeMeasurement) + 'sec')
print()

print("importing matplotlib.pyplot/numpy/"+ '\n'+ "Circle, Polygon, Rectangle/os/datetime/subprocess ...")
import matplotlib.pyplot as plt
print("・matplotlib.pyplot            "+ str(time.time() - TimeMeasurement) + 'sec')

import numpy as np
print("・numpy                        "+ str(time.time() - TimeMeasurement) + 'sec')

from matplotlib.patches import Circle, Polygon, Rectangle
print("・Circle, Polygon, Rectangle   "+ str(time.time() - TimeMeasurement) + 'sec')

import os
print("・os                           "+ str(time.time() - TimeMeasurement) + 'sec')

import datetime
print("・datetime                     "+ str(time.time() - TimeMeasurement) + 'sec')

import subprocess
print("・subprocess                   "+ str(time.time() - TimeMeasurement) + 'sec')
print()

print("importing scipy...")
from scipy import ndimage
print("・scipy                        "+ str(time.time() - TimeMeasurement) + 'sec')
print()

print("importing dropbox/requests/csv...")
import dropbox
print("・dropbox                      "+ str(time.time() - TimeMeasurement) + 'sec')

import requests
print("・requests                     "+ str(time.time() - TimeMeasurement) + 'sec')

import csv
print("・csv                          "+ str(time.time() - TimeMeasurement) + 'sec')
print()


global fname
global contours
global Contours_List
Contours_List=[]

#fname='Sample.jpg'

def check_the_date(): #ファイル名を撮影日時する
    global fname
    dates=datetime.datetime.now()
    exept_microsec=dates.strftime("%Y-%m-%d-%H-%M")
    print('[Today : %s]' % exept_microsec)
    fname='MassObservation_S6_'+exept_microsec+'.png'

def take_the_picture():
    global fname
    subprocess.getoutput('raspistill -w 400 -h 500 -n -o /home/pi/Desktop/%s' % fname) #ラズパイカメラで撮影した画像はデストップに一時保存(後でos.removeで削除する。)

def change_the_color():
    global fname
    frame=cv2.imread('/home/pi/Desktop/%s' % fname)
    # フレームをHSVに変換
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 取得する色の範囲を指定する
    lower_green=np.array([20, 50, 50])
    upper_green=np.array([70, 255, 255])
    # 指定した色に基づいたマスク画像の生成
    img_mask=cv2.inRange(hsv, lower_green, upper_green)
    # フレーム画像とマスク画像の共通の領域を抽出する。
    img_color=cv2.bitwise_and(frame, frame, mask=img_mask)
    #下の関数へ受け渡すためにデスクトップに一時保存(後でremoveで消します。)
    cv2.imwrite('/home/pi/Desktop/Green.png', img_color) #Green.pngは黒色背景にジェンマの画像があります。

def draw_the_contours():
    global fname
    global contours
    # 画像を読み込む。
    img = cv2.imread('/home/pi/Desktop/Green.png')
    os.remove('/home/pi/Desktop/Green.png')
    # 輪郭抽出する。
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, contours,hierarchy=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    fig, ax = plt.subplots(figsize=(6, 6))

    imgforshow=cv2.imread('/home/pi/Desktop/%s' % fname)#matplotlibするにはPicameraで撮影したカラー画像を使います。
    modified_imgforshow=ndimage.median_filter(imgforshow, 1)

    ax.imshow(modified_imgforshow)
    ax.axis('off')
    for i, cnt in enumerate(contours):
        cnt = np.squeeze(cnt, axis=1)  # (NumPoints, 1, 2) -> (NumPoints, 2)
        # 輪郭の点同士を結ぶ線を描画する。
        ax.add_patch(Polygon(cnt, color='b', fill=None, lw=2))
        # 輪郭の点を描画する。
        ax.plot(cnt[:, 0], cnt[:, 1], 'ro', mew=0, ms=4)
        # 輪郭の番号を描画する。
        ax.text(cnt[0][0], cnt[0][1], i, color='orange', size='20')
    #plt.show()
    plt.savefig('/home/pi/Desktop/pre_Area_%s' % fname) #matplotlibの画面をdropboxに直接保存する方法がわからなかったためデスクトップに一時保存します。
    subprocess.getoutput('convert -trim /home/pi/Desktop/pre_Area_%s /home/pi/Desktop/Area_%s' % (fname, fname))

def Get_Serial():
  # Extract serial from cpuinfo file
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

def Upload_on_Dropbox(API, Picname, RasPi_SerialNum):
    dbx = dropbox.Dropbox(API)
    dbx.users_get_current_account()
    Desktop_Picname=Picname
    Picname=Picname.split('.')
    Picname=str(Picname[0])+'_'+RasPi_SerialNum+'.png'
    f = open('/home/pi/Desktop/%s' % Desktop_Picname, 'rb')
    Area_or_not=Desktop_Picname.split('_')
    if Area_or_not[0]=='Area':
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_Filter_%s/%s' % (RasPi_SerialNum,Desktop_Picname)) #dropbox内のディレクトリを書く
    else:
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_unFilter_%s/%s' % (RasPi_SerialNum,Desktop_Picname)) #dropbox内のディレクトリを書く
    f.close()

def save_the_picture():
    global fname
    RasPi_SerialNum=Get_Serial()
    print('[RaspberryPi at %s]' % RasPi_SerialNum)
    if RasPi_SerialNum=='5324ee26':#5
        API_unFilter='pnEJapb3mPAAAAAAAAAA5ExZM4oZx2NfGumBApSJn1lT3zi9jbfn7Oc-1T4-NqpV'
        API_Area='pnEJapb3mPAAAAAAAAAA5VzQxrZiIlAAJRAAfJOGinpU6xD2zIMuktPuUdyobY8D'
    elif RasPi_SerialNum=='dd68d859':#6
        API_unFilter='pnEJapb3mPAAAAAAAAAA5moORyRk81XGbmpR9UAZAOROZ_jfoKjkylrZ7gn-P0fK'
        API_Area='pnEJapb3mPAAAAAAAAAA5_0TQoV1qcdJUhEUT98HgWvGJDCg-rCi-XXiJcTAe-Pd'
    elif RasPi_SerialNum=='cebabe86':#4
        API_unFilter='pnEJapb3mPAAAAAAAAAA6E9YgxmxuV1ZzWQICaXVBltXi3fZmWAr5M4J55PzAN14'
        API_Area='pnEJapb3mPAAAAAAAAAA6Wlsbr1NETPSM2Y0OlfYS9qlRgYsRbWeZaiT8Nv4Cq3e'
    elif RasPi_SerialNum=='712d5dde':#2
        API_unFilter='pnEJapb3mPAAAAAAAAAA6nNd0IwQnYBhLuW7GQNXV1cBEHmk8mjQHyxIIsdkXgum'
        API_Area='pnEJapb3mPAAAAAAAAAA63NDuOtdWn_7tYDg7GKbDI_l7nDqJipaJXokJSLZuwZ2'
    elif RasPi_SerialNum=='b6abc89e': #3
        API_unFilter='pnEJapb3mPAAAAAAAAAA7s6P0bPCTA9P81ZZP7R52ThXAkxDRqzgYqxtLQ-GM-wk'
        API_Area='pnEJapb3mPAAAAAAAAAA7X8YFACiPL1uNJJF5uTKZS2H32OLjIuCsbwln_xzkTS0'
    elif RasPi_SerialNum=='b4abbd7a': #1
        API_unFilter='pnEJapb3mPAAAAAAAAAA74vXf_Nj6crHubBynPX_ZSwB_WMpghR8gye2n6zWRmTa'
        API_Area='pnEJapb3mPAAAAAAAAAA8KPLYjE4QVoqfdbG4xV8Ijre0Jwxxd94PLXkZQeYJe5I'
    elif RasPi_SerialNum=='c310a350': #7
        API_unFilter='pnEJapb3mPAAAAAAAAAA8Z_DIcE5TrkhkYWB8fY3GOFmz1rndz4LrkUFtNLaezwU'
        API_Area='pnEJapb3mPAAAAAAAAAA8mK2hcnXVe_w0AnMcT6_5-iItrxcBd3vdBTLWBUtoSJi'
    elif RasPi_SerialNum=='5ae9b47f': #8
        API_unFilter='pnEJapb3mPAAAAAAAAABD5j497IjWUpvKkHup8EAamyIKyfTTJLEQkuz5BBTokhu'
        API_Area='pnEJapb3mPAAAAAAAAABDn1HIdTjVeMU5fid_TaUhqksALt3l1QJZ5-9t3H5DHHO'
    else:
        return

    Upload_on_Dropbox(API_unFilter, fname, RasPi_SerialNum) #Dropbox内に保存 ノーマルな写真
    Upload_on_Dropbox(API_Area, 'Area_%s' % fname, RasPi_SerialNum) #輪郭を記述した写真

def send_message(Picname_LINE):
    global Contours_List
    url = "https://notify-api.line.me/api/notify"   #line notifyでラズパイからlineに画像を送信
    token = '2Rm15NEZNBO8A8kLZHAmKXBAk4fnwOnxQMJCknwdw4p'   #lineのtoken
    headers = {"Authorization" : "Bearer "+ token}
    RasPi_SerialNumber=Get_Serial()
    RasPi_Number='[picamera_%s]' % RasPi_SerialNumber
    Area_7=''
    j=0
    for i in Contours_List:
        Area_7=Area_7+str(j)+'_'+str(i)+'\n'
        j+=1
    message =  RasPi_Number+ Picname_LINE + '\n' + '面積の記録成功です。\n'+Area_7
    payload = {"message" :  message}
    files = {"imageFile": open("/home/pi/Desktop/%s" % Picname_LINE, "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。
    r = requests.post(url ,headers = headers ,params=payload, files=files)
    #os.remove("/home/pi/Desktop/%s" % fname)

def calculate_the_Area():
    global contours
    global Contours_List
    RasPi_SerialNum=Get_Serial()
    #file=open('/home/pi/Desktop/rasp-ge/beginner/Assets/Assets_Output/Area_Record_%s.txt' % RasPi_SerialNum, mode='a')#open()のaモードは追記するモード
    #file.write('%s' % fname)
    #面積を求める
    Date=datetime.date.today()
    Contours_List.append(Date)
    for i, cnt in enumerate(contours):
        # 輪郭の面積を計算する。
        area = cv2.contourArea(cnt)
        #file.write('contour: {}, area: {}'.format(i, area))
        Contours_List.append(area)
        print('contour: {}, area: {}'.format(i, area))
    #S3 file.write('\n')

    with open('/home/pi/Desktop/rasp-ge/beginner/Assets/Assets_Output/Area_Record_S6_%s.csv' % RasPi_SerialNum, 'a') as f:
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Contours_List)

    Area_Fname='Area_'+fname
    send_message(Area_Fname)

def finish_program():
    os.remove('/home/pi/Desktop/pre_Area_%s' % fname)
    os.remove('/home/pi/Desktop/Area_%s' % fname) #Dropboxに保存したため削除。
    os.remove('/home/pi/Desktop/%s' % fname)

def main(TimeMeasurement):
    print("Check date...")
    check_the_date()
    print("Check date Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Taking Picture... ")
    take_the_picture()
    print("Take Picture Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Finding Green...")
    change_the_color()
    print("Found Leaves!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Drowing Contours...")
    draw_the_contours()
    print("Draw Contours!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Saving Picture...")
    save_the_picture()
    print("Saved Pictures!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Calculating the Area...")
    calculate_the_Area()
    print("Calculation Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("finish program...")
    finish_program()
    print("Everything is fine!!! Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')

if __name__ == '__main__':
    main(TimeMeasurement)
