def tatildukkani(compoter="",tdID=0):
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
            i =0;

            while(True):
                i += 1;
                if(i>2): break;
                try:
                    browser.get(url)
                    time.sleep(0)
                    tdprice = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='pck_price0']"))).text
                    print("LOG > Otel Fiyatı "+str(tdprice))
                    tdg = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='d_dtime']"))).text
                    tdc = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='r_dtime']"))).text
                    tdDesc = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#reservation_result > div.row > div.col-md-6.col-sm-12.col-xs-12 > ul > li > div.row > div.col-md-5.col-sm-5.col-xs-6.text-center.p0"))).text
                    tdDesc=tdDesc.splitlines()
                    tdroom=tdDesc[0]
                    tdconcept=tdDesc[1]
                    tdprice, remainder = map(str, tdprice.split('.'))
                    tdprice1, tdprice2 = map(str, tdprice.split(','))
                    tdPriceAmount=int(tdprice1+tdprice2)
                    tdplanestime=tdg+'/'+tdc
                    tdprice = { "PriceProductID": tdHotelID, "PriceCompetitorID": str(tdId), "PriceTitle":tdroom, "PriceDesc":tdconcept, "PriceAmount":tdPriceAmount, "PriceCur":"TRY", "IsDelete":isDelete, "PriceSet":{"PriceSetFlightTime":tdplanestime, "PriceSetType":priceSetType, "PriceSetDate":str(priceDate), "PriceSetStartDate":str(checkin), "PriceSetFinishDate":str(checkout), "PriceSetQuery":""}}
                    pricecol.insert_one(tdprice)
                    break;
                except TimeoutException  as e:
                    print("Fiyat Bulunmadı! "+url+" "+str(e))
        browser.quit()