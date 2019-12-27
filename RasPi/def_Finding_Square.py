import re
import csv

import def_Identifying_RasPi
import def_Browse_data_on_CSV

def pull_the_base_Coordinates(theDate, Season,RasPi_SerialNum):
    role="Base"
    Latest_Coordinates_List=def_Browse_data_on_CSV.pull_the_latest_Coordinates(theDate, Season, role,RasPi_SerialNum)

    return Latest_Coordinates_List

def make_Header(Season,RasPi_SerialNum):
    Header=[]
    #RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    Header=["Date","Area_1","Coordinates_1"]
    with open('Assets/Assets_Output/Base_Record_%s_on_%s.csv' % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Header)

def Record_the_base_object(Largest_object,Today_Dict,Season, theDate,RasPi_SerialNum):
    #RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()

    try:
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/Base_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), sep=",", engine="python")
    except: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        print("Base_Record_%s_on_%s.csvが存在しません。" % (Season,RasPi_SerialNum), sep=",")
        make_Header(Season,RasPi_SerialNum)

    print('これからBaseを保存します。')
    Today_Dict_reverse = {v: k for k, v in Today_Dict.items()} #辞書のkey=座標,value=面積を逆にする。

    with open("Assets/Assets_Output/Base_Record_%s_on_%s.csv" % (Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        Base_List=[]
        Base_List.clear()
        Base_List.append(theDate)
        print('s')
        Base_List.append(Largest_object)
        print('ss')
        Base_List.append(Today_Dict_reverse[Largest_object])
        print('sss')
        writer.writerow(Base_List)
        print('SSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        #print("Todayと : ", Today_Coordinates_List)

def finding_largest_object(Conventional_Area_List,RasPi_SerialNum):
    Largest_object=0
    for Area in Conventional_Area_List:
        if re.search("-", str(Area)):
            continue
        elif (float(Area) > float(Largest_object)) and (float(Area) < 600):
            Largest_object = Area
    print("一番大きい値は",str(Largest_object),"です。")

    return Largest_object
