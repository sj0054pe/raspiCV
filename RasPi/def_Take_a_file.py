import subprocess

def make_the_filename(theDate, Season, RasPi_SerialNum): #ファイル名を撮影日時する
    fname=RasPi_SerialNum+"_"+Season+"_"+theDate+'.png'
    print(fname)
    return fname

def take_the_picture(fname): #写真を撮影する
    try:
        subprocess.getoutput('raspistill -w 400 -h 500 -n -o ~/Desktop/%s' % fname) #ラズパイカメラで撮影した画像はデストップに一時保存(後でos.removeで削除する。) #RaspberryPi
        print('[撮影成功]')
        print(fname,"を利用します。")
        return fname
    except:
        print('[撮影失敗]')
        fname='MassObservation_S7_2019-10-29-07-00.png' #Mac
        print('変更：保存されている写真を利用します。')
        print(fname)
        #fname='Sample.jpeg' #Mac
        return fname
