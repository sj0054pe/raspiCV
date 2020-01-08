import datetime

def check_the_date(Season, RasPi_SerialNum):
    dates=datetime.datetime.now()
    exept_microsec=dates.strftime("%Y-%m-%d-%H-%M")
    print('[Today : %s]' % str(exept_microsec))
    #fname=RasPi_SerialNum+"_"+Season+"_"+exept_microsec+'.png'
    theDate=dates.strftime("%Y-%m-%d")
    fname=RasPi_SerialNum+"_"+Season+"_"+theDate+'.png'
    return fname, theDate
