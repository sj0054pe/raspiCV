import cv2
import csv
import subprocess
import pandas as pd
import re

import def_Browse_data_on_CSV
import def_Compare_these_Coordinates
import def_Identifying_RasPi
import def_Finding_Square

def make_Header(Season):
    Header=[]
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    for i in range(120+1):
        if i == 0:
            Header.append("Date")
        else:
            Header.extend(["Area_%s" % i,"Coordinates_%s" % i])
    print("Header", Header)
    with open('Assets/Assets_Output/Newest_Record_%s_on_%s.csv' % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Header)

def Record(Checked_Today_Record_List, Checked_Today_Area_List, Checked_Today_Coordinates_List,Season,fname):
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    try:
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/Newest_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), sep=",")
    except: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        make_Header(Season)

    with open("Assets/Assets_Output/Newest_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Checked_Today_Record_List)

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

def Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None): #画像上にデータを付与する

    print('比較するため今日の面積と中心座標を辞書にする。')
    Today_Dict={}
    print(Conventional_Area_List)
    print(Today_Coordinates_List)
    for i in range(0,int(len(Today_Coordinates_List))):
        if re.search("-", Today_Coordinates_List[i]):
            continue
        else:
            Area=Conventional_Area_List[i]
            Today_Dict["%s" % Today_Coordinates_List[i]]=Area #面積と座標を結びつける

    Checked_Today_Record_List=[]
    Checked_Today_Area_List=[]
    Checked_Today_Record_List.insert(0,str(theDate))
    Checked_Today_Area_List.insert(0,str(theDate))

    print('直近の座標を取得します。')
    Yesterday_Coordinates_List=def_Browse_data_on_CSV.pull_the_latest_Coordinates(Today_Coordinates_List, theDate, Season)
    Checked_Today_Coordinates_List=def_Compare_these_Coordinates.Compare_these_Coordinates(Today_Coordinates_List, Yesterday_Coordinates_List, theDate)

    if Checked_Today_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        Largest_object=def_Finding_Square.finding_largest_object(Conventional_Area_List)
        def_Finding_Square.Record_the_base_object(Largest_object,Today_Dict,Season,theDate)
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
        for element in Checked_Today_Coordinates_List: #element=座標
            print(element)
            if re.search("-", element):
                continue
            elif re.match("NA", str(element)): #不要の可能性あり
                Checked_Today_Record_List.extend(["NA", "NA"])
                Checked_Today_Area_List.append("NA")
                continue
            Checked_Today_Record_List.extend([Today_Dict["%s" % element], element])
            Checked_Today_Area_List.append(Today_Dict["%s" % element])

    Record(Checked_Today_Record_List, Checked_Today_Area_List, Checked_Today_Coordinates_List, Season, fname)
    return Checked_Today_Area_List

def main(): #不完全
    Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None)

    return 0

if __name__ == '__main__':

    main()
