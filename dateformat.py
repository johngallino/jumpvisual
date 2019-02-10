
def parseDate(origdate):
    """ formats a mm/dd """
    
    if origdate is '':
        origdate = '00/00'

    try:
        split = origdate.split('/')
        month = int(split[0])
    except:
        return 'error'
    
    try:
        day = int(split[1])
    except:
        day = 0
        
    formatedDate = ''
    if month == 1:
        formatedDate += 'Jan '
    elif month == 2:
        formatedDate += 'Feb '
    elif month == 3:
        formatedDate += 'Mar '
    elif month == 4:
        formatedDate += 'Apr '
    elif month == 5:
        formatedDate += 'May '
    elif month == 6:
        formatedDate += 'June '
    elif month == 7:
        formatedDate += 'July '
    elif month == 8:
        formatedDate += 'Aug '
    elif month == 9:
        formatedDate += 'Sept '
    elif month == 10:
        formatedDate += 'Oct '
    elif month == 11:
        formatedDate += 'Nov '
    elif month == 12:
        formatedDate += 'Dec '
    else:
        formatedDate += 'ERROR '
        
    gix = str(day)
    print('GIX is ' + gix)
    if day < 1 or day > 31:
        formatedDate += 'ERROR'

    elif gix.startswith('1'):
        formatedDate += str(day) + 'th'
    elif gix.endswith('1'):
            formatedDate += str(day) + 'st'
    elif gix.endswith('2'):
            formatedDate += str(day) + 'nd'
    elif gix.endswith('3'):
            formatedDate += str(day) + 'rd'
    else:
        formatedDate += str(day) + 'th'
    #print(formatedDate)
    
    return formatedDate

#print(parseDate('15/142'))