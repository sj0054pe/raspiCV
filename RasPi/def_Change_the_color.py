import cv2
import numpy as np

def change_the_color(fname): #カラー画像を緑&黒の画像にする
    print("ファイル名：", fname)
    frame=cv2.imread('~/Desktop/%s' % fname)
    # フレームをHSVに変換
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # 取得する色の範囲を指定する
    lower_green=np.array([20, 50, 50])
    upper_green=np.array([70, 255, 255])
    # 指定した色に基づいたマスク画像の生成
    img_mask=cv2.inRange(hsv, lower_green, upper_green)
    # フレーム画像とマスク画像の共通の領域を抽出する。
    img_color=cv2.bitwise_and(frame, frame, mask=img_mask)
    #下の関数へ受け渡すためにデスクトップに一時保存(後でremoveで消します。)
    cv2.imwrite('~/Desktop/Green.png', img_color) #Green.pngは黒色背景にジェンマの画像があります。
