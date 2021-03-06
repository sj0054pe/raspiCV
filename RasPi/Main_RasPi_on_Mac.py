import def_datetime
import def_Take_a_file
import def_Change_the_color
import def_Calculation_from_Contours
import def_Labeling_by_Coordinates
import def_Identifying_RasPi
import def_Send_the_message
import def_Save_the_picture
import def_finish
import def_PhotoLINE

import csv
import pandas as pd

from datetime import datetime, date, timedelta
import time
TimeMeasurement = time.time()

def Setting():
    #初期設定--------------------------------------------------------------------
    Season="MAYO" #シーズンごとに変更する。(いろんなモジュールに存在するSeasonはここから派生しているのでこの部分の変更をするだけでいい。)
    num_of_object=12+1 #1つのカメラで撮影する個体数。 12はゼニゴケの数、1はスケール
    #---------------------------------------------------------------------------
    return Season, num_of_object

def main(theDate, RasPi_SerialNum):
    try:
        progress_num=0
        '''
        print("Check date...")
        fname, theDate = def_datetime.check_the_date(Season, RasPi_SerialNum)
        print("Check date Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()
        '''

        print("Taking Picture... ")
        fname = def_Take_a_file.make_the_filename(theDate, Season, RasPi_SerialNum)
        print("Take Picture Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()

        print("Finding Green...")
        def_Change_the_color.change_the_color(fname)
        print("Found Leaves!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()

        print("Calculating the Area...")
        [Conventional_Area_List, Today_Coordinates_List, Today_Record_List_When_Latest_Data_is_None] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season,RasPi_SerialNum)
        print("Calculation Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()

        #progress_num=progress_num+1

        try:
            print("Labeling...")
            Checked_Today_Area_List = def_Labeling_by_Coordinates.Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None, num_of_object,RasPi_SerialNum)
            print("Labeling Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
            print()
        except:
            print('error 変更前のデータを記録します。')
            def_Labeling_by_Coordinates.Record(Today_Record_List_When_Latest_Data_is_None, Conventional_Area_List, Today_Coordinates_List, Season, fname, num_of_object,RasPi_SerialNum)
            Checked_Today_Area_List=Conventional_Area_List

        '''
        print("Sanding messeges...")
        def_Send_the_message.send_message(RasPi_SerialNum, fname, Checked_Today_Area_List) #本番
        print("Sending Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()
        '''

        print("Saving Picture...")
        def_Save_the_picture.save_the_picture(RasPi_SerialNum, fname) #本番
        print("Saved Pictures!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()

        print("finish program...")
        #def_finish.organize_on_Mac(fname, Season, RasPi_SerialNum)
        print("Everything is fine!!! Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')

    except:
        print("エラー　画像が見つかりません。")

if __name__ == '__main__':
    Season, num_of_object=Setting()
    #Information_csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Input/Information/Information_RasPi_and_API.csv", sep=",", index_col="RasPi_SerialNum",engine="python")
    #print(Information_csv_input)
    #API_unFilter=Information_csv_input.loc[RasPi_SerialNum,"Dropbox_API_unFilter"]
    #API_Filter=Information_csv_input.loc[RasPi_SerialNum,"Dropbox_API_Filter"]

    Start_Day="2019-09-03"
    End_Day="2019-09-03"

    Start_Day= datetime.strptime(Start_Day, '%Y-%m-%d')

    #today = datetime.today()
    #End_Day= datetime.strftime(End_Day, '%Y-%m-%d')
    End_Day= datetime.strptime(End_Day, '%Y-%m-%d')

    Difference=End_Day-Start_Day
    Difference=abs(Difference.days)

    RasPi_SerialNum=def_Identifying_RasPi.manual_select()
    print("RasPi-CPU : ", RasPi_SerialNum)
    print("Idenitfying RasPi-CPU Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    for i in range(0,int(Difference)+1):
        print(i)

        theDate = Start_Day + timedelta(days=(i))
        theDate = datetime.strftime(theDate, '%Y-%m-%d')
        print(theDate)
        #theDate=theDate+"-"+"07-00"
        #theDate=input('保存できてない日付を入力：')

        print('- -<%s>- - - - - - - - - - - - - - - - - - - - - - - - -' % theDate)
        main(theDate, RasPi_SerialNum)
