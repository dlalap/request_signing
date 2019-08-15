import datetime

def generateCurrentDate():
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hour = str(now.time().hour).zfill(2)
    minute = str(now.time().minute).zfill(2)
    second = str(now.time().second).zfill(2)
    microsecond = str(now.time().microsecond).zfill(2)

    dtString = "{}-{}-{}T{}:{}:{}.000-08:00".format(year, month, day, hour, minute, second)

    return dtString