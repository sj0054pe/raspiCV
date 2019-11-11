import subprocess

def take_the_picture(fname): #写真を撮影する
    print(fname)
    try:
        subprocess.getoutput('raspistill -w 400 -h 500 -n -o ../../%s' % fname) #ラズパイカメラで撮影した画像はデストップに一時保存(後でos.removeで削除する。) #RaspberryPi
        return fname
    except:
        #fname='MassObservation_S6_2019-10-03-07-00.png' #Mac
        fname='Sample.jpeg' #Mac
        return fname
