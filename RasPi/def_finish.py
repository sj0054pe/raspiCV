import os

def organize_on_Mac(fname):
    if not os.path.isdir("Assets/Assets_Output/%s" % Season):
        os.mkdir("Assets/Assets_Output/%s/%s" % Season)
    if not os.path.isdir("Assets/Assets_Output/%s/%s" % (Season, RasPi_SerialNum)):
        os.mkdir("Assets/Assets_Output/%s/%s" % (Season, RasPi_SerialNum))

    os.move("../../%s Assets/Assets_Output/%s/%s/%s" % (fname, Season, RasPi_SerialNum, fname))
    os.move('../../%s Assets/Assets_Output/%s/%s/Area_%s' % (fname, Season, RasPi_SerialNum, fname))

    #os.remove('../../%s' % fname)
    os.remove('../../Green.png')
    os.remove('../../Contours_on_%s' % fname)
    try:
        os.remove('../../pre_Area_%s' % fname)
        #os.remove('../../Area_%s' % fname)
    except:
        print('remove に失敗')
    print('不必要な画像を削除します。')

def organize_on_RasPi(fname):
    os.remove('../../%s' % fname)
    os.remove('../../Green.png')
    os.remove('../../Contours_on_%s' % fname)
    try:
        os.remove('../../pre_Area_%s' % fname)
        os.remove('../../Area_%s' % fname)
    except:
        print('remove に失敗')
    print('不必要な画像を削除します。')
