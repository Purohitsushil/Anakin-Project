import time

import pandas as pd
from appium import webdriver
from selenium.webdriver.common.by import By


#Intialize the device
data = {
    "platformName": "android",
    "platformVersion": "10",
    "deviceName": "FA6AX0300950"
}

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",data)

#open the app with its homepage and loction in singapore
driver.find_element(By.XPATH,'(//android.widget.ImageView[@content-desc="ImageView"])[3]').click()
time.sleep(10)


driver.swipe(150, 1200, 150, 200, 1000)
driver.swipe(150, 1200, 150, 200, 1000)
driver.swipe(150, 1200, 150, 200, 1000)

name = []
openhour = []
address = []

#Restaurant is selected from loading then open the restraurant page and grab the restaurant info 
for j in range(200):
    y = driver.find_elements(By.ID, 'com.grabtaxi.passenger:id/rootView')
    for i in range(len(y)):
        try:
            n1 = ''
            n2 = ''
            n3 = ''
            y[i].click()
            time.sleep(5)
            driver.swipe(300, 250, 300, 250, 50)
            time.sleep(5)
            driver.find_element(By.ID, 'com.grabtaxi.passenger:id/gf_mex_name_with_icon').click()
            time.sleep(5)
            driver.swipe(150, 1200, 150, 200, 1000)
            item = driver.find_element(By.ID, 'com.grabtaxi.passenger:id/toolbar_title')
            print(item.get_attribute('text'))
            n1 = (item.get_attribute('text'))
            item = driver.find_element(By.ID, 'com.grabtaxi.passenger:id/open_hours_container')
            item1 = driver.find_elements(By.ID, 'com.grabtaxi.passenger:id/gf_open_hours_day')
            item2 = driver.find_elements(By.ID, 'com.grabtaxi.passenger:id/gf_open_hours_time')
            x2 = []
            for x1 in range(len(item1)):
                x2.append((item1[x1].get_attribute('text')) + ' ' + (item2[x1].get_attribute('text')))
            print(x2)
            n2 = x2
            item = driver.find_element(By.ID, 'com.grabtaxi.passenger:id/address')
            print(item.get_attribute('text'))
            n3 = item.get_attribute('text')
            driver.find_element(By.ID, 'com.grabtaxi.passenger:id/back_icon').click()
            time.sleep(5)
            driver.find_element(By.ID, 'com.grabtaxi.passenger:id/back_icon').click()
            time.sleep(5)
            if n1 != '' and n2 != '' and n3 != '' :
                name.append(n1)
                openhour.append(n2)
                address.append(n3)
                dict = {
                    'Restaurant name': name,
                    'Open Hours': openhour,
                    'Address': address
                }
                df1 = pd.DataFrame(dict)
                df1 = df1.drop_duplicates(subset='Restaurant name')
                df1.to_csv('restro.csv')
        except:
            pass
    driver.swipe(150, 800, 150, 200, 600)

