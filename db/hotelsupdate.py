import pymongo
from bson.objectid import ObjectId

hotelId=input('Hotel Id: ')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["price_comparison"]
mycol = mydb["hotels"]
try:
    hotelId={ "_id": ObjectId(hotelId) }
    hotelfind = mycol.find_one(hotelId)
except:
    print("Id Bulunamadı.")
else:
    if hotelfind:
        print(hotelfind)
        hotelTitle=input('HotelTitle: ')
        hotelCode=input('Hotel Code: ')
        hotelRegion=input('Hotel Region: ')
        hotelRegionCode=input('Hotel Region Code: ')
        hotelCountry=input('Hotel Country: ')
        isDelete=input('is Delete (Aktif:0 veya Pasif:1): ')
        hotelVerification=input('Veriler Kaydedilsin mi? (y veya n): ')
        if hotelVerification != 'y':
            print("Güncelleme Başarısız!")
            exit()
        else:
            colhotelupdate ={ "$set":  { "HotelTitle": hotelTitle, "HotelCode": hotelCode, "HotelRegion":hotelRegion, "HotelRegionCode":hotelRegionCode, "HotelCountry":hotelCountry, "IsDelete":isDelete }}
            mycol.update_one(hotelId, colhotelupdate)
            print("Güncellendi.")
    else:
        print("Id Bulunamadı.")