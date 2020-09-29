import cv2

def Video_to_picture():
    path_input="../../Assets/Assets_Input/"
    fname_input="768x576.avi"
    cap = cv2.VideoCapture('%s%s' % (path_input, fname_input))
    end_flag, frame = cap.read()

    while(end_flag):
        #処理したい画像を選択
        #img_name = 'pedestrian4.jpg'

        # HoG特徴量の計算
        hog = cv2.HOGDescriptor()

        # サポートベクタマシンによる人検出
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.2}
        print(hogParams)

        # 人を検出した座標
        human, r = hog.detectMultiScale(frame, **hogParams)

        # バウンディングボックス
        for (x, y, w, h) in human:
            cv2.rectangle(frame, (x, y),(x+w, y+h),(0,50,255), 3)

        # 検出した画像を保存
        cv2.imshow('SVM', frame)

        #cv2.imwrite('out_default_%s.jpeg' % i,im)

        # ESCキー押下で終了
        if cv2.waitKey(30) & 0xff == 27:
            break

        #次のフレームへ移動
        try:
            _, frame = cap.read()
        except:
            cap = cv2.VideoCapture('%s%s' % (path_input, fname_input))
            end_flag, frame = cap.read()

def main():
    Video_to_picture()

if __name__ =='__main__':
    main()
