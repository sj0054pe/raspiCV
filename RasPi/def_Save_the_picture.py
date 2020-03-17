import dropbox
import csv
import pandas as pd

def Upload_on_Dropbox(API, Picname, RasPi_SerialNum): #DropboxのAPIを利用するためのテンプレ
    dbx = dropbox.Dropbox(API)
    dbx.users_get_current_account()
    f = open('../../%s' % Picname, 'rb')
    Area_or_not=Picname.split('_')
    if Area_or_not[0]=='Area':
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_Filter_%s/%s' % (RasPi_SerialNum, Picname)) #dropbox内のディレクトリを書く
    else:
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_unFilter_%s/%s' % (RasPi_SerialNum,Picname)) #dropbox内のディレクトリを書く
    f.close()

def save_the_picture(RasPi_SerialNum, fname):
    Information_csv_input = pd.read_csv(filepath_or_buffer="Assets/Assets_Input/Information/Information_RasPi_and_API.csv", sep=",", index_col="RasPi_SerialNum",engine="python")
    #print(Information_csv_input)
    API_unFilter=Information_csv_input.loc[RasPi_SerialNum,"Dropbox_API_unFilter"]
    API_Filter=Information_csv_input.loc[RasPi_SerialNum,"Dropbox_API_Filter"]

    Upload_on_Dropbox(API_unFilter, fname, RasPi_SerialNum)
    Upload_on_Dropbox(API_Filter, 'Area_%s' % fname, RasPi_SerialNum)
    '''
    try:
        Upload_on_Dropbox(API_unFilter, fname, RasPi_SerialNum) #Dropbox内に保存 ノーマルな写真
    except:
        print('すでに%sはDropbox上に保存してあります。' % fname)
    try:
        Upload_on_Dropbox(API_Area, 'Area_%s' % fname, RasPi_SerialNum) #輪郭を記述した写真
    except:
        print('すでにArea_%sはDropbox上に保存してあります。' % fname)
    '''
def main():
    RasPi_SerialNum="5324ee26" #例
    fname="5324ee26_MAYO_2019-09-03.png" #例
    save_the_picture(RasPi_SerialNum, fname)

if __name__ == '__main__':
    main()
