from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlwt
import threading
from hoteltd import hotelList
from functions import monthint, aystr, tariharaligi, daterange
from datetime import datetime, date

start = time.perf_counter()

date_entry = input('Giriş Tarihi (ör: 07-07-2020)')
date_release = input('Çıkış Tarihi (ör: 12-07-2020)')
day_entry, month_entry, year_entry = map(int, date_entry.split('-'))
day_release, month_release, year_release = map(int, date_release.split('-'))
e_date = datetime(year_entry, month_entry, day_entry)
r_date = datetime(year_release, month_release, day_release)
delta = r_date - e_date

targirisgun= day_entry
targirisguntd= targirisgun-1
targirisguntd= str(targirisguntd)
targirisay= month_entry
targirisyil= year_entry
tarcikisgun=day_release
tarcikisguntd=tarcikisgun-1
tarcikisguntd=str(tarcikisguntd)
tarcikisay=month_release
tarcikisyil=year_release
gunsayisi=delta.days
tatilcomcheckin= date(year_entry, month_entry, day_entry)
tatilcomcheckout= date(year_release, month_release, day_release)
tatildukkanicheckin= str(day_entry)+'.'+str(month_entry)+'.'+ str(year_entry)
tatildukkanicheckout= str(day_release)+'.'+str(month_release)+'.'+ str(year_release)
tatilcomurlek='?pax=2&checkin=' + str(tatilcomcheckin) + '&checkout=' + str(tatilcomcheckout)
tatildukkaniurlek='?checkin='+tatildukkanicheckin+'&checkout='+tatildukkanicheckout+'&adult=2&child=0&child1_age=1&child2_age=1&airport=SAW'
tsepetiurlek='?ara=oda:2;tarih:'+tatildukkanicheckin+','+tatildukkanicheckout+'&up=tab:1;from:saw'
tbudururlek='?checkInDate='+tatildukkanicheckin+'&checkOutDate='+tatildukkanicheckout+'&adult=2,'
touristicaday, touristicamonth, touristicayear= map(str, date_entry.split('-'))
touristicacheckin=touristicaday+"."+touristicamonth+"."+touristicayear
touristicaday, touristicamonth, touristicayear= map(str, date_release.split('-'))
touristicacheckout=touristicaday+"."+touristicamonth+"."+touristicayear

mngturizmday, mngturizmmonth, mngturizmyear= map(str, date_entry.split('-'))
mngturizmcheckin=mngturizmday+"/"+mngturizmmonth+"/"+mngturizmyear
mngturizmday, mngturizmmonth, mngturizmyear= map(str, date_release.split('-'))
mngturizmcheckout=mngturizmday+"/"+mngturizmmonth+"/"+mngturizmyear
mngturizmurlek="?CheckIn="+mngturizmcheckin+"&CheckOut="+mngturizmcheckout+"&AC=2&CC=0&CA1=1&CA2=1&CA3=1&CA4=1&CA5=1&CA6=1"
#Excel Yapısı
fontBold = xlwt.Font()
fontBold.bold = True    #  bold 
fontBold.name = 'Calibri'   #  select the font
fontBold.height = 220  #  the font size 

fontRegular = xlwt.Font()
fontRegular.bold = False    #  bold 
fontRegular.name = 'Calibri'   #  select the font
fontRegular.height = 220  #  the font size 

borders = xlwt.Borders()
borders.left = borders.THIN
borders.right = borders.THIN
borders.top = borders.THIN
borders.bottom = borders.THIN

#Yatay ortalama
alignmentcenter = xlwt.Alignment()
alignmentcenter.horz = xlwt.Alignment.HORZ_CENTER

#Otel Başlık Renk
bgoteltitle = xlwt.Pattern()
bgoteltitle.pattern = bgoteltitle.SOLID_PATTERN   # NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
bgoteltitle.pattern_fore_colour = xlwt.Style.colour_map['light_yellow']

#Otel İçerik Renk
bgotelcontent = xlwt.Pattern()
bgotelcontent.pattern = bgotelcontent.SOLID_PATTERN   # NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
bgotelcontent.pattern_fore_colour = xlwt.Style.colour_map['light_yellow']

#TatilDükkanı İçerik Renk
bgtdcontent = xlwt.Pattern()
bgtdcontent.pattern = bgtdcontent.SOLID_PATTERN   # NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
bgtdcontent.pattern_fore_colour = xlwt.Style.colour_map['ivory']

