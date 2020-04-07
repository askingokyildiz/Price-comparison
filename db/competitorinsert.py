import pymongo

competitorTitle=input('Competitor Title: ')
competitorURL=input('Competitor URL: ')
competitorDesc=input('Competitor Desc: ')
competitorGroup=input('Competitor Group: ')
competitorMarket=input('Competitor Market: ')
competitorVerification=input('Veriler Kaydedilsin mi? (y veya n): ')
isDelete=0
if competitorVerification != 'y':
    print("Kayıt Başarısız!")
    exit()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["price_comparison"]
mycol = mydb["competitor"]
colcompetitor = { "CompetitorTitle": competitorTitle, "CompetitorURL": competitorURL, "CompetitorDesc":competitorDesc, "CompetitorGroup":competitorGroup, "CompetitorMarket":competitorMarket, "IsDelete":isDelete }
mycol.insert_one(colcompetitor)
print("Kaydedildi.")