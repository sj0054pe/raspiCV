import cv2
from datetime import datetime, date, timedelta
import math
import re
import csv
import os
import subprocess
import pandas as pd
import math

import def_Identifying_RasPi

def Compare_these_Coordinates(Today_Coordinates_List, Yesterday_Coordinates_List, theDate):
    if Yesterday_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        return "No_Data"
    else:
        print("昨日の座標 　　　 : ", Yesterday_Coordinates_List)
        print("今日の座標(変更前): ", Today_Coordinates_List)
        Checked_Today_Coordinates_List=[]
        right_num_list=[]
        #print(len(Today_Coordinates_List)-1)

        for i in range(1,int(len(Today_Coordinates_List)-1)):
            exec("List_ToCoordinates_YeCoordinates_r_num_%s=[]" % str(i))
            exec("List_ToCoordinates_YeCoordinates_r_num_%s.clear()" % str(i))

        #print(int(len(Today_Coordinates_List)))
        for i in range(1,int(len(Today_Coordinates_List))): #日付もリストに含まれてるから-1する
            print(i)
            #print(Today_Coordinates_List[i])
            [Today_X,Today_Y]=Today_Coordinates_List[i].split(",")
            right_num, nearest_r=1000, 1000 #初期値なのであり得ない数字を入れておく
            #dict_iのiはToday_Coordinates_List[i]のi。
            exec("List_ToCoordinates_YeCoordinates_r_num_%s=[]" % str(i))
            exec("List_ToCoordinates_YeCoordinates_r_num_%s.append(Today_Coordinates_List[%s])" % (str(i),i))
            for j in range(int(len(Today_Coordinates_List)-1)): #日付もリストに含まれてるから-1する
                if re.search("-",Yesterday_Coordinates_List[j]):
                    continue
                [Yesterday_X,Yesterday_Y]=str(Yesterday_Coordinates_List[j]).split(",")
                print("(",Today_X,",",Today_Y,") / (",Yesterday_X,",",Yesterday_Y,")")
                try:
                    int(Yesterday_X)
                    a=int(Today_X)-int(Yesterday_X)
                    b=int(Today_Y)-int(Yesterday_Y)
                    r=math.sqrt(a*a+b*b) #距離=√(a^2+b^2)より、最短距離の個体を見つける。
                    print("距離:", int(r))
                    if 0< int(r) and int(r) < int(nearest_r):
                        right_num, nearest_r=j, r
                        nearest_Yesterday_Coordinates=Yesterday_Coordinates_List[j]
                        print("変更：",right_num)
                    elif r==0:
                        right_num, nearest_r=j, r
                        nearest_Yesterday_Coordinates=Yesterday_Coordinates_List[j]
                        print("変更：",right_num)
                        break
                    else:
                        continue
                except:
                    continue
            #print(nearest_Yesterday_Coordinates)
            exec("List_ToCoordinates_YeCoordinates_r_num_%s.append(nearest_Yesterday_Coordinates)" % (str(i)))
            exec("List_ToCoordinates_YeCoordinates_r_num_%s.append(nearest_r)" % str(i))
            exec("List_ToCoordinates_YeCoordinates_r_num_%s.append(right_num)" % str(i))
            exec("print(List_ToCoordinates_YeCoordinates_r_num_%s)" % str(i))
            right_num_list.append(right_num)
            print("最終：",right_num)
            print()
        print("昨日の何番になるかのリスト：",right_num_list)

        position_List=[]
        print("ToCoordinates_YeCoordinates_r_num")
        for k in range(1,int(len(Today_Coordinates_List))):
            exec("print(List_ToCoordinates_YeCoordinates_r_num_%s)" % str(k))
            position_List.append(k)

        for m in range(7):
            Checked_Today_Coordinates_List.append("NA")

        print('競合している場所の番号について距離の比較を開始します')
        Loser_ToCoordinates_List=[]
        count_remove=0
        for num in position_List:
            Shortest_r=1000
            print('- - - - - -')
            for l in range(1,int(len(Today_Coordinates_List))):
                if eval("List_ToCoordinates_YeCoordinates_r_num_%s[3] == num" % (l)):
                    exec('print(List_ToCoordinates_YeCoordinates_r_num_%s[3])' % (l))
                    exec("Loser_ToCoordinates_List.append(List_ToCoordinates_YeCoordinates_r_num_%s[0])" % (l))
                    print("List_ToCoordinates_YeCoordinates_r_num_%s[0]は昨日の%s番を指し示しています。"% (l,num))
                    print(Loser_ToCoordinates_List)
                    if eval("List_ToCoordinates_YeCoordinates_r_num_%s[2] < Shortest_r" % (l)):
                        #Loser_ToCoordinates_List.pop(-1)
                        print("現在のShortest_rは%sです。" % Shortest_r)
                        print("List_ToCoordinates_YeCoordinates_r_num_%s[0]は%sより短いです。" % (l,Shortest_r))
                        print("List_ToCoordinates_YeCoordinates_r_num_%s[0]が昨日の%s番の位置になりました。" % (l,num))
                        Shortest_r=eval("List_ToCoordinates_YeCoordinates_r_num_%s[2]" % (l))
                        suitable_num_in_Today=num
                        suitable_Coordinates=eval("List_ToCoordinates_YeCoordinates_r_num_%s[0]" % (l))
                        #print(suitable_num_in_Today)
                else:
                    continue
                Checked_Today_Coordinates_List[suitable_num_in_Today-1]=suitable_Coordinates
                print(Loser_ToCoordinates_List)
            for element in Loser_ToCoordinates_List:
                if element == suitable_Coordinates: #Loser_ToCoordinates_Listははじき出された座標のリスト。suitableな座標は削除して"NA,NAに置き換え。"
                    print("%sをLoser_ToCoordinates_Listから削除します" % element)
                    Loser_ToCoordinates_List.remove(element)
                    count_remove=count_remove+1

        print(count_remove)
        for i in range(1,count_remove):
            Loser_ToCoordinates_List.append("NA")

        print("Loser_ToCoordinates_List",Loser_ToCoordinates_List)
        print("Checked_Today_Coordinates_List",Checked_Today_Coordinates_List)
        print((len(Loser_ToCoordinates_List)-1))
        count_for_Checked=0
        count_for_Loser=0
        for element in Checked_Today_Coordinates_List:
            print('Coordinates : ', element)
            if element =="NA":
                print("NA発見")
                if (count_for_Checked) > (len(Loser_ToCoordinates_List)):
                    break
                Checked_Today_Coordinates_List[count_for_Checked]=Loser_ToCoordinates_List[count_for_Loser]
                count_for_Loser=count_for_Loser+1
            print(count_for_Checked)
            print(count_for_Loser)
            count_for_Checked=count_for_Checked+1

        Checked_Today_Coordinates_List.insert(0,Today_Coordinates_List[0])
        print('Checked_Today_Coordinates_List : ', Checked_Today_Coordinates_List)

        return Checked_Today_Coordinates_List


