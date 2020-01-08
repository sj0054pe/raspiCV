import os
import shutil

def organize_on_Mac(fname, Season, RasPi_SerialNum):
    if not os.path.isdir("Assets/Assets_Output/%s" % Season):
        os.mkdir("Assets/Assets_Output/%s" % Season)
    if not os.path.isdir("Assets/Assets_Output/%s/%s" % (Season, RasPi_SerialNum)):
        os.mkdir("Assets/Assets_Output/%s/%s" % (Season, RasPi_SerialNum))

    shutil.move("~/Desktop/%s" % fname, "Assets/Assets_Output/%s/%s/%s" % (Season, RasPi_SerialNum, fname))
    shutil.move("~/Desktop/Area_%s" % fname, "Assets/Assets_Output/%s/%s/Area_%s" % (Season, RasPi_SerialNum, fname))

    #os.remove('../../%s' % fname)
    os.remove('~/Desktop/Green.png')
    os.remove('~/Desktop/Contours_on_%s' % fname)
    try:
        os.remove('~/Desktop/pre_Area_%s' % fname)
        #os.remove('../../Area_%s' % fname)
    except:
        print('remove に失敗')
    print('不必要な画像を削除します。')

def organize_on_RasPi(fname):
    os.remove('~/Desktop/%s' % fname)
    os.remove('~/Desktop/Green.png')
    os.remove('~/Desktop/Contours_on_%s' % fname)
    try:
        os.remove('~/Desktop/pre_Area_%s' % fname)
        os.remove('~/Desktop/Area_%s' % fname)
    except:
        print('remove に失敗')
    print('不必要な画像を削除します。')
