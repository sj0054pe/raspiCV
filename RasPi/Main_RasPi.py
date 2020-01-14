import time
TimeMeasurement = time.time()

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

import os
try:
    os.chdir('/home/pi/Desktop/raspiCV/RasPi')
except:
    print("ラズパイではありません。")

try:
    #初期設定
    progress_num=0 #プログラムの進行度を測る番号(main関数内のexcept時に使う。)
    Season="S8" #シーズンごとに変更する。(いろんなモジュールに存在するSeasonはここから派生しているのでこの部分の変更をするだけでいい。)
    num_of_object=8+1 #個体数 6はゼニゴケの数、1はスケール

    #ラズパイの特定
    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    print("RasPi-CPU : ", RasPi_SerialNum)
    print("Idenitfying RasPi-CPU Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    #日付を取得
    print("Check date...")
    fname, theDate = def_datetime.check_the_date(Season, RasPi_SerialNum)
    print("Check date Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    #写真を撮影
    print("Taking Picture... ")
    fname = def_Take_a_file.take_the_picture(fname)
    print("Take Picture Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    #葉を検出
    print("Finding Green...")
    def_Change_the_color.change_the_color(fname)
    print("Found Leaves!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    #輪郭を認識したのちに面積と座標を導出
    print("Calculating the Area...")
    [Conventional_Area_List, Today_Coordinates_List, Today_Record_List_When_Latest_Data_is_None] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season,RasPi_SerialNum)
    print("Calculation Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    progress_num=progress_num+1

    #個体番号を識別したのち写真にラベリング処理を開始
    try:
        print("Labeling...")
        Checked_Today_Area_List = def_Labeling_by_Coordinates.Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None, num_of_object,RasPi_SerialNum)
        print("Labeling Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()
    except:
        print('error 変更前のデータを記録します。')
        def_Labeling_by_Coordinates.Record(Today_Record_List_When_Latest_Data_is_None, Conventional_Area_List, Today_Coordinates_List, Season, fname, num_of_object,RasPi_SerialNum)
        Checked_Today_Area_List=Conventional_Area_List

    #LINEを送信
    print("Sanding messeges...")
    def_Send_the_message.send_message(RasPi_SerialNum, fname, Checked_Today_Area_List) #本番
    print("Sending Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    #Dropboxに保存
    print("Saving Picture...")
    def_Save_the_picture.save_the_picture(RasPi_SerialNum, fname) #本番
    print("Saved Pictures!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    #必要のないプログラムは削除
    print("finish program...")
    def_finish.organize_on_RasPi(fname)
    print("Everything is fine!!! Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')

except:
    try:
        #途中で終わってしまったら撮影した写真はDropboxに保存したらローカルストレージから削除するようにする。
        def_Save_the_picture.save_the_picture(RasPi_SerialNum, fname) #本番
        progress_num=2
        Checked_Today_Area_List="ソフトの動作に不具合が発生しました。"+'\n'+"Dropboxへの保存は完了しています。"
        def_Send_the_message.send_message(RasPi_SerialNum, fname, Checked_Today_Area_List)
    except:
        if progress_num==2:
            def_finish.organize_on_RasPi(fname)

    if progress_num<1:
        [Conventional_Area_List, Today_Coordinates_List] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season)