def make_Header(Season):
    Header=[]
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    for i in range(7+1):
        if i == 0:
            Header.append("Date")
        else:
            Header.extend(["Area_%s" % i,"Coordinates_%s" % i])
    print("Header", Header)
    with open('Assets/Assets_Output/Newest_Record_%s_on_%s.csv' % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Header)

#csvファイルに保存されている直近の日付のデータを取り出す。
def pull_the_latest_Coordinates(Today_Coordinates_List, theDate, Season):
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    try:
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/Newest_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), sep=",")
    except: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        make_Header(Season)
        return "No_Data"

    #print(list(csv_input["Date"])) #csvファイルに保存されている日付の一覧を表示
    Date_List=list(csv_input["Date"])
    print(csv_input)
    YESTERDAY=Date_List[0] #print("START_DAY：", YESTERDAY_DAY) #csvファイルにある当日から直近の日付を調べる。まずは一番早い日から。
    print('YESTERDAY : ', YESTERDAY)

    YESTERDAY=datetime.strptime(YESTERDAY, '%Y-%m-%d')
    theDate=datetime.strptime(theDate, '%Y-%m-%d')

    Difference=theDate-YESTERDAY
    Difference=abs(Difference.days)

    DataFrame_Column_num=1 #DataFrame_Column_num=直近の日付が何行目かを表示。#データフレームは、ヘッダーが行0番目だから、Date_List[0]に入る日付はデータフレームでいうと行1番目になる。リスト⇄データフレーム間の調整。
    for Date in Date_List:
        Date=datetime.strptime(Date, '%Y-%m-%d')
        new_Difference=theDate-Date
        new_Difference=abs(new_Difference.days)
        if (0 < int(new_Difference)) and (int(new_Difference) < int(Difference)):
            YESTERDAY=Date
            print("YESTERDAYは%sに変更になりました。", YESTERDAY)
            DataFrame_Column_num=DataFrame_Column_num+1
    Latest_Data_on_csv=csv_input.iloc[DataFrame_Column_num-1,]

    Latest_Coordinates_List=[]
    Latest_Coordinates_List.clear()
    Latest_Coordinates_List.insert(0,Latest_Data_on_csv["Date"])
    for i in range(int(len(csv_input.columns)/2)):
        i=i+1
        #print(Latest_Data_on_csv["Coordinates_%s" % i])
        Latest_Coordinates_List.append(Latest_Data_on_csv["Coordinates_%s" % i])
    #print("Yesterday : ", Latest_Coordinates_List)
    return Latest_Coordinates_List

