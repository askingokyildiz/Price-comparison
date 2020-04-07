import pymongo
from bson.objectid import ObjectId

competitorId=input('Competitor Id: ')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["price_comparison"]
mycol = mydb["competitor"]
try:
    competitorId={ "_id": ObjectId(competitorId) }
    competitorfind = mycol.find_one(competitorId)
except:
    print("Id Bulunamadı.")
else:
    if competitorfind:
        print(competitorfind)
        competitorDesc=input('Competitor Desc: ')
        competitorGroup=input('Competitor Group: ')
        competitorMarket=input('Competitor Market: ')
        isDelete=input('is Delete (Aktif:0 veya Pasif:1): ')
        competitorVerification=input('Veriler Güncellensin mi? (y veya n): ')
        if competitorVerification != 'y':
            print("Güncelleme Başarısız!")
            exit()
        else:
            colcompetitorupdate ={ "$set": { "CompetitorDesc":competitorDesc, "CompetitorGroup":competitorGroup, "CompetitorMarket":competitorMarket, "IsDelete":isDelete }}
            mycol.update_one(competitorId, colcompetitorupdate)
            print("Güncellendi.")
    else:
        print("Id Bulunamadı.")