#Tatil.com İçerik Renk
bgtcomcontent = xlwt.Pattern()
bgtcomcontent.pattern = bgtcomcontent.SOLID_PATTERN   # NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
bgtcomcontent.pattern_fore_colour = xlwt.Style.colour_map['white']

#Tatil Sepeti İçerik Renk
bgtsepeticontent = xlwt.Pattern()
bgtsepeticontent.pattern = bgtsepeticontent.SOLID_PATTERN   # NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
bgtsepeticontent.pattern_fore_colour = xlwt.Style.colour_map['white']

#Başlık Sütunlar
style0 = xlwt.XFStyle()
style0.font = fontBold
style0.pattern = bgoteltitle
style0.borders = borders
style0.alignment = alignmentcenter

#oteller Sütun
style00 = xlwt.XFStyle()
style00.font = fontBold
style00.pattern = bgotelcontent
style00.borders = borders

#TatilDükkanı Sütun
style1 = xlwt.XFStyle()
style1.font = fontRegular
style1.pattern = bgtdcontent
style1.borders = borders

#Tatil.com Sütun
style2 = xlwt.XFStyle()
style2.font = fontRegular
style2.pattern = bgtcomcontent
style2.borders = borders

#Tatil.com Sütun
style3 = xlwt.XFStyle()
style3.font = fontRegular
style3.pattern = bgtsepeticontent
style3.borders = borders

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet('Fiyatlar')
ws.write_merge(0,1,0,0, "Oteller", style0)
ws.write_merge(0,0,1,4, "Tatil Dükkanı", style0)
ws.write(1, 1, "Fiyat", style0)
ws.write(1, 2, "Konsept", style0)
ws.write(1, 3, "Oda", style0)
ws.write(1, 4, "Uçak", style0)
ws.write_merge(0,0,5,9, "Tatil.com", style0)
ws.write(1, 5, "Fiyat", style0)
ws.write(1, 6, "Fark", style0)
ws.write(1, 7, "Konsept", style0)
ws.write(1, 8, "Oda", style0)
ws.write(1, 9, "Uçak", style0)
ws.write_merge(0,0,10,14, "Tatil Sepeti", style0)
ws.write(1, 10, "Fiyat", style0)
ws.write(1, 11, "Fark", style0)
ws.write(1, 12, "Konsept", style0)
ws.write(1, 13, "Oda", style0)
ws.write(1, 14, "Uçak", style0)
ws.write_merge(0,0,15,19, "Touristica", style0)
ws.write(1, 15, "Fiyat", style0)
ws.write(1, 16, "Fark", style0)
ws.write(1, 17, "Konsept", style0)
ws.write(1, 18, "Oda", style0)
ws.write(1, 19, "Uçak", style0)
ws.write_merge(0,0,20,24, "Tatil Budur", style0)
ws.write(1, 20, "Fiyat", style0)
ws.write(1, 21, "Fark", style0)
ws.write(1, 22, "Konsept", style0)
ws.write(1, 23, "Oda", style0)
ws.write(1, 24, "Uçak", style0)
ws.write_merge(0,0,25,29, "Mng Turizm", style0)
ws.write(1, 25, "Fiyat", style0)
ws.write(1, 26, "Fark", style0)
ws.write(1, 27, "Konsept", style0)
ws.write(1, 28, "Oda", style0)
ws.write(1, 29, "Uçak", style0)
ws.col(0).width = 7200
ws.col(4).width = 3500
ws.col(9).width = 3500
ws.col(14).width = 3500
ws.col(19).width = 3500
ws.col(24).width = 3500
ws.col(29).width = 3500