def Record(Checked_Today_Record_List, Checked_Today_Area_List, Checked_Today_Coordinates_List,Season,fname):
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    try:
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/Newest_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), sep=",")
    except: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        make_Header(Season)

    with open("Assets/Assets_Output/Newest_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Checked_Today_Record_List)
        #print("Todayと : ", Today_Coordinates_List)

    print("Checked_Today_Record_List : ", Checked_Today_Record_List)
    print("Checked_Today_Area_List : ", Checked_Today_Area_List)
    print("Checked_Today_Coordinates_List : ", Checked_Today_Coordinates_List)

    print("-----結果------")
    print(range(int(len(Checked_Today_Area_List))))
    frame_with_contours=cv2.imread('../../Contours_on_%s' % fname) #デスクトップ
    for i in range(int(len(Checked_Today_Area_List))):
        print(i)
        if re.search("-", str(Checked_Today_Area_List[i])):
            print("日付を確認")
            continue
        elif re.search("NA", str(Checked_Today_Area_List[i])):
            print("NAを確認")
            continue
        print("Checked_Today_Coordinates_List[i] : ",Checked_Today_Coordinates_List[i])
        [x,y]=str(Checked_Today_Coordinates_List[i]).split(",")
        print("(",x,",",y,")"," : ", Checked_Today_Area_List[i])
        #画像にデータを貼り付ける。
        cv2.putText(frame_with_contours, "ID:" +str(i), (int(x), int(y)+10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255)) #各オブジェクトのラベル番号と面積に黄文字で表示
        cv2.putText(frame_with_contours, "S:" +str(Checked_Today_Area_List[i]), (int(x), int(y)+25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(frame_with_contours, "C:(" + str(Checked_Today_Coordinates_List[i]) + ")", (int(x), int(y)+40), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 255)) # 各オブジェクトの重心座標をに黄文字で表示

    # 画像の保存
    cv2.imwrite('../../pre_Area_%s' % fname, frame_with_contours) #デスクトップ
    subprocess.getoutput('convert -trim ../../pre_Area_%s ../../Area_%s' % (fname, fname)) #デスクトップ
    os.remove('../../pre_Area_%s' % fname) #デスクトップ

def Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None): #画像上にデータを付与する
    #Date=datetime.date.today()

    #比較するため今日の面積と中心座標をリストと辞書にする。
    Today_Dict={}
    #for i in range(int(len(Today_Coordinates_List))):
    for i in range(8):
        Area=Conventional_Area_List[i]
        if re.search("-", Today_Coordinates_List[i]):
            continue
        Today_Dict["%s" % Today_Coordinates_List[i]]=Area #面積と座標を結びつける

    '''
    #比較するため今日の面積と中心座標をリストと辞書にする。
    Today_Record_List_When_Latest_Data_is_None=[] #前日の比較する座標がなかった時にcsvファイルに保存する用
    Today_Dict={}
    #for i in range(int(len(Today_Coordinates_List))):
    for i in range(8):
        try:
            [num, Area]=Conventional_Area_List[i]
            Today_Record_List_When_Latest_Data_is_None.append(Area)
            Today_Dict["%s" % Today_Coordinates_List[i]]=Area #面積と座標を結びつける
            if re.search("-", Today_Coordinates_List[i]):
                continue
            Today_Record_List_When_Latest_Data_is_None.append(Today_Coordinates_List[i])
        except:
            Today_Record_List_When_Latest_Data_is_None.extend(["NA","NA"])
    #print("前日と比較前：", Today_Dict)
    print("Today_Record_List_When_Latest_Data_is_None", Today_Record_List_When_Latest_Data_is_None)
    #Today_Record_List_When_Latest_Data_is_None.insert(0,str(theDate)) #一番最初に日付を挿入。
    '''

    Checked_Today_Record_List=[]
    Checked_Today_Area_List=[]
    Checked_Today_Record_List.insert(0,str(theDate))
    Checked_Today_Area_List.insert(0,str(theDate))

    Yesterday_Coordinates_List=pull_the_latest_Coordinates(Today_Coordinates_List, theDate, Season)
    Checked_Today_Coordinates_List=Compare_these_Coordinates(Today_Coordinates_List, Yesterday_Coordinates_List, theDate)
    if Checked_Today_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        Checked_Today_Coordinates_List=[]
        Checked_Today_Coordinates_List.clear()
        Checked_Today_Record_List=Today_Record_List_When_Latest_Data_is_None
        for element in Checked_Today_Record_List:
            if re.search("-", str(element)):
                continue
            elif re.search(",", str(element)):
                Checked_Today_Coordinates_List.append(element)
            else:
                Checked_Today_Area_List.append(element)
                print(Checked_Today_Area_List)
        Checked_Today_Coordinates_List.insert(0,str(theDate))

    else: #前日の座標があった場合
        print("Checked_Today_Area_Listの作成開始")
        for element in Checked_Today_Coordinates_List: #element=座標
            if re.search("-", element):
                continue
            elif re.match("NA", str(element)): #不要の可能性あり
                Checked_Today_Record_List.extend(["NA", "NA"])
                Checked_Today_Area_List.append("NA")
                continue
            Checked_Today_Record_List.extend([Today_Dict["%s" % element], element])
            Checked_Today_Area_List.append(Today_Dict["%s" % element])

    Record(Checked_Today_Record_List, Checked_Today_Area_List, Checked_Today_Coordinates_List)
    return Checked_Today_Area_List
