import def_datetime
import def_Take_the_picture
import def_Change_the_color
import def_Calculation_from_Contours
import def_Labeling_by_Coordinates
import def_Identifying_RasPi
import def_Send_the_message
import def_Save_the_picture
import def_finish

try:
    progress_num=0
    Season="S7"

    RasPi_SerialNum=def_Identifying_RasPi.Get_Serial()

    fname, theDate = def_datetime.check_the_date()

    fname = def_Take_the_picture.take_the_picture(fname)

    def_Change_the_color.change_the_color(fname)

    [Conventional_Area_List, Today_Coordinates_List] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season)

    progress_num=progress_num+1

    Checked_Today_Area_List = def_Labeling_by_Coordinates.Labeling(fname, Conventional_Area_List, Today_Coordinates_List, theDate, Season)

    def_Send_the_message.send_message(RasPi_SerialNum, fname, Checked_Today_Area_List) #本番

    def_Save_the_picture.save_the_picture(RasPi_SerialNum, fname) #本番

    def_finish.organize(fname)

except:
    if progress_num<1:
        [Conventional_Area_List, Today_Coordinates_List] = def_Calculation_from_Contours.draw_the_contours(fname, theDate, Season)
