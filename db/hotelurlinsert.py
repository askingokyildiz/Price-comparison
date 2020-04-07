import pymongo

hotelUrlHotelID=input('Hotel ID: ')
hotelUrlCompetitorID=input('Competitor ID: ')
hotelUrl=input('Hotel Url: ')
hotelUrlVerification=input('Veriler Kaydedilsin mi? (y veya n): ')
isDelete=0
if hotelUrlVerification != 'y':
    print("Kayıt Başarısız!")
    exit()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["price_comparison"]
mycol = mydb["hotelurl"]
colhotelurl = { "HotelUrlHotelID": hotelUrlHotelID, "HotelUrlCompetitorID": hotelUrlCompetitorID, "HotelUrl":hotelUrl, "IsDelete":isDelete }
mycol.insert_one(colhotelurl)
print("Kaydedildi.")