def tatildukkani():
    browser=webdriver.Firefox()
    rowplus=1
    for hotel in hotelList:
        rowplus=rowplus+1
        url=hotel[1]+tatildukkaniurlek
        browser.get(url)
        time.sleep(4)
        try:
            tdprice= browser.find_element_by_xpath("//*[@id='pck_price0']").text
            tdg= browser.find_element_by_xpath("//*[@id='d_dtime']").text
            tdc= browser.find_element_by_xpath("//*[@id='r_dtime']").text
            tdconcept= browser.find_elements_by_css_selector("#reservation_result > div.row > div.col-md-6.col-sm-12.col-xs-12 > ul > li > div.row > div.col-md-5.col-sm-5.col-xs-6.text-center.p0")[0].text
            tdconcept=tdconcept.splitlines()
            tdroom=tdconcept[0]
            tdconcept=tdconcept[1]
            fiyat, kusurat = map(str, tdprice.split('.'))
            tdprice1, tdprice2 = map(str, fiyat.split(','))
            tdprice=int(tdprice1+tdprice2)
        except:
            try:
                time.sleep(4)
                tdprice= browser.find_element_by_xpath("//*[@id='pck_price0']").text
                tdg= browser.find_element_by_xpath("//*[@id='d_dtime']").text
                tdc= browser.find_element_by_xpath("//*[@id='r_dtime']").text
                tdconcept= browser.find_elements_by_css_selector("#reservation_result > div.row > div.col-md-6.col-sm-12.col-xs-12 > ul > li > div.row > div.col-md-5.col-sm-5.col-xs-6.text-center.p0")[0].text
                tdconcept=tdconcept.splitlines()
                tdroom=tdconcept[0]
                tdconcept=tdconcept[1]
                fiyat, kusurat = map(str, tdprice.split('.'))
                tdprice1, tdprice2 = map(str, fiyat.split(','))
                tdprice=int(tdprice1+tdprice2)
            except:
                ws.write(rowplus, 0, hotel[0], style00)
                ws.write(rowplus, 1, "", style1)
                ws.write(rowplus, 2, "", style1)
                ws.write(rowplus, 3, "", style1)
                ws.write(rowplus, 4, "", style1)
            else:
                ws.write(rowplus, 0, hotel[0], style00)
                ws.write(rowplus, 1, tdprice, style1)
                ws.write(rowplus, 2, tdconcept, style1)
                ws.write(rowplus, 3, tdroom, style1)
                tdplanestime=tdg+' / '+tdc
                ws.write(rowplus, 4, tdplanestime, style1)
        else:
            ws.write(rowplus, 0, hotel[0], style00)
            ws.write(rowplus, 1, tdprice, style1)
            ws.write(rowplus, 2, tdconcept, style1)
            ws.write(rowplus, 3, tdroom, style1)
            tdplanestime=tdg+' / '+tdc
            ws.write(rowplus, 4, tdplanestime, style1)
    brower.close()

def tatilcom():
    browser=webdriver.Firefox()
    rowplus=1
    time.sleep(1)
    for hotel in hotelList:
        rowplus=rowplus+1
        url=hotel[2]+tatilcomurlek
        try:
            browser.get(url)
            time.sleep(7)
            browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_rblReservationType']/label[2]").click()
        except:
            try:
                browser.get(url)
                time.sleep(7)
                browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_rblReservationType']/label[2]").click()
            except:
                print("Site Error")
        try:
            time.sleep(10)
            tatilcomprice= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[4]/span/strong").text
            tatilcomg= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblDepartureFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
            tatilcomc= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblReturnFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
            tatilcomconcept= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h6").text
            tatilcomroom= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h5").text
        except:
            try:
                time.sleep(4)
                tatilcomprice= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[4]/span/strong").text
                tatilcomg= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblDepartureFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                tatilcomc= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblReturnFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                tatilcomconcept= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h6").text
                tatilcomroom= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h5").text
            except:
                try:
                    time.sleep(4)
                    tatilcomprice= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[4]/span/strong").text
                    tatilcomg= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblDepartureFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                    tatilcomc= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblReturnFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                    tatilcomconcept= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h6").text
                    tatilcomroom= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h5").text
                except:
                    tatilcomformulacol=rowplus+1
                    ws.write(rowplus, 5, "", style2)
                    ws.write(rowplus, 6, "", style2)
                    ws.write(rowplus, 7, "", style2)
                    ws.write(rowplus, 8, "", style2)
                    ws.write(rowplus, 9, "", style2) 
                else:    
                    tatilcomformulacol=rowplus+1
                    tatilcomformula='B'+str(tatilcomformulacol)+'-F'+str(tatilcomformulacol)
                    ws.write(rowplus, 5, int(tatilcomprice), style2)
                    ws.write(rowplus, 6, xlwt.Formula(tatilcomformula), style2)
                    ws.write(rowplus, 7, tatilcomconcept, style2)
                    ws.write(rowplus, 8, tatilcomroom, style2)
                    tatilcomplanestime=tatilcomg+' / '+tatilcomc
                    ws.write(rowplus, 9, tatilcomplanestime, style2) 
            else:    
                tatilcomformulacol=rowplus+1
                tatilcomformula='B'+str(tatilcomformulacol)+'-F'+str(tatilcomformulacol)
                ws.write(rowplus, 5, int(tatilcomprice), style2)
                ws.write(rowplus, 6, xlwt.Formula(tatilcomformula), style2)
                ws.write(rowplus, 7, tatilcomconcept, style2)
                ws.write(rowplus, 8, tatilcomroom, style2)
                tatilcomplanestime=tatilcomg+' / '+tatilcomc
                ws.write(rowplus, 9, tatilcomplanestime, style2) 
        else:    
            tatilcomformulacol=rowplus+1
            tatilcomformula='B'+str(tatilcomformulacol)+'-F'+str(tatilcomformulacol)
            ws.write(rowplus, 5, int(tatilcomprice), style2)
            ws.write(rowplus, 6, xlwt.Formula(tatilcomformula), style2)
            ws.write(rowplus, 7, tatilcomconcept, style2)
            ws.write(rowplus, 8, tatilcomroom, style2)
            tatilcomplanestime=tatilcomg+' / '+tatilcomc
            ws.write(rowplus, 9, tatilcomplanestime, style2) 
    brower.close()

