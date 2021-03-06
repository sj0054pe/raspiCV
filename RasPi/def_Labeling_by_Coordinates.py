import cv2
import csv
import subprocess
import pandas as pd
import re

import def_Browse_data_on_CSV
import def_Compare_these_Coordinates
import def_Identifying_RasPi
import def_Finding_Square

def make_Header(Season, num_of_object,RasPi_SerialNum):
    Header=[]
    #RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    for i in range(num_of_object+1):
        if i == 0:
            Header.append("Date")
        else:
            Header.extend(["Area_%s" % i,"Coordinates_%s" % i])
    print("Header", Header)
    with open('Assets/Assets_Output/Arranged_%s_on_%s.csv' % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Header)

def Record(Checked_Today_Record_List, Checked_Today_Area_List, Checked_Today_Coordinates_List,Season,fname,num_of_object,RasPi_SerialNum):
    #RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    try:
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/Arranged_%s_on_%s.csv" % (Season,RasPi_SerialNum), sep=",", engine="python")
    except: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        make_Header(Season, num_of_object,RasPi_SerialNum)

    with open("Assets/Assets_Output/%s_on_%s.csv" % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Checked_Today_Record_List)

    print("-----結果------")
    print("Checked_Today_Record_List : ", Checked_Today_Record_List)
    print("Checked_Today_Area_List : ", Checked_Today_Area_List)
    print("Checked_Today_Coordinates_List : ", Checked_Today_Coordinates_List)

    print("")
    #print(range(int(len(Checked_Today_Area_List))))
    frame_with_contours=cv2.imread('../../Contours_on_%s' % fname) #デスクトップ
    for i in range(int(len(Checked_Today_Area_List))):
        #print(i)
        if re.search("-", str(Checked_Today_Area_List[i])):
            print("日付を確認。スキップします。")
            continue
        elif re.search("NA", str(Checked_Today_Area_List[i])):
            print("NAを確認。スキップします。")
            continue
        #print("Checked_Today_Coordinates_List[i] : ",Checked_Today_Coordinates_List[i])
        [x,y]=str(Checked_Today_Coordinates_List[i]).split(",")
        print("(",x,",",y,")"," : ", Checked_Today_Area_List[i])
        #画像にデータを貼り付ける。
        cv2.putText(frame_with_contours, "ID:" +str(i), (int(x), int(y)+10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255)) #各オブジェクトのラベル番号と面積に黄文字で表示
        cv2.putText(frame_with_contours, "S:" +str(Checked_Today_Area_List[i]), (int(x), int(y)+25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(frame_with_contours, "C:(" + str(Checked_Today_Coordinates_List[i]) + ")", (int(x), int(y)+40), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 255)) # 各オブジェクトの重心座標をに黄文字で表示

    # 画像の保存
    #cv2.imwrite('../../pre_Area_%s' % fname, frame_with_contours) #デスクトップにある
    cv2.imwrite('../../Area_%s' % fname, frame_with_contours) #デスクトップにある
    #subprocess.run('convert -trim ../../pre_Area_%s ../../Area_%s' % (fname, fname)) #デスクトップにある

def Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None, num_of_object,RasPi_SerialNum): #画像上にデータを付与する

    print('はじめに面積と中心座標を辞書にする。')
    Today_Dict={}
    print("今日の面積", Conventional_Area_List)
    print("今日の座標", Today_Coordinates_List)
    for i in range(0,int(len(Today_Coordinates_List))):
        if re.search("-", Today_Coordinates_List[i]):
            continue
        else:
            Area=Conventional_Area_List[i]
            Today_Dict["%s" % Today_Coordinates_List[i]]=Area #面積と座標を結びつける
    print('Today_Dict(完成した辞書) : ', Today_Dict)

    print("以下のリストを宣言します。")
    print(' ・Checked_Today_Record_List :最終的な保存リスト')
    print(' ・Checked_Today_Area_List   :最終的な面積のリスト')
    print(' ・Checked_Today_Coordinates :最終的な座標のリスト')
    print('')
    Checked_Today_Record_List=[]
    Checked_Today_Area_List=[]
    Checked_Today_Record_List.insert(0,str(theDate))
    Checked_Today_Area_List.insert(0,str(theDate))
    Checked_Today_Coordinates_List=[]

    print('Browsing...')
    print('これから直近の座標(Yesterday_Coordinates_List)と比較します。')
    role="Arranged"
    Yesterday_Coordinates_List=def_Browse_data_on_CSV.pull_the_latest_Coordinates(theDate, Season, role, RasPi_SerialNum, num_of_object)
    print('Browsing Done!\n')
    print('Compareing Todays Coordinates to Yesterdays one...')
    Checked_Today_Coordinates_List=def_Compare_these_Coordinates.Compare_these_Coordinates(Today_Coordinates_List, Yesterday_Coordinates_List, theDate,RasPi_SerialNum)
    print('Compareing Done!\n')
    if Checked_Today_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        Largest_object=def_Finding_Square.finding_largest_object(Conventional_Area_List,RasPi_SerialNum)
        def_Finding_Square.Record_the_base_object(Largest_object,Today_Dict,Season,theDate,RasPi_SerialNum)
        Base_Coordinates_List=def_Finding_Square.pull_the_base_Coordinates(theDate, Season,RasPi_SerialNum, num_of_object)
        Base_Coordinates=Base_Coordinates_List[1]
        Base_Area=Today_Dict[Base_Coordinates]

        Checked_Today_Coordinates_List=[]
        Checked_Today_Coordinates_List.clear()
        Checked_Today_Record_List=Today_Record_List_When_Latest_Data_is_None
        num=0
        for element in Checked_Today_Record_List:
            if re.search("-", str(element)):
                num+=1
                continue
            elif re.search(",", str(element)):
                Checked_Today_Coordinates_List.append(element)
            else:
                Area_cm2=element/Base_Area
                Area_cm2=round(Area_cm2, 5)
                Checked_Today_Area_List.append(Area_cm2)
                Checked_Today_Record_List[num]=Area_cm2
                #print(Checked_Today_Area_List)
            num+=1
        Checked_Today_Coordinates_List.insert(0,str(theDate))
        print('')

    else: #前日の座標があった場合
        print("これからスケールを判別します。")
        Base_Coordinates_List=def_Finding_Square.pull_the_base_Coordinates(theDate, Season, RasPi_SerialNum)
        Checked_Base_Coordinates_List=def_Compare_these_Coordinates.Compare_these_Coordinates(Today_Coordinates_List, Base_Coordinates_List, theDate,RasPi_SerialNum)
        Checked_Base_Coordinates=Checked_Base_Coordinates_List[1]
        Base_Area=Today_Dict[Checked_Base_Coordinates]
        for element in Checked_Today_Coordinates_List: #element=座標
            if re.search("-", element):
                continue
            elif re.match("NA", str(element)): #不要の可能性あり
                Checked_Today_Record_List.extend(["NA", "NA"])
                Checked_Today_Area_List.append("NA")
                continue
            Area=Today_Dict[element]
            Area_cm2=Area/Base_Area
            Area_cm2=round(Area_cm2, 5)
            Checked_Today_Record_List.extend([Area_cm2, element])
            Checked_Today_Area_List.append(Area_cm2)

    Record(Checked_Today_Record_List, Checked_Today_Area_List, Checked_Today_Coordinates_List, Season, fname, num_of_object,RasPi_SerialNum)
    return Checked_Today_Area_List

def main(): #不完全
    Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None,RasPi_SerialNum)

    return 0

if __name__ == '__main__':

    main()
