import math
import re
import os

def Compare_these_Coordinates(Today_Coordinates_List, Yesterday_Coordinates_List, theDate,RasPi_SerialNum):

    if Yesterday_Coordinates_List=="No_Data": #観察初日に参照する前日のデータがあるorないで条件分岐。
        print('昨日の記録に関してNo_Dataを確認。')
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

        #print(Yesterday_Coordinates_List)
        for i in range(1,int(len(Today_Coordinates_List))): #日付もリストに含まれてるから-1する
            print(i)
            #print(Today_Coordinates_List[i])
            [Today_X,Today_Y]=Today_Coordinates_List[i].split(",")
            right_num, nearest_r=1000, 1000 #初期値なのであり得ない数字を入れておく
            #dict_iのiはToday_Coordinates_List[i]のi。
            exec("List_ToCoordinates_YeCoordinates_r_num_%s=[]" % str(i))
            exec("List_ToCoordinates_YeCoordinates_r_num_%s.append(Today_Coordinates_List[%s])" % (str(i),i))

            for j in range(1,int(len(Yesterday_Coordinates_List))): #日付もリストに含まれてるから-1する #未確認
                print(j)
                print(Yesterday_Coordinates_List[j])
                if re.search("-",str(Yesterday_Coordinates_List[j])):
                    continue
                elif re.search("nan",str(Yesterday_Coordinates_List[j])):
                    continue
                [Yesterday_X,Yesterday_Y]=str(Yesterday_Coordinates_List[j]).split(",")
                print("(",Today_X,",",Today_Y,") / (",Yesterday_X,",",Yesterday_Y,")")
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

        for m in range(1,int(len(Today_Coordinates_List))):
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
        num=0
        count_for_Loser=0
        for element in Checked_Today_Coordinates_List:
            print('Coordinates : ', element)
            if element =="NA":
                print("NA発見")
                if int(num) > int(len(Loser_ToCoordinates_List)):
                    break
                Checked_Today_Coordinates_List[num]=Loser_ToCoordinates_List[count_for_Loser]
                count_for_Loser=count_for_Loser+1
            print(num)
            print(count_for_Loser)
            num=num+1 #ただ単にループした回数を数えているだけ。だからnumでもいい。

        Checked_Today_Coordinates_List.insert(0,Today_Coordinates_List[0]) #日付を代入する。
        print('Checked_Today_Coordinates_List : ', Checked_Today_Coordinates_List)

        return Checked_Today_Coordinates_List

def main(): #不完全
    Compare_these_Coordinates(Today_Coordinates_List, Yesterday_Coordinates_List, theDate)

    return 0

if __name__ == '__main__':

    main()
