import def_datetime
import def_Take_the_picture
import def_Change_the_color
import def_Calculation_from_Contours
import def_Labeling_by_Coordinates
import def_Identifying_RasPi
import def_Send_the_message
import def_Save_the_picture
import def_finish

import time
TimeMeasurement = time.time()

try:
    progress_num=0
    Season="S8"

    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()
    print("RasPi-CPU : ", RasPi_SerialNum)

    print("Check date...")
    fname, theDate = def_datetime.check_the_date(Season)
    print("Check date Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Taking Picture... ")
    fname = def_Take_the_picture.take_the_picture(fname)
    print("Take Picture Done!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Finding Green...")
    def_Change_the_color.change_the_color(fname)
    print("Found Leaves!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Calculating the Area...")
    [Conventional_Area_List, Today_Coordinates_List, Today_Record_List_When_Latest_Data_is_None] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season)
    print("Calculation Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    progress_num=progress_num+1

    try:
        print("Labeling...")
        Checked_Today_Area_List = def_Labeling_by_Coordinates.Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season, Today_Record_List_When_Latest_Data_is_None)
        print("Labeling Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
        print()
    except:
        print('error 変更前のデータを記録します。')
        def_Labeling_by_Coordinates.Record(Today_Record_List_When_Latest_Data_is_None, Conventional_Area_List, Today_Coordinates_List, Season, fname)

    print("Sanding messeges...")
    def_Send_the_message.send_message(RasPi_SerialNum, fname, Checked_Today_Area_List) #本番
    print("Sending Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("Saving Picture...")
    def_Save_the_picture.save_the_picture(RasPi_SerialNum, fname) #本番
    print("Saved Pictures!   "+ str(time.time() - TimeMeasurement) + 'sec')
    print()

    print("finish program...")
    def_finish.organize(fname)
    print("Everything is fine!!! Done!!   "+ str(time.time() - TimeMeasurement) + 'sec')

except:
    if progress_num<1:
        [Conventional_Area_List, Today_Coordinates_List] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season)
