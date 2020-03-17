import csv
import pandas as pd
from datetime import datetime, date, timedelta
import math
import re
import os

import def_Identifying_RasPi

'''
def make_Header(role,Season, num_of_object,RasPi_SerialNum):
    Header=[]
    #RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    for i in range(num_of_object+1):
        if i == 0:
            Header.append("Date")
        else:
            Header.extend(["Area_%s" % i,"Coordinates_%s" % i])
    print("Header", Header)
    with open('Assets/Assets_Output/%s_Record_%s_on_%s.csv' % (role,Season,RasPi_SerialNum), 'a') as f: #Mac
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(Header)
'''

#csvファイルに保存されている直近の日付のデータを取り出す。
def pull_the_latest_Coordinates(theDate, Season, role,RasPi_SerialNum, num_of_object):
    #RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    try:
        #print("Assets/Assets_Output/%s_Record_%s_on_%s.csv" % (role,Season,RasPi_SerialNum))
        csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Output/%s_Record_%s_on_%s.csv" % (role,Season,RasPi_SerialNum), sep=",", engine="python")
        print("%s_Record_%s_on_%s.csvを発見" % (role,Season,RasPi_SerialNum))
    except: #観察初日は参照する前日のデータがないので、csvファイルのヘッダーを作るところから始める。
        #make_Header(role,Season, num_of_object,RasPi_SerialNum)
        print("記録用csvファイル(%s_Record_%s_on_%s.csv)がありませんでした。" % (role,Season,RasPi_SerialNum))
        return "No_Data"
    #print(list(csv_input["Date"])) #csvファイルに保存されている日付の一覧を表示
    Date_List=list(csv_input["Date"])
    #print(csv_input)
    YESTERDAY=Date_List[0] #print("START_DAY：", YESTERDAY_DAY) #csvファイルにある当日から直近の日付を調べる。まずは一番早い日から。
    #print('YESTERDAY : ', YESTERDAY)

    YESTERDAY=datetime.strptime(YESTERDAY, '%Y-%m-%d')
    theDate=datetime.strptime(theDate, '%Y-%m-%d')
    #print(YESTERDAY)

    Difference=theDate-YESTERDAY
    Difference=abs(Difference.days)
    #print(Difference)

    DataFrame_Column_num=1 #DataFrame_Column_num=直近の日付が何行目かを表示。#データフレームは、ヘッダーが行0番目だから、Date_List[0]に入る日付はデータフレームでいうと行1番目になる。リスト⇄データフレーム間の調整。
    for Date in Date_List:
        if re.match("Date", Date):
            continue
        Date=datetime.strptime(Date, '%Y-%m-%d')
        new_Difference=theDate-Date
        new_Difference=abs(new_Difference.days)
        print(new_Difference)
        if (0 < int(new_Difference)) and (int(new_Difference) < int(Difference)):
            YESTERDAY=Date
            print("YESTERDAYは%sに変更になりました。" % YESTERDAY)
            DataFrame_Column_num=DataFrame_Column_num+1
    Latest_Data_on_csv=csv_input.iloc[DataFrame_Column_num-1,]

    Latest_Coordinates_List=[]
    Latest_Coordinates_List.clear()
    Latest_Coordinates_List.insert(0,Latest_Data_on_csv["Date"])
    for i in range(int(len(csv_input.columns)/2)):
        i=i+1
        print(Latest_Data_on_csv["Coordinates_%s" % i])
        Latest_Coordinates_List.append(Latest_Data_on_csv["Coordinates_%s" % i])
    #print("Yesterday : ", Latest_Coordinates_List)
    return Latest_Coordinates_List

def main(): #不完全
    pull_the_latest_Coordinates(theDate, Season, role,RasPi_SerialNum)

    return 0

if __name__ == '__main__':

    main()
