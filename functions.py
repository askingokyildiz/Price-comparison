def monthint(aysayi):
    if aysayi == "Ocak":
        a=1
        return (a)
    elif aysayi == "Şubat":
        a=2
        return (a)
    elif aysayi == "Mart":
        a=3
        return (a)
    elif aysayi == "Nisan":
        a=4
        return (a)
    elif aysayi == "Mayıs":
        a=5
        return (a)
    elif aysayi == "Haziran":
        a=6
        return (a)
    elif aysayi == "Temmuz":
        a=7
        return (a)
    elif aysayi == "Ağustos":
        a=8
        return (a)
    elif aysayi == "Eylül":
        a=9
        return (a)
    elif aysayi == "Ekim":
        a=10
        return (a)
    elif aysayi == "Kasım":
        a=11
        return (a)
    else:
        a=12
        return (a)

def aystr(aystring):
    if aystring == 1:
        b="Ocak"
        return (b)
    elif aystring == 2:
        b="Şubat"
        return (b)
    elif aystring == 3:
       b="Mart"
       return (b)
    elif aystring == 4:
       b="Nisan"
       return (b)
    elif aystring == 5:
       b="Mayıs"
       return (b)
    elif aystring == 6:
       b="Haziran"
       return (b)
    elif aystring == 7:
       b="Temmuz"
       return (b)
    elif aystring == 8:
       b="Ağustos"
       return (b)
    elif aystring == 9:
      b="Eylül"
      return (b)
    elif aystring ==10 :
     b="Ekim"
     return (b)
    elif aystring == 11 :
        b="Kasım"
        return (b)
    else:
       b="Aralık"
       return (b)
       
def daterange(defaultmonth, defaultyear, month_entry, year_entry):
    defaultmonth = monthint(defaultmonth)
    defaultyear=int(defaultyear)
    if defaultyear == year_entry:
        if defaultmonth == month_entry:
            monthdifference = 0
        else:
            monthdifference = month_entry - defaultmonth
        return monthdifference
    else:
        if defaultmonth == month_entry:
            monthdifference=12
        elif defaultmonth > month_entry:
            missingmonth = defaultmonth - month_entry
            monthdifference = 12 - missingmonth
        else:
            missingmonth = month_entry - defaultmonth
            monthdifference = 12 + missingmonth
        return monthdifference
    return monthdifference

def tariharaligi(varsayilanay, varsayilanyil, istenilenay, istenilenyil):
    vsylnay = ayint(varsayilanay)
    istenilenyil=str(istenilenyil)
    if varsayilanyil == istenilenyil:
        if vsylnay == istenilenay:
            ayfarki = 0
        else:
            ayfarki = istenilenay - vsylnay
        return ayfarki
    else:
        if vsylnay == istenilenay:
            ayfarki=12
        elif vsylnay > istenilenay:
            eksikay = vsylnay - istenilenay
            ayfarki = 12 - eksikay
        else:
            eksikay = istenilenay - vsylnay
            ayfarki = 12 + eksikay
        return ayfarki
    return ayfarki

#print(tariharaligi("Şubat", 2020, 7, 2020))