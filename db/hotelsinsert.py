import pymongo

hotelTitle=input('HotelTitle: ')
hotelCode=input('Hotel Code: ')
hotelRegion=input('Hotel Region: ')
hotelRegionCode=input('Hotel Region Code: ')
hotelCountry=input('Hotel Country: ')
hotelVerification=input('Veriler Kaydedilsin mi? (y veya n): ')
isDelete=0
if hotelVerification != 'y':
    print("Kayıt Başarısız!")
    exit()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["price_comparison"]
mycol = mydb["hotels"]
colhotel = { "HotelTitle": hotelTitle, "HotelCode": hotelCode, "HotelRegion":hotelRegion, "HotelRegionCode":hotelRegionCode, "HotelCountry":hotelCountry, "IsDelete":isDelete }
mycol.insert_one(colhotel)
print("Kaydedildi.")