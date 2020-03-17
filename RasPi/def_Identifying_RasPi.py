def manual_select():
    print("どのRaspberryPiを選びますか?")
    RasPi_dict={}
    RasPi_dict[3]='b4abbd7a' #b4abbd7aは3
    RasPi_dict[2]='5ae9b47f' #練習用
    RasPi_dict[8]='b6abc89e' #b6abc89eは8
    RasPi_dict[4]='cebabe86' #cebabe86は4
    RasPi_dict[5]='5324ee26' #5324ee26は5
    RasPi_dict[6]='dd68d859' #dd68d859は6
    RasPi_dict[7]='c310a350' #c310a350は7
    RasPi_dict[1]='712d5dde' #712d5ddeは1

    for i in range(1,8+1): #8はラズベリーパイの数
        print(i,",", RasPi_dict[i])

    RasPi_Number=input('数字を半角で入力 例)1 : ')
    RasPi_SerialNum=RasPi_dict[int(RasPi_Number)]

    return RasPi_SerialNum

def Get_Serial(): #ラズパイのCPU晩報を取得する(各ラズパイを識別するため)
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[18:26]
    f.close()
  except:
    cpuserial = "5ae9b47f" #テスト用CPU番号 #8番ラズペリーパイ

  return cpuserial
