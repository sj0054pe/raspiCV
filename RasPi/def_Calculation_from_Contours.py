import datetime
import matplotlib.pyplot as plt
import numpy as np
import csv
import cv2
import os
from matplotlib.patches import Circle, Polygon, Rectangle
from scipy import ndimage
import subprocess

import def_Identifying_RasPi

def Record_Area(Area_List, Season): #とりあえず従来の方法で面積データを保存する
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    csv_List=[]
    for Elements in Area_List:
        [Contours_num, Contours_Area]=Elements
        csv_List.append(Contours_Area)
    with open('Assets/Assets_Output/Conventional_Record_%s_on_%s.csv' % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(csv_List)

def Calculate_the_Area(contours,theDate, Season): #輪郭(cnt)から面積を導出する
    #Date=datetime.date.today()
    Area_List = []
    #面積を求める
    for i, cnt in enumerate(contours):
        # 輪郭の面積を計算する。
        area = cv2.contourArea(cnt)
        #file.write('contour: {}, area: {}'.format(i, area))
        sub_Area_List=[]
        num=(len(contours)-1)-i #新しいラベリング処理方法に合わせてサンプルの上から番号を添付するように変更。
        #print(num)
        sub_Area_List.append(num)
        sub_Area_List.append(area)
        #print(sub_Area_List)
        Area_List.append(sub_Area_List)
        #print('contour: {}, area: {}'.format(i, area))
    #Area_List_reversed=Area_List[::-1]
    print("日付：", theDate)
    Area_List.insert(0,[str(theDate),str(theDate)]) #一番最初に日付を挿入。
    print("-",len(contours), "個検出しました。-")
    #print("面積(輪郭)：", Conventional_Area_List)
    Record_Area(Area_List, Season)

    return Area_List

def draw_the_contours(fname, theDate, Season): #輪郭を描写する
    #↓画像を読み込む。
    img = cv2.imread('../../Green.png') #デスクトップ
    #↓面積導出関数へ渡す。
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #緑色を白、背景を黒にした二値化をする。(そうしないと輪郭抽出や他のOpenCVの関数で扱いずらい。)
    contours,hierarchy=cv2.findContours(gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    Conventional_Area_List = []
    Conventional_Area_List=Calculate_the_Area(contours, theDate, Season) #def

    Today_Coordinates_List=[]  #昨日と今日の中心座標を比較する用
    for Elements in contours:
        mu = cv2.moments(Elements)
        x,y= int(mu["m10"]/mu["m00"]) , int(mu["m01"]/mu["m00"])
        Coordinates=str(x)+","+str(y)
        Today_Coordinates_List.append(Coordinates)
    #Today_Coordinates_List=Today_Coordinates_List[::-1]
    Today_Coordinates_List.insert(0,str(theDate))

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
        #ax.text(cnt[0][0], cnt[0][1], j, color='orange', size='20')
    #plt.savefig('../../pre_Contours_on_%s' % fname, bbox_inches='tight') #デスクトップ
    plt.savefig('../../Contours_on_%s' % fname, bbox_inches='tight') #デスクトップ
    #subprocess.getoutput('convert -trim ../../pre_Contours_on_%s ../../Contours_on_%s' % (fname, fname)) #デスクトップ
    #os.remove('../../pre_Contours_on_%s' % fname) #デスクトップ

    return Conventional_Area_List, Today_Coordinates_List