def tsepeti():
    browser=webdriver.Firefox()
    rowplus=1
    for hotel in hotelList:
        rowplus=rowplus+1
        url=hotel[3]+tsepetiurlek
        try:
            browser.get(url)
            time.sleep(15)
            tsepetiprice= browser.find_elements_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div/div[1]/div/div[2]/div[1]/div[2]")
            tsepetiprice=tsepetiprice[0].text
            tsepetig= browser.find_element_by_xpath("//*[@id='divGidisUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
            tsepetic= browser.find_element_by_xpath("//*[@id='divDonusUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
            tsepeticoncept= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/p").text
            tsepetiroom= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/ul/li[1]/a").text
            fiyat, kusurat = map(str, tsepetiprice.split(','))
            tsepetiprice1, tsepetiprice2 = map(str, fiyat.split('.'))
            tsepetiprice=int(tsepetiprice1+tsepetiprice2)
            tatilsepetiplanestime=tsepetig+' / '+tsepetic
            tsepetiformulacol=rowplus+1
            tsepetiformula='B'+str(tsepetiformulacol)+'-K'+str(tsepetiformulacol)
        except:
            try:
                browser.get(url)
                time.sleep(15)
                tsepetiprice= browser.find_elements_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div/div[1]/div/div[2]/div[1]/div[2]")
                tsepetiprice=tsepetiprice[0].text
                tsepetig= browser.find_element_by_xpath("//*[@id='divGidisUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
                tsepetic= browser.find_element_by_xpath("//*[@id='divDonusUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
                tsepeticoncept= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/p").text
                tsepetiroom= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/ul/li[1]/a").text
                fiyat, kusurat = map(str, tsepetiprice.split(','))
                tsepetiprice1, tsepetiprice2 = map(str, fiyat.split('.'))
                tsepetiprice=int(tsepetiprice1+tsepetiprice2)
                tatilsepetiplanestime=tsepetig+' / '+tsepetic
                tsepetiformulacol=rowplus+1
                tsepetiformula='B'+str(tsepetiformulacol)+'-K'+str(tsepetiformulacol)
            except:
                ws.write(rowplus, 10, "", style1)
                ws.write(rowplus, 11, "", style1)
                ws.write(rowplus, 12, "", style1)
                ws.write(rowplus, 13, "", style1)
                ws.write(rowplus, 14, "", style1)
            else:
                ws.write(rowplus, 10, int(tsepetiprice), style1)
                ws.write(rowplus, 11, xlwt.Formula(tsepetiformula), style1)
                ws.write(rowplus, 12, tsepeticoncept, style1)
                ws.write(rowplus, 13, tsepetiroom, style1)
                ws.write(rowplus, 14, tatilsepetiplanestime, style1)
        else:
            ws.write(rowplus, 10, int(tsepetiprice), style1)
            ws.write(rowplus, 11, xlwt.Formula(tsepetiformula), style1)
            ws.write(rowplus, 12, tsepeticoncept, style1)
            ws.write(rowplus, 13, tsepetiroom, style1)
            ws.write(rowplus, 14, tatilsepetiplanestime, style1) 
    brower.close()

def touristica():
    time.sleep(7)
    browser=webdriver.Firefox()
    try:
        browser.get("https://www.touristica.com.tr/acapulco-resort-convention-spa")
        browser.execute_script("document.getElementById('txtCheckInDate').readOnly = false;")
        browser.find_element_by_id("txtCheckInDate").send_keys(touristicacheckin)
        browser.execute_script("document.getElementById('txtCheckOutDate').readOnly = false;")
        browser.find_element_by_id("txtCheckOutDate").send_keys(touristicacheckout)  
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id='formMain']/div[2]/div[3]/div/div/div/button").click() 
        time.sleep(13)
        rowplus=1
    except:
        try:
            browser.get("https://www.touristica.com.tr/acapulco-resort-convention-spa")
            browser.execute_script("document.getElementById('txtCheckInDate').readOnly = false;")
            browser.find_element_by_id("txtCheckInDate").send_keys(touristicacheckin)
            browser.execute_script("document.getElementById('txtCheckOutDate').readOnly = false;")
            browser.find_element_by_id("txtCheckOutDate").send_keys(touristicacheckout)  
            time.sleep(3)
            browser.find_element_by_xpath("//*[@id='formMain']/div[2]/div[3]/div/div/div/button").click() 
            time.sleep(13)
            rowplus=1
        except:
            try:
                browser.get("https://www.touristica.com.tr/acapulco-resort-convention-spa")
                browser.execute_script("document.getElementById('txtCheckInDate').readOnly = false;")
                browser.find_element_by_id("txtCheckInDate").send_keys(touristicacheckin)
                browser.execute_script("document.getElementById('txtCheckOutDate').readOnly = false;")
                browser.find_element_by_id("txtCheckOutDate").send_keys(touristicacheckout)  
                time.sleep(3)
                browser.find_element_by_xpath("//*[@id='formMain']/div[2]/div[3]/div/div/div/button").click() 
                time.sleep(13)
                rowplus=1
            except:       
                print("Hata")   
    for hotel in hotelList:
        rowplus=rowplus+1
        url=hotel[4]
        browser.get(url)
        time.sleep(5)
        try:
            browser.execute_script("window.scrollTo(0, 800);")
            time.sleep(2)
            browser.find_element_by_xpath("//*[@id='HotelRoomListPlaceHolder']/div/ul/li[2]/a").click()
        except:
            try:
                browser.execute_script("window.scrollTo(0, 800);")
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='formMain']/div[2]/section/div[5]/div/ul/li[2]/a").click()
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='HotelRoomListPlaceHolder']/div/ul/li[2]/a").click()
            except:
                try:
                    browser.get(url)
                    time.sleep(5)
                    browser.execute_script("window.scrollTo(0, 800);")
                    time.sleep(2)
                    browser.find_element_by_xpath("//*[@id='HotelRoomListPlaceHolder']/div/ul/li[2]/a").click()
                except:
                    try:
                        browser.execute_script("window.scrollTo(0, 800);")
                        time.sleep(2)
                        browser.find_element_by_xpath("//*[@id='formMain']/div[2]/section/div[5]/div/ul/li[2]/a").click()
                        time.sleep(2)
                        browser.find_element_by_xpath("//*[@id='HotelRoomListPlaceHolder']/div/ul/li[2]/a").click()
                    except:
                        print("Tab Click Error")
        time.sleep(15)
        try:
            touristicaprice= browser.find_elements_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[2]/div[1]/div[3]/div[1]/div[2]/span")
            touristicaprice=touristicaprice[0].text
            touristicag= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/strong[1]").text
            touristicac= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/strong[1]").text
            touristicaconcept= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h5").text
            touristicaroom= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h4").text
            fiyat, kusurat = map(str, touristicaprice.split(','))
            touristicaprice1, touristicaprice2 = map(str, fiyat.split('.'))
            touristicaprice=int(touristicaprice1+touristicaprice2)
            touristicaplanestime=touristicag+' / '+touristicac
            touristicaformulacol=rowplus+1
            touristicaformula='B'+str(touristicaformulacol)+'-P'+str(touristicaformulacol)
        except:
            try:
                time.sleep(6)
                touristicaprice= browser.find_elements_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[2]/div[1]/div[3]/div[1]/div[2]/span")
                touristicaprice=touristicaprice[0].text
                touristicag= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/strong[1]").text
                touristicac= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/strong[1]").text
                touristicaconcept= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h5").text
                touristicaroom= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h4").text
                fiyat, kusurat = map(str, touristicaprice.split(','))
                touristicaprice1, touristicaprice2 = map(str, fiyat.split('.'))
                touristicaprice=int(touristicaprice1+touristicaprice2)
                touristicaplanestime=touristicag+' / '+touristicac
                touristicaformulacol=rowplus+1
                touristicaformula='B'+str(touristicaformulacol)+'-P'+str(touristicaformulacol)
            except:
                ws.write(rowplus, 15, "", style2)
                ws.write(rowplus, 16, "", style2)
                ws.write(rowplus, 17, "", style2)
                ws.write(rowplus, 18, "", style2)
                ws.write(rowplus, 19, "", style2)
            else:
                ws.write(rowplus, 15, int(touristicaprice), style2)
                ws.write(rowplus, 16, xlwt.Formula(touristicaformula), style2)
                ws.write(rowplus, 17, touristicaconcept, style2)
                ws.write(rowplus, 18, touristicaroom, style2)
                ws.write(rowplus, 19, touristicaplanestime, style2)
        else:
            ws.write(rowplus, 15, int(touristicaprice), style2)
            ws.write(rowplus, 16, xlwt.Formula(touristicaformula), style2)
            ws.write(rowplus, 17, touristicaconcept, style2)
            ws.write(rowplus, 18, touristicaroom, style2)
            ws.write(rowplus, 19, touristicaplanestime, style2) 
    brower.close()

def tbudur():
    browser=webdriver.Firefox()
    rowplus=1
    for hotel in hotelList:
        rowplus=rowplus+1
        url=hotel[5]
        try:
            browser.get(url)
            time.sleep(2) 
            browser.execute_script("document.getElementsByName('checkInDate')[0].removeAttribute('readonly');")
            browser.execute_script("document.getElementsByName('checkOutDate')[0].removeAttribute('readonly');")
            browser.find_element_by_name("checkInDate").clear()
            browser.find_element_by_name("checkInDate").send_keys(touristicacheckin)
            browser.find_element_by_name("checkOutDate").clear() 
            browser.find_element_by_name("checkOutDate").send_keys(touristicacheckout) 
            time.sleep(3) 
            browser.find_element_by_xpath("//*[@id='allHotelTabForm']/div/div/div/div[3]/button").click()
            time.sleep(5)
            browser.find_element_by_xpath("//*[@id='room-list']/div[1]/div[1]/div[3]/div/div/div/div/div[4]/div/a").click()
            time.sleep(8)
            browser.find_elements_by_css_selector("#departure3 > div > label")[0].click()
            time.sleep(2)
            browser.find_elements_by_css_selector("#return3 > div > label")[0].click()
            time.sleep(2)
            browser.find_element_by_name("flightDefaultFromValue").send_keys("saw")
            time.sleep(2)
            browser.find_element_by_xpath("//*[@id='ui-id-1']/li[1]/a[1]").click()
            time.sleep(2)
            browser.find_element_by_name("flightDefaultToValue").send_keys("saw")
            time.sleep(3)
            browser.find_element_by_xpath("//*[@id='ui-id-2']/li[1]/a[1]").click()
            time.sleep(1)
            browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-md-24.text-center > button.btn.btn-orange.btn-sharp.btn-block.btn-search.mainSearchButton")[0].click()
            time.sleep(10)
        except:
            try:
                browser.get(url)
                time.sleep(2) 
                browser.execute_script("document.getElementsByName('checkInDate')[0].removeAttribute('readonly');")
                browser.execute_script("document.getElementsByName('checkOutDate')[0].removeAttribute('readonly');")
                browser.find_element_by_name("checkInDate").clear()
                browser.find_element_by_name("checkInDate").send_keys(touristicacheckin)
                browser.find_element_by_name("checkOutDate").clear() 
                browser.find_element_by_name("checkOutDate").send_keys(touristicacheckout) 
                time.sleep(3) 
                browser.find_element_by_xpath("//*[@id='allHotelTabForm']/div/div/div/div[3]/button").click()
                time.sleep(5)
                browser.find_element_by_xpath("//*[@id='room-list']/div[1]/div[1]/div[3]/div/div/div/div/div[4]/div/a").click()
                time.sleep(8)
                browser.find_elements_by_css_selector("#departure3 > div > label")[0].click()
                time.sleep(2)
                browser.find_elements_by_css_selector("#return3 > div > label")[0].click()
                time.sleep(2)
                browser.find_element_by_name("flightDefaultFromValue").send_keys("saw")
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='ui-id-1']/li[1]/a[1]").click()
                time.sleep(2)
                browser.find_element_by_name("flightDefaultToValue").send_keys("saw")
                time.sleep(3)
                browser.find_element_by_xpath("//*[@id='ui-id-2']/li[1]/a[1]").click()
                time.sleep(1)
                browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-md-24.text-center > button.btn.btn-orange.btn-sharp.btn-block.btn-search.mainSearchButton")[0].click()
                time.sleep(10)
            except:
                ws.write(rowplus, 20, "", style1)
                ws.write(rowplus, 21, "", style1)
                ws.write(rowplus, 22, "", style1)
                ws.write(rowplus, 23, "", style1)
                ws.write(rowplus, 24, "", style1)
            else:
                try:
                    tbudurg=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.departure.resultArea > div.option-box.departureFlights.dn.departure > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                    tbudurg, tbudurg2 = map(str, tbudurg.split('S'))
                    tbudurc=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.return.resultArea > div.option-box.returnFlights.dn.return > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                    tbudurc, tbudurc2 = map(str, tbudurc.split('E'))
                    tbudurplanestime=tbudurg+' / '+tbudurc
                    tbudurprice= browser.find_elements_by_xpath("//*[@id='reservation-summary']/div[3]/div[2]/span")[0].text
                    tbudurconcept= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[4]/div[2]").text
                    tbudurroom= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[3]/div[2]").text
                    fiyat, kusurat = map(str, tbudurprice.split(','))
                    tbudurprice1, tbudurprice2 = map(str, fiyat.split('.'))
                    tbudurprice=int(tbudurprice1+tbudurprice2)
                    tbudurformulacol=rowplus+1
                    tbudurformula='B'+str(tbudurformulacol)+'-U'+str(tbudurformulacol)
                except:
                    ws.write(rowplus, 20, "", style1)
                    ws.write(rowplus, 21, "", style1)
                    ws.write(rowplus, 22, "", style1)
                    ws.write(rowplus, 23, "", style1)
                    ws.write(rowplus, 24, "", style1)
                else:
                    ws.write(rowplus, 20, int(tbudurprice), style1)
                    ws.write(rowplus, 21, xlwt.Formula(tbudurformula), style1)
                    ws.write(rowplus, 22, tbudurconcept, style1)
                    ws.write(rowplus, 23, tbudurroom, style1)
                    ws.write(rowplus, 24, tbudurplanestime, style1)     
        else:
            try:
                tbudurg=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.departure.resultArea > div.option-box.departureFlights.dn.departure > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                tbudurg, tbudurg2 = map(str, tbudurg.split('S'))
                tbudurc=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.return.resultArea > div.option-box.returnFlights.dn.return > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                tbudurc, tbudurc2 = map(str, tbudurc.split('E'))
                tbudurplanestime=tbudurg+' / '+tbudurc
                tbudurprice= browser.find_elements_by_xpath("//*[@id='reservation-summary']/div[3]/div[2]/span")[0].text
                tbudurconcept= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[4]/div[2]").text
                tbudurroom= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[3]/div[2]").text
                fiyat, kusurat = map(str, tbudurprice.split(','))
                tbudurprice1, tbudurprice2 = map(str, fiyat.split('.'))
                tbudurprice=int(tbudurprice1+tbudurprice2)
                tbudurformulacol=rowplus+1
                tbudurformula='B'+str(tbudurformulacol)+'-U'+str(tbudurformulacol)
            except:
                ws.write(rowplus, 20, "", style1)
                ws.write(rowplus, 21, "", style1)
                ws.write(rowplus, 22, "", style1)
                ws.write(rowplus, 23, "", style1)
                ws.write(rowplus, 24, "", style1)
            else:
                ws.write(rowplus, 20, int(tbudurprice), style1)
                ws.write(rowplus, 21, xlwt.Formula(tbudurformula), style1)
                ws.write(rowplus, 22, tbudurconcept, style1)
                ws.write(rowplus, 23, tbudurroom, style1)
                ws.write(rowplus, 24, tbudurplanestime, style1)
    brower.close()

