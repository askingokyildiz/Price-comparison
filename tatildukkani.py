from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import threading
from datetime import datetime, date
import time
import pymongo
from bson.objectid import ObjectId
import json

options = Options()#Seçenek nesnesi oluşturduk
options.headless = True #Seçenek nesnesi içerisindeki headless modunu aktif hale getirdik

#İşlem Süresini Başlatma
start = time.perf_counter()
print("Paket Fiyat Oluşturma")
date_entry = input('Giriş Tarihi (ör: 07-07-2020): ')
date_release = input('Çıkış Tarihi (ör: 12-07-2020): ')
competitorVerification=input('Veriler Kaydedilsin mi? (y veya n): ')
if competitorVerification != 'y':
    print("Kayıt Başarısız!")
    exit()
try:
    day_entry, month_entry, year_entry = map(int, date_entry.split('-'))
    day_release, month_release, year_release = map(int, date_release.split('-'))
except:
    print("Tarih İstenilen Formatta girilmedi!")
    exit()
checkin= date(year_entry, month_entry, day_entry)
checkout= date(year_release, month_release, day_release)
priceDate=date.today()
priceSetType="Otel + Uçak + Transfer"

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["price_comparison"]
competitorcol = db["competitor"]
hotelurlcol = db["hotelurl"]
pricecol = db["price"]

