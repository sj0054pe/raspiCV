import datetime

def check_the_date(Season):
    dates=datetime.datetime.now()
    exept_microsec=dates.strftime("%Y-%m-%d-%H-%M")
    print('[Today : %s]' % str(exept_microsec))
    fname=Season+"_"+exept_microsec+'.png'
    theDate=dates.strftime("%Y-%m-%d")
    return fname, theDate
