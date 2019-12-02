import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
import os
import datetime
import subprocess
from scipy import ndimage
import dropbox
import csv
import requests
import pandas as pd
import math
import re

global fname

def check_the_date(): #ファイル名を撮影日時する
    global fname
    dates=datetime.datetime.now()
    exept_microsec=dates.strftime("%Y-%m-%d-%H-%M")
    print('[Today : %s]' % str(exept_microsec))
    fname='MassObservation_S6_'+exept_microsec+'.png'

def take_the_picture(): #写真を撮影する
    global fname
    #subprocess.getoutput('raspistill -w 400 -h 500 -n -o /home/pi/Desktop/%s' % fname) #ラズパイカメラで撮影した画像はデストップに一時保存(後でos.removeで削除する。) #RaspberryPi
    #print('ex) Sample.jpeg') #Mac
    fname='Sample.jpeg' #Mac

def change_the_color(): #カラー画像を緑&黒の画像にする
    global fname
    print("ファイル名：", fname)
    frame=cv2.imread('Assets/Assets_Input/%s' % fname)
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
    cv2.imwrite('../../Green.png', img_color) #Green.pngは黒色背景にジェンマの画像があります。

def Record_Area(Contours_List_reversed): #とりあえず従来の方法で面積データを保存する
    csv_List=[]
    for Elements in Contours_List_reversed:
        [Contours_num, Contours_Area]=Elements
        csv_List.append(Contours_Area)
    with open('Assets/Assets_Output/Area_Record_on_Mac.csv', 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(csv_List)

def calculate_the_Area(contours): #輪郭(cnt)から面積を導出する
    Date=datetime.date.today()
    Contours_List = []
    #面積を求める
    for i, cnt in enumerate(contours):
        # 輪郭の面積を計算する。
        area = cv2.contourArea(cnt)
        #file.write('contour: {}, area: {}'.format(i, area))
        sub_Contours_List=[]
        num=(len(contours)-1)-i #新しいラベリング処理方法に合わせてサンプルの上から番号を添付するように変更。
        #print(num)
        sub_Contours_List.append(num)
        sub_Contours_List.append(area)
        #print(sub_Contours_List)
        Contours_List.append(sub_Contours_List)
        #print('contour: {}, area: {}'.format(i, area))
    #Contours_List_reversed=Contours_List[::-1]
    print("今日の日付：", Date)
    Contours_List.insert(0,[str(Date),str(Date)]) #一番最初に日付を挿入。
    print("-",len(contours), "個検出しました。-")
    #print("面積(輪郭)：", Contours_List)
    Record_Area(Contours_List)

    return Contours_List

def draw_the_contours(): #輪郭を描写する
    global fname
    global contours
    #↓画像を読み込む。
    img = cv2.imread('../../Green.png') #デスクトップ
    os.remove('../../Green.png') #デスクトップ
    #↓面積導出関数へ渡す。
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #緑色を白、背景を黒にした二値化をする。(そうしないと輪郭抽出や他のOpenCVの関数で扱いずらい。)
    contours,hierarchy=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    Conventional_Area_List = []
    Conventional_Area_List=calculate_the_Area(contours) #def

    #輪郭をプロットする部分。
    frame=cv2.imread('../../rasp-ge/beginner/Assets/Assets_Input/%s' % fname) #生画像 #ディレクトリはデスクトップ
    modified_imgforshow=ndimage.median_filter(frame, 1)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(modified_imgforshow)
    ax.axis('off')
    for j, cnt in enumerate(contours):
        cnt = np.squeeze(cnt, axis=1)
        ax.add_patch(Polygon(cnt, color='r', fill=None, lw=0.5))
        #ax.text(cnt[0][0], cnt[0][1], j, color='orange', size='20')
    #plt.savefig('../../pre_Contours_on_%s' % fname, bbox_inches='tight') #デスクトップ
    plt.savefig('../../Contours_on_%s' % fname, bbox_inches='tight') #デスクトップ
    #subprocess.getoutput('convert -trim ../../pre_Contours_on_%s ../../Contours_on_%s' % (fname, fname)) #デスクトップ
    #os.remove('../../pre_Contours_on_%s' % fname) #デスクトップ

    return Conventional_Area_List, contours

#csvファイルに保存されている直近の日付のデータを取り出す。
def pull_the_latest_Coordinates(Today_Coordinates_List):
    try: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/Area_Record_Test_on_Mac.csv",sep=",")
    except:
        Header_Length=len(Today_Coordinates_List)
        Header=[]
        for i in range(int(len(Today_Coordinates_List))):
            if i == 0:
                Header.append("Date")
            else:
                Header.append("Area_%s" % i)
                Header.append("Coordinates_%s" % i)
        print(Header)
        Header=["Date","Area_1","Coordinates_1","Area_2","Coordinates_2","Area_3","Coordinates_3","Area_4","Coordinates_4","Area_5","Coordinates_5","Area_6","Coordinates_6","Area_7","Coordinates_7"]
        with open('Assets/Assets_Output/Area_Record_Test_on_Mac.csv', 'a') as f: #Mac
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerow(Header)
            return "No_Data"

    #print(csv_input) #csvファイルを表示
    #print(list(csv_input["Date"])) #csvファイルに保存されている日付の一覧を表示
    Date_List=list(csv_input["Date"])

    YESTERDAY=Date_List[0]
    [YESTERDAY_YEAR, YESTERDAY_MONTH, YESTERDAY_DAY] = str(YESTERDAY).split('-')
    #print("START_DAY：", YESTERDAY_DAY) #csvファイルにある当日から直近の日付を調べる。まずは一番早い日から。

    TODAY=datetime.date.today()
    [TODAY_YEAR, TODAY_MONTH, TODAY_DAY] = str(TODAY).split('-')
    DataFrame_Column_num=1 #データフレームは、ヘッダーが行0番目だから、Date_List[0]に入る日付はデータフレームでいうと行1番目になる。リスト⇄データフレーム間の調整。
    for Date in Date_List:
        [YEAR, MONTH, DAY] = str(Date).split('-')
        #print(YESTERDAY_DAY, DAY, DAY, TODAY_DAY)
        if (int(YESTERDAY_DAY) < int(DAY)) and (int(DAY) < int(TODAY_DAY)):
            YESTERDAY=Date
            DataFrame_Column_num=DataFrame_Column_num+1
    #print("YESTERDAY：",YESTERDAY) #最終的に出されたcsvファイルにある当日から直近の日付を表示。
    #print(DataFrame_Column_num) #↑何行目かを表示。
    a=csv_input.iloc[DataFrame_Column_num-1,]
    #print(a)
    #print(a.iloc[1,])
    Latest_Coordinates_List=[]
    Latest_Coordinates_List.insert(0,a["Date"])
    for i in range(int(len(csv_input.columns)/2)):
        i=i+1
        #print(a["Coordinates_%s" % i])
        Latest_Coordinates_List.append(a["Coordinates_%s" % i])
    #print("Yesterday : ", Coordinates_List)
    return Latest_Coordinates_List

def Compare_these_Coordinates(Today_Coordinates_List):
    Yesterday_Coordinates_List=pull_the_latest_Coordinates(Today_Coordinates_List)
    if Yesterday_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        return "No_Data"

    else:
        print("昨日の座標 : ", Yesterday_Coordinates_List)
        print("今日の座標 : ", Today_Coordinates_List)
        Checked_Today_Coordinates_List=[]
        for k in range(int(len(Today_Coordinates_List)-1)):
            Checked_Today_Coordinates_List.append("None")
            #print(Checked_Today_Coordinates_List)
        for i in range(int(len(Today_Coordinates_List)-1)): #日付もリストに含まれてるから-1する
            i=i+1
            #print(Today_Coordinates_List[i])
            [Today_X,Today_Y]=Today_Coordinates_List[i].split(",")
            right_num=1000
            nearest_r=1000
            for j in range(int(len(Yesterday_Coordinates_List)-1)): #日付もリストに含まれてるから-1する
                j=j+1
                #print(Yesterday_Coordinates_List[j])
                [Yesterday_X,Yesterday_Y]=str(Yesterday_Coordinates_List[j]).split(",")
                #print(Today_X,Today_Y,"/",Yesterday_X,Yesterday_Y)
                a=int(Today_X)-int(Yesterday_X)
                b=int(Today_Y)-int(Yesterday_Y)
                r=math.sqrt(a*a+b*b)
                #print("距離:", int(r))
                if 0< int(r) and int(r) < int(nearest_r):
                    right_num=j
                    nearest_r=r
                    #print("変更：",right_num)
                elif r==0:
                    right_num=j
                    nearest_r=r
                    #print("変更：",right_num)
                    break
            #print("最終：",right_num)
            #print("Today_Coordinates_List", Today_Coordinates_List[i])
            #print("配列リスト　途中経過 : ", Checked_Today_Coordinates_List)
            Checked_Today_Coordinates_List[right_num-1]=Today_Coordinates_List[i]
        #print("適正な座標：",Checked_Today_Coordinates_List)

        while 'None' in Checked_Today_Coordinates_List:
            Checked_Today_Coordinates_List.remove('None')

        #Checked_Today_Coordinates_List=Checked_Today_Coordinates_List[::-1]
        Checked_Today_Coordinates_List.insert(0,Today_Coordinates_List[0])

        return Checked_Today_Coordinates_List

def Labeling(Conventional_Area_List, contours): #画像上にデータを付与する
    global fname
    frame_with_contours=cv2.imread('../../Contours_on_%s' % fname) #デスクトップ
    Date=datetime.date.today()

    Today_Coordinates_List=[]  #昨日と今日の中心座標を比較する用
    for Elements in contours:
        mu = cv2.moments(Elements)
        x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
        Coordinates=str(x)+","+str(y)
        Today_Coordinates_List.append(Coordinates)
    #Today_Coordinates_List=Today_Coordinates_List[::-1]
    Today_Coordinates_List.insert(0,str(Date))

    #とりあえず今日の面積と中心座標をリストにする。
    Today_Record_List_Test=[] #csvファイルに保存する用
    Today_Dict={}
    #print(len(Today_Coordinates_List), len(Conventional_Area_List))
    for i in range(int(len(Today_Coordinates_List))):
        [num, Area]=Conventional_Area_List[i]
        Today_Record_List_Test.append(Area)
        Today_Dict["%s" % Today_Coordinates_List[i]]=Area
        if re.search("-", Today_Coordinates_List[i]):
            continue
        Today_Record_List_Test.append(Today_Coordinates_List[i])
    #print("前日と比較前：", Today_Dict)
    #Today_Record_List_Test.insert(0,str(Date)) #一番最初に日付を挿入。

    print(Today_Record_List_Test)
    Checked_Today_Record_List=[]
    Checked_Today_Area_List=[]
    Checked_Today_Record_List.insert(0,str(Date))
    Checked_Today_Area_List.insert(0,str(Date))

    Checked_Today_Coordinates_List=Compare_these_Coordinates(Today_Coordinates_List)
    if Checked_Today_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        Checked_Today_Coordinates_List=[]
        with open('Assets/Assets_Output/Area_Record_Test_on_Mac.csv', 'a') as f: #Mac
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerow(Today_Record_List_Test)
        for element in Today_Record_List_Test:
            searching_date=re.search("-", str(element))
            searching_Coordinates=re.search(",", str(element))
            if searching_date:
                continue
            elif searching_Coordinates:
                Checked_Today_Record_List.append(element)
                Checked_Today_Coordinates_List.append(element)
            else:
                Checked_Today_Record_List.append(element)
                Checked_Today_Area_List.append(element)
        Checked_Today_Coordinates_List.insert(0,str(Date))

    else:
        #print(Checked_Today_Coordinates_List)
        for element in Checked_Today_Coordinates_List:
            searching_date=re.search("-", element)
            if searching_date:
                continue
            #print("Checked Coordinates：",element)
            #print("Dict", Today_Dict["%s" % element])
            Checked_Today_Record_List.append(Today_Dict["%s" % element])
            Checked_Today_Record_List.append(element)
            Checked_Today_Area_List.append(Today_Dict["%s" % element])

        with open('Assets/Assets_Output/Area_Record_Test_on_Mac.csv', 'a') as f: #Mac
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerow(Checked_Today_Record_List)
            #print("Today : ", Today_Coordinates_List)

    print("Checked_Today_Record_List : ", Checked_Today_Record_List)
    print("Checked_Today_Area_List : ", Checked_Today_Area_List)
    print("Checked_Today_Coordinates_List : ", Checked_Today_Coordinates_List)

    print("------------------------------")
    print("結果")
    print(Checked_Today_Area_List)
    for i in range(int(len(Checked_Today_Area_List))):
        #print(Checked_Today_Area_List)
        if re.search("-", str(Checked_Today_Area_List[i])):
            continue
        Area=Checked_Today_Area_List[i] #従来の面積測定方法を今回の面積に代入する(今回の面積測定方法は外接四角形の面積を測っているだけだから。)
        print("Checked_Today_Coordinates_List[i] : ",Checked_Today_Coordinates_List[i])
        [x,y]=str(Checked_Today_Coordinates_List[i]).split(",")
        print("(",x,",",y,")"," : ", Area)
        #画像にデータを貼り付ける。
        #cv2.putText(frame_with_contours, "(0,0)", (11,23), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255)) #各オブジェクトのラベル番号と面積に黄文字で表示
        cv2.putText(frame_with_contours, "ID:" +str(i), (int(x), int(y)+10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255)) #各オブジェクトのラベル番号と面積に黄文字で表示
        cv2.putText(frame_with_contours, "S:" +str(Area), (int(x), int(y)+25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(frame_with_contours, "C:(" + str(Checked_Today_Coordinates_List[i]) + ")", (int(x), int(y)+40), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 255)) # 各オブジェクトの重心座標をに黄文字で表示

    # 画像の保存
    cv2.imwrite('../../pre_Area_%s' % fname, frame_with_contours) #デスクトップ
    subprocess.getoutput('convert -trim ../../pre_Area_%s Assets/Assets_Output/Area_%s' % (fname, fname)) #デスクトップ
    os.remove('../../pre_Area_%s' % fname) #デスクトップ

    return Checked_Today_Area_List

def Get_Serial(): #ラズパイのCPU晩報を取得する(各ラズパイを識別するため)
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

def Upload_on_Dropbox(API, Picname, RasPi_SerialNum): #DropboxのAPIを利用するためのテンプレ
    dbx = dropbox.Dropbox(API)
    dbx.users_get_current_account()
    print(Picname)
    Desktop_Picname=Picname
    Picname=Picname.split('.')
    Picname=str(Picname[0])+'_'+RasPi_SerialNum+'.png'
    f = open('Assets/Assets_Output/%s' % Desktop_Picname, 'rb')
    Area_or_not=Desktop_Picname.split('_')
    if Area_or_not[0]=='Area':
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_Filter_%s/%s' % (RasPi_SerialNum,Desktop_Picname)) #dropbox内のディレクトリを書く
    else:
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_unFilter_%s/%s' % (RasPi_SerialNum,Desktop_Picname)) #dropbox内のディレクトリを書く
    f.close()

def save_the_picture(): #画像をクラウド(Dropbox)に保存する
    global fname
    try:
        RasPi_SerialNum=Get_Serial() #本番 #RaspberryPi
    except:
        RasPi_SerialNum='5ae9b47f' #テスト Mac
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

def send_message(Picname_LINE, Checked_Today_Area_List): #LINEのAPIを利用するためのテンプレ(面積と画像を送信する)
    url = "https://notify-api.line.me/api/notify"   #line notifyでラズパイからlineに画像を送信
    token = '2Rm15NEZNBO8A8kLZHAmKXBAk4fnwOnxQMJCknwdw4p'   #lineのtoken
    headers = {"Authorization" : "Bearer "+ token}
    try:
        RasPi_SerialNumber=Get_Serial() #RaspberryPi
    except:
        RasPi_SerialNumber='from_Mac' #Mac
    RasPi_Number='[picamera_%s]' % RasPi_SerialNumber
    Area_7=''
    j=0
    for i in Checked_Today_Area_List:
        Area_7=Area_7+str(j)+'_'+str(i)+'\n'
        j+=1
    message =  RasPi_Number+ Picname_LINE + '\n' + '面積の記録成功です。\n'+Area_7
    payload = {"message" :  message}
    files = {"imageFile": open("Assets/Assets_Output/%s" % Picname_LINE, "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。
    r = requests.post(url ,headers = headers ,params=payload, files=files)
    #os.remove("/home/pi/Desktop/%s" % fname)

def organize():
    os.remove('../../Contours_on_%s' % fname) #デスクトップ

def main():
    global fname
    check_the_date()
    take_the_picture()

    change_the_color()
    [Conventional_Area_List, contours]=draw_the_contours()
    Checked_Today_Area_List=Labeling(Conventional_Area_List, contours)

    Area_Fname='Area_'+fname
    #send_message(Area_Fname, Checked_Today_Area_List) #本番

    #save_the_picture() #本番

    organize()

if __name__ == '__main__':

    main()