def tatildukkani():
    try:
        tdcompetitor={ "CompetitorURL": "tatildukkani.com" }
        tdcompetitorcol = competitorcol.find_one(tdcompetitor)
        tdId=tdcompetitorcol["_id"]
    except:
        print("Id Bulunamadı.")
    try:
        tdcompetitorHotelUrl = hotelurlcol.find({ "HotelUrlCompetitorID": str(tdId) })
    except:
        print("Hotel Url Bulunamadı.")
    else:
        browser = webdriver.Firefox(options=options) #Tarayıcı nesnesi oluştururken, oluşturduğumuz seçenek nesnesini tanımladık
        for tdHotelsUrl in tdcompetitorHotelUrl:
            tdHotelUrl=tdHotelsUrl["HotelUrl"]
            tdHotelID=tdHotelsUrl["HotelUrlHotelID"]
            isDelete=0
            tdCheckin= str(day_entry)+'.'+str(month_entry)+'.'+ str(year_entry)
            tdCheckout= str(day_release)+'.'+str(month_release)+'.'+ str(year_release)
            tdUrlPiece='?checkin='+tdCheckin+'&checkout='+tdCheckout+'&adult=2&child=0&child1_age=1&child2_age=1&airport=SAW'
            url=tdHotelUrl+tdUrlPiece
            try:
                browser.get(url)
                time.sleep(8)
                tdprice= browser.find_element_by_xpath("//*[@id='pck_price0']").text
                tdg= browser.find_element_by_xpath("//*[@id='d_dtime']").text
                tdc= browser.find_element_by_xpath("//*[@id='r_dtime']").text
                tdDesc= browser.find_elements_by_css_selector("#reservation_result > div.row > div.col-md-6.col-sm-12.col-xs-12 > ul > li > div.row > div.col-md-5.col-sm-5.col-xs-6.text-center.p0")[0].text
                tdDesc=tdDesc.splitlines()
                tdroom=tdDesc[0]
                tdconcept=tdDesc[1]
                tdprice, remainder = map(str, tdprice.split('.'))
                tdprice1, tdprice2 = map(str, tdprice.split(','))
                tdPriceAmount=int(tdprice1+tdprice2)
                tdplanestime=tdg+'/'+tdc
            except:
                try:
                    browser.get(url)
                    time.sleep(8)
                    tdprice= browser.find_element_by_xpath("//*[@id='pck_price0']").text
                    tdg= browser.find_element_by_xpath("//*[@id='d_dtime']").text
                    tdc= browser.find_element_by_xpath("//*[@id='r_dtime']").text
                    tdDesc= browser.find_elements_by_css_selector("#reservation_result > div.row > div.col-md-6.col-sm-12.col-xs-12 > ul > li > div.row > div.col-md-5.col-sm-5.col-xs-6.text-center.p0")[0].text
                    tdDesc=tdDesc.splitlines()
                    tdroom=tdDesc[0]
                    tdconcept=tdDesc[1]
                    tdprice, remainder = map(str, tdprice.split('.'))
                    tdprice1, tdprice2 = map(str, tdprice.split(','))
                    tdPriceAmount=int(tdprice1+tdprice2)
                    tdplanestime=tdg+'/'+tdc
                except:
                    print("Fiyat Bulunmadı! "+url)
                else:
                    tdprice = { "PriceProductID": tdHotelID, "PriceCompetitorID": str(tdId), "PriceFlightTime":tdplanestime, "PriceTitle":tdroom, "PriceDesc":tdconcept, "PriceAmount":tdPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":"" } }
                    pricecol.insert_one(tdprice)
            else:
                tdprice = { "PriceProductID": tdHotelID, "PriceCompetitorID": str(tdId), "PriceFlightTime":tdplanestime, "PriceTitle":tdroom, "PriceDesc":tdconcept, "PriceAmount":tdPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                pricecol.insert_one(tdprice)
        browser.quit()
        
def tsepeti():
    try:
        tsepeticompetitor={ "CompetitorURL": "tatilsepeti.com" }
        tsepeticompetitorcol = competitorcol.find_one(tsepeticompetitor)
        tsepetiId=tsepeticompetitorcol["_id"]
    except:
        print("Id Bulunamadı.")
    try:
        tsepeticompetitorHotelUrl = hotelurlcol.find({ "HotelUrlCompetitorID": str(tsepetiId) })
    except:
        print("Hotel Url Bulunamadı.")
    else:
        browser = webdriver.Firefox(options=options) #Tarayıcı nesnesi oluştururken, oluşturduğumuz seçenek nesnesini tanımladık
        for tsepetiHotelsUrl in tsepeticompetitorHotelUrl:
            tsepetiHotelUrl=tsepetiHotelsUrl["HotelUrl"]
            tsepetiHotelID=tsepetiHotelsUrl["HotelUrlHotelID"]
            isDelete=0
            tsepetiCheckin= str(day_entry)+'.'+str(month_entry)+'.'+ str(year_entry)
            tsepetiCheckout= str(day_release)+'.'+str(month_release)+'.'+ str(year_release)
            tsepetiUrlPiece='?ara=oda:2;tarih:'+tsepetiCheckin+','+tsepetiCheckout+'&up=tab:1;from:saw'
            url=tsepetiHotelUrl+tsepetiUrlPiece
            try:
                browser.get(url)
                time.sleep(1)
                browser.execute_script("window.scrollTo(0, 800);")
                time.sleep(14)
                tsepetiprice= browser.find_elements_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div/div[1]/div/div[2]/div[1]/div[2]")
                tsepetiprice=tsepetiprice[0].text
                tsepetig= browser.find_element_by_xpath("//*[@id='divGidisUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
                tsepetic= browser.find_element_by_xpath("//*[@id='divDonusUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
                tsepeticoncept= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/p").text
                tsepetiroom= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/ul/li[1]/a").text
                fiyat, kusurat = map(str, tsepetiprice.split(','))
                tsepetiprice1, tsepetiprice2 = map(str, fiyat.split('.'))
                tsepetiPriceAmount=int(tsepetiprice1+tsepetiprice2)
                tatilsepetiplanestime=tsepetig+'/'+tsepetic
            except:
                try:
                    browser.get(url)
                    time.sleep(1)
                    browser.execute_script("window.scrollTo(0, 800);")
                    time.sleep(14)
                    tsepetiprice= browser.find_elements_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div/div[1]/div/div[2]/div[1]/div[2]")
                    tsepetiprice=tsepetiprice[0].text
                    tsepetig= browser.find_element_by_xpath("//*[@id='divGidisUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
                    tsepetic= browser.find_element_by_xpath("//*[@id='divDonusUcusListesi']/div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/span[1]").text
                    tsepeticoncept= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/p").text
                    tsepetiroom= browser.find_element_by_xpath("//*[@id='dev-roomList-flight']/div[1]/ul/li[1]/a").text
                    fiyat, kusurat = map(str, tsepetiprice.split(','))
                    tsepetiprice1, tsepetiprice2 = map(str, fiyat.split('.'))
                    tsepetiPriceAmount=int(tsepetiprice1+tsepetiprice2)
                    tatilsepetiplanestime=tsepetig+'/'+tsepetic
                except:
                    print("Fiyat Bulunmadı! "+url)
                else:
                    tsepetiprice = { "PriceProductID": tsepetiHotelID, "PriceFlightTime":tatilsepetiplanestime, "PriceCompetitorID": str(tsepetiId), "PriceTitle":tsepetiroom, "PriceDesc":tsepeticoncept, "PriceAmount":tsepetiPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                    pricecol.insert_one(tsepetiprice)
            else:
                tsepetiprice = { "PriceProductID": tsepetiHotelID, "PriceFlightTime":tatilsepetiplanestime, "PriceCompetitorID": str(tsepetiId), "PriceTitle":tsepetiroom, "PriceDesc":tsepeticoncept, "PriceAmount":tsepetiPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                pricecol.insert_one(tsepetiprice)    
        browser.quit()

def tatilcom():
    try:
        tatilcomcompetitor={ "CompetitorURL": "tatil.com" }
        tatilcomcompetitorcol = competitorcol.find_one(tatilcomcompetitor)
        tatilcomId=tatilcomcompetitorcol["_id"]
    except:
        print("Id Bulunamadı.")
    try:
        tatilcomcompetitorHotelUrl = hotelurlcol.find({ "HotelUrlCompetitorID": str(tatilcomId) })
    except:
        print("Hotel Url Bulunamadı.")
    else:
        browser = webdriver.Firefox(options=options) #Tarayıcı nesnesi oluştururken, oluşturduğumuz seçenek nesnesini tanımladık
        for tatilcomHotelsUrl in tatilcomcompetitorHotelUrl:
            tatilcomHotelUrl=tatilcomHotelsUrl["HotelUrl"]
            tatilcomHotelID=tatilcomHotelsUrl["HotelUrlHotelID"]
            isDelete=0
            tatilcomCheckin= date(year_entry, month_entry, day_entry)
            tatilcomCheckout= date(year_release, month_release, day_release)
            tatilcomUrlPiece='?pax=2&checkin=' + str(tatilcomCheckin) + '&checkout=' + str(tatilcomCheckout)
            url=tatilcomHotelUrl+tatilcomUrlPiece
            try:
                browser.get(url)
                time.sleep(7)
                browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_rblReservationType']/label[2]").click()
                time.sleep(10)
                tatilcomPriceAmount= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[4]/span/strong").text
                tatilcomg= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblDepartureFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                tatilcomc= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblReturnFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                tatilcomconcept= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h6").text
                tatilcomroom= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h5").text
                tatilcomplanestime=tatilcomg+'/'+tatilcomc
            except:
                try:
                    browser.get(url)
                    time.sleep(7)
                    browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_rblReservationType']/label[2]").click()
                    time.sleep(10)
                    tatilcomPriceAmount= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[4]/span/strong").text
                    tatilcomg= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblDepartureFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                    tatilcomc= browser.find_element_by_xpath("//*[@id='bodyContent_bodyContent_HotelRoomList_HotelRoomListPackage_rptFlightTicketList_lblReturnFlightItem_0']/div/div/div[1]/div/div[1]/div[1]").text
                    tatilcomconcept= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h6").text
                    tatilcomroom= browser.find_element_by_xpath("//*[@id='hotel-room-list']/div[3]/div/main/div[1]/div[1]/div/div[1]/h5").text
                    tatilcomplanestime=tatilcomg+'/'+tatilcomc
                except:
                    print("Fiyat Bulunmadı! "+url)
                else:
                    tatilcomprice = { "PriceProductID": tatilcomHotelID, "PriceFlightTime":tatilcomplanestime, "PriceCompetitorID": str(tatilcomId), "PriceTitle":tatilcomroom, "PriceDesc":tatilcomconcept, "PriceAmount":tatilcomPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                    pricecol.insert_one(tatilcomprice)
            else:
                tatilcomprice = { "PriceProductID": tatilcomHotelID, "PriceFlightTime":tatilcomplanestime, "PriceCompetitorID": str(tatilcomId), "PriceTitle":tatilcomroom, "PriceDesc":tatilcomconcept, "PriceAmount":tatilcomPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                pricecol.insert_one(tatilcomprice)
        browser.quit()

def touristica():
    try:
        touristicacompetitor={ "CompetitorURL": "touristica.com.tr" }
        touristicacompetitorcol = competitorcol.find_one(touristicacompetitor)
        touristicaId=touristicacompetitorcol["_id"]
    except:
        print("Id Bulunamadı.")
    try:
        touristicacompetitorHotelUrl = hotelurlcol.find({ "HotelUrlCompetitorID": str(touristicaId) })
    except:
        print("Hotel Url Bulunamadı.")
    else:
        browser = webdriver.Firefox(options=options) #Tarayıcı nesnesi oluştururken, oluşturduğumuz seçenek nesnesini tanımladık
        touristicaday, touristicamonth, touristicayear= map(str, date_entry.split('-'))
        touristicacheckin=touristicaday+"."+touristicamonth+"."+touristicayear
        touristicaday, touristicamonth, touristicayear= map(str, date_release.split('-'))
        touristicacheckout=touristicaday+"."+touristicamonth+"."+touristicayear
        try:
            browser.get("https://www.touristica.com.tr/acapulco-resort-convention-spa")
            browser.execute_script("document.getElementById('txtCheckInDate').readOnly = false;")
            browser.find_element_by_id("txtCheckInDate").send_keys(touristicacheckin)
            browser.execute_script("document.getElementById('txtCheckOutDate').readOnly = false;")
            browser.find_element_by_id("txtCheckOutDate").send_keys(touristicacheckout)  
            time.sleep(3)
            browser.find_element_by_xpath("//*[@id='formMain']/div[2]/div[3]/div/div/div/button").click() 
            time.sleep(15)
        except:
            try:
                browser.get("https://www.touristica.com.tr/acapulco-resort-convention-spa")
                browser.execute_script("document.getElementById('txtCheckInDate').readOnly = false;")
                browser.find_element_by_id("txtCheckInDate").send_keys(touristicacheckin)
                browser.execute_script("document.getElementById('txtCheckOutDate').readOnly = false;")
                browser.find_element_by_id("txtCheckOutDate").send_keys(touristicacheckout)  
                time.sleep(3)
                browser.find_element_by_xpath("//*[@id='formMain']/div[2]/div[3]/div/div/div/button").click() 
                time.sleep(15)
            except:
                try:
                    browser.get("https://www.touristica.com.tr/acapulco-resort-convention-spa")
                    browser.execute_script("document.getElementById('txtCheckInDate').readOnly = false;")
                    browser.find_element_by_id("txtCheckInDate").send_keys(touristicacheckin)
                    browser.execute_script("document.getElementById('txtCheckOutDate').readOnly = false;")
                    browser.find_element_by_id("txtCheckOutDate").send_keys(touristicacheckout)  
                    time.sleep(3)
                    browser.find_element_by_xpath("//*[@id='formMain']/div[2]/div[3]/div/div/div/button").click() 
                    time.sleep(15)
                except:       
                    print("Hata")
                    exit()
        for touristicaHotelsUrl in touristicacompetitorHotelUrl:
            touristicaHotelUrl=touristicaHotelsUrl["HotelUrl"]
            touristicaHotelID=touristicaHotelsUrl["HotelUrlHotelID"]
            isDelete=0
            url=touristicaHotelUrl
            try:
                browser.get(url)
                time.sleep(5)
                browser.execute_script("window.scrollTo(0, 800);")
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='formMain']/div[2]/section/div[5]/div/ul/li[2]/a").click()
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='HotelRoomListPlaceHolder']/div/ul/li[2]/a").click()
                time.sleep(20)
                touristicaprice= browser.find_elements_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[2]/div[1]/div[3]/div[1]/div[2]/span")
                touristicaprice=touristicaprice[0].text
                touristicag= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/strong[1]").text
                touristicac= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/strong[1]").text
                touristicaconcept= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h5").text
                touristicaroom= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h4").text
                fiyat, kusurat = map(str, touristicaprice.split(','))
                touristicaprice1, touristicaprice2 = map(str, fiyat.split('.'))
                touristicaPriceAmount=int(touristicaprice1+touristicaprice2)
                touristicaplanestime=touristicag+'/'+touristicac
            except:
                try:
                    browser.get(url)
                    time.sleep(5)
                    browser.execute_script("window.scrollTo(0, 800);")
                    time.sleep(2)
                    browser.find_element_by_xpath("//*[@id='formMain']/div[2]/section/div[5]/div/ul/li[2]/a").click()
                    time.sleep(2)
                    browser.find_element_by_xpath("//*[@id='HotelRoomListPlaceHolder']/div/ul/li[2]/a").click()
                    time.sleep(20)
                    touristicaprice= browser.find_elements_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[2]/div[1]/div[3]/div[1]/div[2]/span")
                    touristicaprice=touristicaprice[0].text
                    touristicag= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/strong[1]").text
                    touristicac= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/strong[1]").text
                    touristicaconcept= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h5").text
                    touristicaroom= browser.find_element_by_xpath("//*[@id='HotelRoomListPackagePlaceHolder']/div[3]/div[1]/div/div[1]/h4").text
                    fiyat, kusurat = map(str, touristicaprice.split(','))
                    touristicaprice1, touristicaprice2 = map(str, fiyat.split('.'))
                    touristicaPriceAmount=int(touristicaprice1+touristicaprice2)
                    touristicaplanestime=touristicag+'/'+touristicac
                except:
                    print("Fiyat Bulunmadı! "+url)
                else:
                    touristicaprice = { "PriceProductID": touristicaHotelID, "PriceFlightTime":touristicaplanestime, "PriceCompetitorID": str(touristicaId), "PriceTitle":touristicaroom, "PriceDesc":touristicaconcept, "PriceAmount":touristicaPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                    pricecol.insert_one(touristicaprice)
            else:
                touristicaprice = { "PriceProductID": touristicaHotelID, "PriceFlightTime":touristicaplanestime, "PriceCompetitorID": str(touristicaId), "PriceTitle":touristicaroom, "PriceDesc":touristicaconcept, "PriceAmount":touristicaPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                pricecol.insert_one(touristicaprice)
        browser.quit()

def tbudur():
    try:
        tbudurcompetitor={ "CompetitorURL": "tatilbudur.com" }
        tbudurcompetitorcol = competitorcol.find_one(tbudurcompetitor)
        tbudurId=tbudurcompetitorcol["_id"]
    except:
        print("Id Bulunamadı.")
    try:
        tbudurcompetitorHotelUrl = hotelurlcol.find({ "HotelUrlCompetitorID": str(tbudurId) })
    except:
        print("Hotel Url Bulunamadı.")
    else:
        browser = webdriver.Firefox(options=options) #Tarayıcı nesnesi oluştururken, oluşturduğumuz seçenek nesnesini tanımladık
        for tbudurHotelsUrl in tbudurcompetitorHotelUrl:
            tbudurHotelUrl=tbudurHotelsUrl["HotelUrl"]
            tbudurHotelID=tbudurHotelsUrl["HotelUrlHotelID"]
            isDelete=0
            tbudurday, tbudurmonth, tbuduryear= map(str, date_entry.split('-'))
            tbudurcheckin=tbudurday+"."+tbudurmonth+"."+tbuduryear
            tbudurday, tbudurmonth, tbuduryear= map(str, date_release.split('-'))
            tbudurcheckout=tbudurday+"."+tbudurmonth+"."+tbuduryear
            url=tbudurHotelUrl
            try:
                browser.get(url)
                time.sleep(2) 
                browser.execute_script("document.getElementsByName('checkInDate')[0].removeAttribute('readonly');")
                browser.execute_script("document.getElementsByName('checkOutDate')[0].removeAttribute('readonly');")
                browser.find_element_by_name("checkInDate").clear()
                browser.find_element_by_name("checkInDate").send_keys(tbudurcheckin)
                browser.find_element_by_name("checkOutDate").clear() 
                browser.find_element_by_name("checkOutDate").send_keys(tbudurcheckout) 
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
                tbudurg=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.departure.resultArea > div.option-box.departureFlights.dn.departure > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                tbudurg, tbudurg2 = map(str, tbudurg.split('S'))
                tbudurc=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.return.resultArea > div.option-box.returnFlights.dn.return > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                tbudurc, tbudurc2 = map(str, tbudurc.split('E'))
                tbudurplanestime=tbudurg+'/'+tbudurc
                tbudurprice= browser.find_elements_by_xpath("//*[@id='reservation-summary']/div[3]/div[2]/span")[0].text
                tbudurconcept= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[4]/div[2]").text
                tbudurroom= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[3]/div[2]").text
                fiyat, kusurat = map(str, tbudurprice.split(','))
                tbudurprice1, tbudurprice2 = map(str, fiyat.split('.'))
                tbudurPriceAmount=int(tbudurprice1+tbudurprice2)
            except:
                try:
                    browser.get(url)
                    time.sleep(2) 
                    browser.execute_script("document.getElementsByName('checkInDate')[0].removeAttribute('readonly');")
                    browser.execute_script("document.getElementsByName('checkOutDate')[0].removeAttribute('readonly');")
                    browser.find_element_by_name("checkInDate").clear()
                    browser.find_element_by_name("checkInDate").send_keys(tbudurcheckin)
                    browser.find_element_by_name("checkOutDate").clear() 
                    browser.find_element_by_name("checkOutDate").send_keys(tbudurcheckout) 
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
                    tbudurg=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.departure.resultArea > div.option-box.departureFlights.dn.departure > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                    tbudurg, tbudurg2 = map(str, tbudurg.split('S'))
                    tbudurc=browser.find_elements_by_css_selector("#arrival > section > section.col-md-16.col-xxs-24 > div > div.col-sm-12.col-xxs-24.return.resultArea > div.option-box.returnFlights.dn.return > div.slimScrollDiv > ul > li.no-flight-group.selected > div.row > div:nth-child(2) > span:nth-child(1)")[0].text
                    tbudurc, tbudurc2 = map(str, tbudurc.split('E'))
                    tbudurplanestime=tbudurg+'/'+tbudurc
                    tbudurprice= browser.find_elements_by_xpath("//*[@id='reservation-summary']/div[3]/div[2]/span")[0].text
                    tbudurconcept= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[4]/div[2]").text
                    tbudurroom= browser.find_element_by_xpath("//*[@id='reservation-summary']/ul/li[3]/div[2]").text
                    fiyat, kusurat = map(str, tbudurprice.split(','))
                    tbudurprice1, tbudurprice2 = map(str, fiyat.split('.'))
                    tbudurPriceAmount=int(tbudurprice1+tbudurprice2)
                except:
                    print("Fiyat Bulunmadı! "+url)
                else:
                    tbudurprice = { "PriceProductID": tbudurHotelID, "PriceFlightTime":tbudurplanestime, "PriceCompetitorID": str(tbudurId), "PriceTitle":tbudurroom, "PriceDesc":tbudurconcept, "PriceAmount":tbudurPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                    pricecol.insert_one(tbudurprice) 
            else:
                tbudurprice = { "PriceProductID": tbudurHotelID, "PriceFlightTime":tbudurplanestime, "PriceCompetitorID": str(tbudurId), "PriceTitle":tbudurroom, "PriceDesc":tbudurconcept, "PriceAmount":tbudurPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                pricecol.insert_one(tbudurprice)    
        browser.quit()

def mngturizm():
    try:
        mngturizmcompetitor={ "CompetitorURL": "mngturizm.com" }
        mngturizmcompetitorcol = competitorcol.find_one(mngturizmcompetitor)
        mngturizmId=mngturizmcompetitorcol["_id"]
    except:
        print("Id Bulunamadı.")
    try:
        mngturizmcompetitorHotelUrl = hotelurlcol.find({ "HotelUrlCompetitorID": str(mngturizmId) })
    except:
        print("Hotel Url Bulunamadı.")
    else:
        browser = webdriver.Firefox(options=options) #Tarayıcı nesnesi oluştururken, oluşturduğumuz seçenek nesnesini tanımladık
        for mngturizmHotelsUrl in mngturizmcompetitorHotelUrl:
            mngturizmHotelUrl=mngturizmHotelsUrl["HotelUrl"]
            mngturizmHotelID=mngturizmHotelsUrl["HotelUrlHotelID"]
            isDelete=0
            mngturizmday, mngturizmmonth, mngturizmyear= map(str, date_entry.split('-'))
            mngturizmcheckin=mngturizmday+"/"+mngturizmmonth+"/"+mngturizmyear
            mngturizmday, mngturizmmonth, mngturizmyear= map(str, date_release.split('-'))
            mngturizmcheckout=mngturizmday+"/"+mngturizmmonth+"/"+mngturizmyear
            mngturizmUrlPiece="?CheckIn="+mngturizmcheckin+"&CheckOut="+mngturizmcheckout+"&AC=2&CC=0&CA1=1&CA2=1&CA3=1&CA4=1&CA5=1&CA6=1"
            url=mngturizmHotelUrl+mngturizmUrlPiece
            try:
                browser.get(url)
                browser.execute_script("window.scrollTo(0, 800);")
                time.sleep(1)
                browser.execute_script("document.getElementById('body_packageTab').click();")
                time.sleep(17)
                browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").clear()
                browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").send_keys("saw")
                time.sleep(2)
                browser.find_element_by_xpath("//*[@id='ui-id-1']/li[2]/a[1]").click()
                time.sleep(2)
                browser.find_elements_by_css_selector("#body_packageContent > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > button:nth-child(1)")[0].click()
                time.sleep(35)
                mngturizmg=browser.find_elements_by_css_selector("#DepartureFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span")[0].text
                mngturizmg, mngturizmg2 = map(str, mngturizmg.split(' '))
                mngturizmc=browser.find_elements_by_css_selector("#ArrivalFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span:nth-child(1)")[0].text
                mngturizmc, mngturizmc2 = map(str, mngturizmc.split(' '))
                mngturizmplanestime=mngturizmg+'/'+mngturizmc
                mngturizmprice= browser.find_elements_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[2]/span")[0].text
                mngturizmconcept= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[1]").text
                mngturizmroom= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[2]/div[1]").text
                fiyat, kusurat = map(str, mngturizmprice.split(','))
                mngturizmprice1, mngturizmprice2 = map(str, fiyat.split('.'))
                mngturizmprice=int(mngturizmprice1+mngturizmprice2)
                mngturizmPriceAmount= mngturizmprice+160
            except:
                try:
                    browser.get(url)
                    browser.execute_script("window.scrollTo(0, 800);")
                    time.sleep(1)
                    browser.execute_script("document.getElementById('body_packageTab').click();")
                    time.sleep(17)
                    browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").clear()
                    browser.find_element_by_xpath("//*[@id='hdPackDepLocation']").send_keys("saw")
                    time.sleep(2)
                    browser.find_element_by_xpath("//*[@id='ui-id-1']/li[2]/a[1]").click()
                    time.sleep(2)
                    browser.find_elements_by_css_selector("#body_packageContent > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(6) > button:nth-child(1)")[0].click()
                    time.sleep(35)
                    mngturizmg=browser.find_elements_by_css_selector("#DepartureFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span")[0].text
                    mngturizmg, mngturizmg2 = map(str, mngturizmg.split(' '))
                    mngturizmc=browser.find_elements_by_css_selector("#ArrivalFlightResult > div.hdFlightItem.choosed > div.hdfDetails > span:nth-child(1)")[0].text
                    mngturizmc, mngturizmc2 = map(str, mngturizmc.split(' '))
                    mngturizmplanestime=mngturizmg+'/'+mngturizmc
                    mngturizmprice= browser.find_elements_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[2]/span")[0].text
                    mngturizmconcept= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[3]/div[1]").text
                    mngturizmroom= browser.find_element_by_xpath("//*[@id='packageHotelResult']/div[1]/div[2]/div[1]").text
                    fiyat, kusurat = map(str, mngturizmprice.split(','))
                    mngturizmprice1, mngturizmprice2 = map(str, fiyat.split('.'))
                    mngturizmprice=int(mngturizmprice1+mngturizmprice2)
                    mngturizmPriceAmount= mngturizmprice+160
                except:
                    print("Fiyat Bulunmadı! "+url)
                else:
                    mngturizmprice = { "PriceProductID": mngturizmHotelID, "PriceFlightTime":mngturizmplanestime, "PriceCompetitorID": str(mngturizmId), "PriceTitle":mngturizmroom, "PriceDesc":mngturizmconcept, "PriceAmount":mngturizmPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                    pricecol.insert_one(mngturizmprice)
            else:
                mngturizmprice = { "PriceProductID": mngturizmHotelID, "PriceFlightTime":mngturizmplanestime, "PriceCompetitorID": str(mngturizmId), "PriceTitle":mngturizmroom, "PriceDesc":mngturizmconcept, "PriceAmount":mngturizmPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                pricecol.insert_one(mngturizmprice)    
        browser.quit()

t1 = threading.Thread(target=tatildukkani)
t2 = threading.Thread(target=tatilcom)
t3 = threading.Thread(target=tsepeti)
t4 = threading.Thread(target=touristica)
t5 = threading.Thread(target=tbudur)
t6 = threading.Thread(target=mngturizm)

t4.start()
time.sleep(25)
t1.start()
t2.start()
t3.start()
t5.start()
t6.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()

#İşlem Süresini Bitirip Yazdırma.
finish = time.perf_counter()
print('Bitiş saniyesi:', round(finish-start, 2))

"""
PriceID:""
PriceProductID:""  HotelID  / tdHotelID / tsepetiHotelID
PriceCompetitorID:"" Fiyat Rakip Kimliği / tsepetiId
PriceTitle:"" Oda Türü / 
PriceDesc:"" Konsept / 
PriceAmount:"" Fiyat Tutarı / 
PriceCur:"" Fiyat Cur / TRY
PriceFlightTime:"" Flight Time /
IsDelete:"" 0
PriceSet:
  {
    PriceSetType:"" Paket Fiyat Türü / priceSetType
    PriceSetDate:"" Paket Fiyat Tarihi / priceDate
    PriceSetStartDate:"" Paket Fiyat Başlangıç Tarihi / checkin
    PriceSetFinishDate:"" Paket Fiyat Bitiş Tarihi / checkout
    PriceSetQuery:"" Paket Fiyat Sorgusu / ""
  }



"PriceSet":{"PriceSetType":priceSetType, "PriceSetDate":priceDate, "PriceSetStartDate":checkin, "PriceSetFinishDate":checkout, "PriceSetQuery":"" }
"""