import datetime
import matplotlib.pyplot as plt
import numpy as np
import csv
import cv2
import os
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy import ndimage
import subprocess

#import def_Identifying_RasPi

#開発初期の保存方法も念のため採用している。#個体番号を並べ替えず、かつ面積だけを保存する
def Record_Area(Area_List, Season,RasPi_SerialNum): #とりあえず従来の方法で面積データを保存する
    csv_List=[]
    for Elements in Area_List:
        Contours_Area=Elements
        csv_List.append(Contours_Area)
    with open('Assets/Assets_Output/Conventional_Record_%s_on_%s.csv' % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(csv_List)

def Calculate_the_Area(contours,theDate, Season,RasPi_SerialNum): #輪郭(cnt)から面積を導出する
    #Date=datetime.date.today()
    Area_List = []
    #面積を求める
    for i, cnt in enumerate(contours):
        # 輪郭の面積を計算する。
        area = cv2.contourArea(cnt)
        Area_List.append(area)
        #print("日付：", theDate)
    Area_List.insert(0,str(theDate)) #一番最初に日付を挿入。
    print("-",len(contours), "個検出しました。-")
    #print("面積(輪郭)：", Conventional_Area_List)
    Record_Area(Area_List, Season, RasPi_SerialNum)

    return Area_List

def Coordinates(contours, theDate, Season,RasPi_SerialNum, Conventional_Area_List, Today_Coordinates_List):
    i=0
    Error_Coordinates_List=[]
    Error_Coordinates_List.clear()
    for Elements in contours:
        try:
            mu = cv2.moments(Elements)
            x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
            Coordinates=str(x)+","+str(y)
            #print("try", Coordinates)
            Today_Coordinates_List.append(Coordinates)
            i+=1
            #print(i)
        except:
            i+=1
            Error_Coordinates_List.append(int(i))
            #print("Error", int(i))
            continue

    dellist = lambda items, indexes: [item for index, item in enumerate(items) if index not in indexes] #https://qiita.com/nagataaaas/items/531b1fc5ce42a791c7df
    Conventional_Area_List=dellist(Conventional_Area_List, Error_Coordinates_List)
    #print("Conventional_Area_List",Conventional_Area_List)
    Today_Coordinates_List.insert(0,str(theDate))

    return Today_Coordinates_List, Conventional_Area_List

def draw_the_contours(fname, theDate, Season, RasPi_SerialNum): #輪郭を描写する
    #↓画像を読み込む。
    img = cv2.imread('../../Green.png') #デスクトップ
    #↓面積導出関数へ渡す。
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #緑色を白、背景を黒にした二値化をする。(そうしないと輪郭抽出や他のOpenCVの関数で扱いずらい。)

    #OpenCV3.0と4.0で使用が違うにで場合分け
    try:
        contours,hierarchy=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    except:
        _,contours,hierarchy=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    Conventional_Area_List = []
    Conventional_Area_List=Calculate_the_Area(contours, theDate, Season,RasPi_SerialNum) #def

    Today_Coordinates_List=[]  #昨日と今日の中心座標を比較する用
    Today_Coordinates_List, Conventional_Area_List=Coordinates(contours, theDate, Season,RasPi_SerialNum, Conventional_Area_List, Today_Coordinates_List)

    print("Conventional_Area_List : ", Conventional_Area_List)
    print("Today_Coordinates_List : ", Today_Coordinates_List)

    #比較するため今日の面積と中心座標をリストと辞書にする。
    Today_Record_List_When_Latest_Data_is_None=[] #前日の比較する座標がなかった時にcsvファイルに保存する用
    for i in range(1,int(len(Today_Coordinates_List))):
        print(Today_Coordinates_List[i])
        print(Conventional_Area_List[i])
        try:
            Area=Conventional_Area_List[i]
            Today_Record_List_When_Latest_Data_is_None.append(Area)
            Today_Record_List_When_Latest_Data_is_None.append(Today_Coordinates_List[i])
        except:
            Today_Record_List_When_Latest_Data_is_None.extend(["NA","NA"])

    Today_Record_List_When_Latest_Data_is_None.insert(0,str(theDate)) #一番最初に日付を挿入。
    print("Today_Record_List_When_Latest_Data_is_None : ", Today_Record_List_When_Latest_Data_is_None)

    #輪郭をプロットする部分。
    frame=cv2.imread('../../%s' % fname) #生画像 #ディレクトリはデスクトップ
    #frame=img #for Presentation
    modified_imgforshow=ndimage.median_filter(frame, 1)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(modified_imgforshow)
    ax.axis('off')
    for j, cnt in enumerate(contours):
        cnt = np.squeeze(cnt, axis=1)
        ax.add_patch(Polygon(cnt, color='r', fill=None, lw=0.5))
    plt.savefig('../../Contours_on_%s' % fname, bbox_inches='tight') #デスクトップ

    return Conventional_Area_List, Today_Coordinates_List, Today_Record_List_When_Latest_Data_is_None

def main(): #不完全
    def_Change_the_color.change_the_color(fname)
    Calculate_the_Area(contours,theDate, Season)

    return 0

if __name__ == '__main__':

    main()
