from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
from datetime import datetime, date
import time

start = time.perf_counter()


finish = time.perf_counter()
print('Bitiş saniyesi:', round(finish-start, 2))