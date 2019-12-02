import os

def organize(fname):
    os.remove('../../%s' % fname)
    os.remove('../../Green.png')
    os.remove('../../Contours_on_%s' % fname)
    os.remove('../../pre_Area_%s' % fname)
    os.remove('../../Area_%s' % fname)
    print('不必要な画像を削除します。')
