import dropbox

def Upload_on_Dropbox(API, Picname, RasPi_SerialNum): #DropboxのAPIを利用するためのテンプレ
    dbx = dropbox.Dropbox(API)
    dbx.users_get_current_account()
    print(Picname)
    Desktop_Picname=Picname
    Picname=Picname.split('.')
    Picname=str(Picname[0])+'_'+RasPi_SerialNum+'.png'
    print(Picname)
    f = open('../../%s' % Desktop_Picname, 'rb')
    Area_or_not=Desktop_Picname.split('_')
    print("------")
    if Area_or_not[0]=='Area':
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_Filter_%s/%s' % (RasPi_SerialNum,Desktop_Picname)) #dropbox内のディレクトリを書く
    else:
        dbx.files_upload(f.read(),'/Dropbox/アプリ/Mapoly_unFilter_%s/%s' % (RasPi_SerialNum,Desktop_Picname)) #dropbox内のディレクトリを書く
    f.close()

def save_the_picture(RasPi_SerialNum, fname): #画像をクラウド(Dropbox)に保存する
    print('[RaspberryPi at %s]' % RasPi_SerialNum)
    if RasPi_SerialNum=='5324ee26':#5
        API_unFilter='pnEJapb3mPAAAAAAAAAA5ExZM4oZx2NfGumBApSJn1lT3zi9jbfn7Oc-1T4-NqpV'
        API_Area='pnEJapb3mPAAAAAAAAAA5VzQxrZiIlAAJRAAfJOGinpU6xD2zIMuktPuUdyobY8D'
    elif RasPi_SerialNum=='dd68d859':#6
        API_unFilter='pnEJapb3mPAAAAAAAAAA5moORyRk81XGbmpR9UAZAOROZ_jfoKjkylrZ7gn-P0fK'
        API_Area='pnEJapb3mPAAAAAAAAAA5_0TQoV1qcdJUhEUT98HgWvGJDCg-rCi-XXiJcTAe-Pd'
    elif RasPi_SerialNum=='cebabe86':#4
        API_unFilter='pnEJapb3mPAAAAAAAAAA6E9YgxmxuV1ZzWQICaXVBltXi3fZmWAr5M4J55PzAN14'
        API_Area='pnEJapb3mPAAAAAAAAAA6Wlsbr1NETPSM2Y0OlfYS9qlRgYsRbWeZaiT8Nv4Cq3e'
    elif RasPi_SerialNum=='712d5dde':#2
        API_unFilter='pnEJapb3mPAAAAAAAAAA6nNd0IwQnYBhLuW7GQNXV1cBEHmk8mjQHyxIIsdkXgum'
        API_Area='pnEJapb3mPAAAAAAAAAA63NDuOtdWn_7tYDg7GKbDI_l7nDqJipaJXokJSLZuwZ2'
    elif RasPi_SerialNum=='b6abc89e': #3
        API_unFilter='pnEJapb3mPAAAAAAAAAA7s6P0bPCTA9P81ZZP7R52ThXAkxDRqzgYqxtLQ-GM-wk'
        API_Area='pnEJapb3mPAAAAAAAAAA7X8YFACiPL1uNJJF5uTKZS2H32OLjIuCsbwln_xzkTS0'
    elif RasPi_SerialNum=='b4abbd7a': #1
        API_unFilter='pnEJapb3mPAAAAAAAAAA74vXf_Nj6crHubBynPX_ZSwB_WMpghR8gye2n6zWRmTa'
        API_Area='pnEJapb3mPAAAAAAAAAA8KPLYjE4QVoqfdbG4xV8Ijre0Jwxxd94PLXkZQeYJe5I'
    elif RasPi_SerialNum=='c310a350': #7
        API_unFilter='pnEJapb3mPAAAAAAAAAA8Z_DIcE5TrkhkYWB8fY3GOFmz1rndz4LrkUFtNLaezwU'
        API_Area='pnEJapb3mPAAAAAAAAAA8mK2hcnXVe_w0AnMcT6_5-iItrxcBd3vdBTLWBUtoSJi'
    elif RasPi_SerialNum=='5ae9b47f': #8
        API_unFilter='pnEJapb3mPAAAAAAAAABD5j497IjWUpvKkHup8EAamyIKyfTTJLEQkuz5BBTokhu'
        API_Area='pnEJapb3mPAAAAAAAAABDn1HIdTjVeMU5fid_TaUhqksALt3l1QJZ5-9t3H5DHHO'
    else:
        return

    Upload_on_Dropbox(API_unFilter, fname, RasPi_SerialNum) #Dropbox内に保存 ノーマルな写真
    Upload_on_Dropbox(API_Area, 'Area_%s' % fname, RasPi_SerialNum) #輪郭を記述した写真