def mngturizm():
    browser=webdriver.Firefox()
    rowplus=1
    for hotel in hotelList:
        rowplus=rowplus+1
        url=hotel[6]+mngturizmurlek
        try:
            browser.get(url)
            browser.execute_script("window.scrollTo(0, 800);")
            time.sleep(1)
            browser.execute_script("document.getElementById('body_packageTab').click();")
            time.sleep(8)
            browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").clear()
            browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").send_keys("saw")
            time.sleep(2)
            browser.find_element_by_xpath("//*[@id='ui-id-1']/li[2]/a[1]").click()
            time.sleep(2)
            browser.find_elements_by_css_selector("#body_packageContent > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > button:nth-child(1)")[0].click()
        except:
            try:
                browser.get(url)
                browser.execute_script("window.scrollTo(0, 800);")
                time.sleep(1)
                browser.execute_script("document.getElementById('body_packageTab').click();")
                time.sleep(8)
                browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").clear()
                browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").send_keys("saw")
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='ui-id-1']/li[2]/a[1]").click()
                time.sleep(2)
                browser.find_elements_by_css_selector("#body_packageContent > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > button:nth-child(1)")[0].click()
            except:
                try:
                    browser.get(url)
                    browser.execute_script("window.scrollTo(0, 800);")
                    time.sleep(1)
                    browser.execute_script("document.getElementById('body_packageTab').click();")
                    time.sleep(8)
                    browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").clear()
                    browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").send_keys("saw")
                    time.sleep(2)
                    browser.find_element_by_xpath("//*[@id='ui-id-1']/li[2]/a[1]").click()
                    time.sleep(2)
                    browser.find_elements_by_css_selector("#body_packageContent > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > button:nth-child(1)")[0].click()
                except:
                    print("Saw Error")
        try:
            time.sleep(20)
            mngturizmg=browser.find_elements_by_css_selector("#DepartureFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span")[0].text
            mngturizmg, mngturizmg2 = map(str, mngturizmg.split(' '))
            mngturizmc=browser.find_elements_by_css_selector("#ArrivalFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span:nth-child(1)")[0].text
            mngturizmc, mngturizmc2 = map(str, mngturizmc.split(' '))
            mngturizmplanestime=mngturizmg+' / '+mngturizmc
            mngturizmprice= browser.find_elements_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[2]/span")[0].text
            mngturizmconcept= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[1]").text
            mngturizmroom= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[2]/div[1]").text
            fiyat, kusurat = map(str, mngturizmprice.split(','))
            mngturizmprice1, mngturizmprice2 = map(str, fiyat.split('.'))
            mngturizmprice=int(mngturizmprice1+mngturizmprice2)
            mngturizmprice= mngturizmprice+160
            mngturizmformulacol=rowplus+1
            mngturizmformula='B'+str(mngturizmformulacol)+'-Z'+str(mngturizmformulacol)
        except:
            try:
                time.sleep(2)
                mngturizmg=browser.find_elements_by_css_selector("#DepartureFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span")[0].text
                mngturizmg, mngturizmg2 = map(str, mngturizmg.split(' '))
                mngturizmc=browser.find_elements_by_css_selector("#ArrivalFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span:nth-child(1)")[0].text
                mngturizmc, mngturizmc2 = map(str, mngturizmc.split(' '))
                mngturizmplanestime=mngturizmg+' / '+mngturizmc
                mngturizmprice= browser.find_elements_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[2]/span")[0].text
                mngturizmconcept= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[1]").text
                mngturizmroom= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[2]/div[1]").text
                fiyat, kusurat = map(str, mngturizmprice.split(','))
                mngturizmprice1, mngturizmprice2 = map(str, fiyat.split('.'))
                mngturizmprice=int(mngturizmprice1+mngturizmprice2)
                mngturizmprice= mngturizmprice+160
                mngturizmformulacol=rowplus+1
                mngturizmformula='B'+str(mngturizmformulacol)+'-Z'+str(mngturizmformulacol)
            except:
                ws.write(rowplus, 25, "", style2)
                ws.write(rowplus, 26, "", style2)
                ws.write(rowplus, 27, "", style2)
                ws.write(rowplus, 28, "", style2)
                ws.write(rowplus, 29, "", style2)
            else: 
                ws.write(rowplus, 25, int(mngturizmprice), style2)
                ws.write(rowplus, 26, xlwt.Formula(mngturizmformula), style2)
                ws.write(rowplus, 27, mngturizmconcept, style2)
                ws.write(rowplus, 28, mngturizmroom, style2)
                ws.write(rowplus, 29, mngturizmplanestime, style2)
        else: 
            ws.write(rowplus, 25, int(mngturizmprice), style2)
            ws.write(rowplus, 26, xlwt.Formula(mngturizmformula), style2)
            ws.write(rowplus, 27, mngturizmconcept, style2)
            ws.write(rowplus, 28, mngturizmroom, style2)
            ws.write(rowplus, 29, mngturizmplanestime, style2)
    brower.close()

t1 = threading.Thread(target=tatildukkani)
t2 = threading.Thread(target=tatilcom)
t3 = threading.Thread(target=tsepeti)
t4 = threading.Thread(target=touristica)
t5 = threading.Thread(target=tbudur)
t6 = threading.Thread(target=mngturizm)

t2.start()
t4.start()
t5.start()
t6.start()

t2.join()
t4.join()
t5.join()
t6.join()

t1.start()
t3.start()
t1.join()
t3.join()

datenow=date.today()
wb.save('./Raporlar/Rapor-'+str(datenow)+'.xls')
time.sleep(1)
finish = time.perf_counter()
print('Bitiş saniyesi:', round(finish-start, 2))



