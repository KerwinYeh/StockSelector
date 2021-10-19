
# Functoin of get datelist for crawldata
def dateforGetData(todayWeek, today):
    if todayWeek == 7:
        datelist = [str(int(today) - 3), str(int(today) - 2)]
    elif todayWeek == 1:
        datelist = [str(int(today) - 4), str(int(today) - 3)]
    elif todayWeek == 2:
        datelist = [str(int(today) - 4), str(int(today) - 1)]
    else:
        datelist = [str(int(today) - 2), str(int(today) - 1)]
    
    return datelist 