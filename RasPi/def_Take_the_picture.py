import subprocess

def take_the_picture(fname): #写真を撮影する
    try:
        subprocess.run('raspistill -w 400 -h 500 -n -o ../../%s' % fname) #ラズパイカメラで撮影した画像はデストップに一時保存(後でos.removeで削除する。) #RaspberryPi
        print(fname,"を利用します。")
        return fname
    except:
        fname='MassObservation_S7_2019-10-29-07-00.png' #Mac
        print('変更：保存されている写真を利用します。')
        print(fname)
        #fname='Sample.jpeg' #Mac
        return fname
