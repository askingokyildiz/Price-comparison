from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
from datetime import datetime, date
import time
import pymongo
from bson.objectid import ObjectId
import json

#İşlem Süresini Başlatma
start = time.perf_counter()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["price_comparison"]
competitorcol = db["competitor"]
try:
    for competitor in competitorcol.find():
        print(competitor["CompetitorTitle"])
        print(competitor["_id"])
except:
    print("Id Bulunamadı.")

#İşlem Süresini Bitirip Yazdırma.
finish = time.perf_counter()
print('Bitiş saniyesi:', round(finish-start, 2))