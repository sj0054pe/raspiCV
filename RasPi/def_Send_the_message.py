import requests

def send_message(RasPi_SerialNumber, fname, Checked_Today_Area_List): #LINEのAPIを利用するためのテンプレ(面積と画像を送信する)
    url = "https://notify-api.line.me/api/notify"   #line notifyでラズパイからlineに画像を送信
    token = '2Rm15NEZNBO8A8kLZHAmKXBAk4fnwOnxQMJCknwdw4p'   #lineのtoken
    headers = {"Authorization" : "Bearer "+ token}
    RasPi_Number='[picamera_%s]' % RasPi_SerialNumber
    Picname_LINE="Area_" + fname
    Area_7=''
    j=0
    print("making message...")
    for i in Checked_Today_Area_List:
        Area_7=Area_7+str(j)+'_'+str(i)+'\n'
        j+=1
    message =  RasPi_Number+ '\n'+ Picname_LINE + '\n' + '面積の記録成功です。\n'+Area_7
    payload = {"message" :  message}
    files = {"imageFile": open("../../%s" % Picname_LINE, "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。
    r = requests.post(url ,headers = headers ,params=payload, files=files)
    #os.remove("/home/pi/Desktop/%s" % fname)
