from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from hoteltd import hotelList
from functions import ayint, aystr, tariharaligi
from datetime import datetime

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

browser=webdriver.Firefox()
for hotel in hotelList:
    url=hotel[1]
    browser.get(url)
    time.sleep(1)
    konaklamasec = browser.find_element_by_xpath("//*[@id='type_select']/div/fieldset/label[2]")
    konaklamasec.click()
    time.sleep(2)
    giristarihi= browser.find_element_by_xpath("//*[@id='cin']")
    giristarihi.click()
    varsayilanay= browser.find_element_by_xpath("//*[@id='cin_root']/div/div/div/div/div[1]/div[1]").text
    varsayilanyil= browser.find_element_by_xpath("//*[@id='cin_root']/div/div/div/div/div[1]/div[2]").text
    fark = tariharaligi(varsayilanay, varsayilanyil, targirisay, targirisyil)
    clickdatenext = "document.getElementsByClassName('picker__nav--next')[0].click();"
    i = 0
    while i < fark:
        browser.execute_script(clickdatenext)
        time.sleep(1)
        i += 1
    datedayclick = "document.getElementsByClassName('picker__day--infocus')["+ targirisguntd +"].click();"
    browser.execute_script(datedayclick)
    time.sleep(3)
    cikistarihi= browser.find_element_by_xpath("//*[@id='cout']")
    cikistarihi.click()
    time.sleep(2)
    i = 1
    while i <= gunsayisi:
        browser.find_element_by_css_selector('body').send_keys(Keys.RIGHT)
        time.sleep(1)
        i += 1
    browser.find_element_by_css_selector('body').send_keys(Keys.RETURN)
    time.sleep(1)
    gosterbutton = browser.find_element_by_xpath("//*[@id='ch']/div/div[3]/button")
    gosterbutton.click()
    time.sleep(6)
    price= browser.find_element_by_xpath("//*[@id='reservation_result']/ul/li[1]/div/div[3]/div[1]/span").text
    print("Konaklama Fiyatı:"+price)
    time.sleep(2)
    paketsec = browser.find_element_by_xpath("//*[@id='type_select']/div/fieldset/label[1]")
    paketsec.click()
    time.sleep(1)
    havalimaniclick = browser.find_element_by_xpath("//*[@id='hotel_from']/fieldset/div")
    havalimaniclick.click()
    time.sleep(1)
    havalimanisec = browser.find_element_by_xpath("//*[@id='hotel_from']/fieldset/div/div/ul/li[7]/a")
    havalimanisec.click()
    time.sleep(1)
    paketgonder = browser.find_element_by_xpath("//*[@id='ch']/div/div[3]/button")
    paketgonder.click()
    time.sleep(8)
    dep_checked = browser.find_element_by_xpath("//*[@id='d_dtime']").text
    print("Uçak Gidiş Saati:"+ dep_checked)
    time.sleep(1)
    ret_checked = browser.find_element_by_xpath("//*[@id='r_dtime']").text
    time.sleep(1)
    paketprice= browser.find_element_by_xpath("//*[@id='pck_price0']").text
    time.sleep(1)
    print("Uçak Dönüş Saati:"+ ret_checked)
    print("Paket Fiyatı:"+ paketprice)
    time.sleep(4)
"""
istenilenay= browser.find_element_by_xpath("//*[@id='cin_root']/div/div/div/div/div[1]/div[1]").text
print(istenilenay)
"""
browser.close()


