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
