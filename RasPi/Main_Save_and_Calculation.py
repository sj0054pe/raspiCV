import def_Set_picname_on_Mac
import def_Change_the_color
import def_Calculation_from_Contours
import def_Labeling_by_Coordinates
import def_Identifying_RasPi
import def_Send_the_message
import def_Save_the_picture
import def_finish

from datetime import datetime, date, timedelta
import math

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

#Season=input("When is the Season? ex) S3 : ") #本番
Season="S7" #テスト
#print("ex)2019年07月20日") #本番
#Start_Day=input("Start Date : ") #本番
Start_Day="2019-10-29" #テスト
Start_Day=datetime.strptime(Start_Day, '%Y-%m-%d')

#print("ex)2019年08月10日") #本番
#End_Day=input("End Date : ") #本番
End_Day ="2019-10-29" #テスト
#today=datetime.strftime(today, '%Y-%m-%d')
#today=datetime.strptime(today, '%Y-%m-%d')

End_Day=datetime.strptime(End_Day, '%Y-%m-%d')

Difference=End_Day-Start_Day
Difference=abs(Difference.days)

for i in range(int(Difference)+1):
    j=int(Difference)-i
    theDate = End_Day - timedelta(days=(j))
    theDate = datetime.strftime(theDate, '%Y-%m-%d')
    #theDate = datetime.strftime(theDate, '%Y-%m-%d')
    print(theDate)

    #theDate=theDate+"-"+"07-00"
    theDate_with_time=theDate+"-"+"07-00"
    #theDate=input('保存できてない日付を入力：')

    try:
        fname=def_Set_picname_on_Mac.make_the_filename(Season, theDate_with_time)

        def_Change_the_color.change_the_color(fname)

        [Conventional_Area_List, contours] = def_Calculation_from_Contours.draw_the_contours(fname, theDate)

        Checked_Today_Area_List = def_Labeling_by_Coordinates.Labeling(fname, Conventional_Area_List, contours, theDate)

        RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()

        #def_Send_the_message.send_message(RasPi_SerialNum, fname, Checked_Today_Area_List) #本番

        #def_Save_the_picture.save_the_picture(RasPi_SerialNum, fname) #本番

        def_finish.organize(fname)
    except:
        print('Not Found...')
