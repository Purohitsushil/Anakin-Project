##Importing libraries

from selenium.webdriver.common.by import By
import time
from seleniumwire import webdriver
from seleniumwire.utils import decode
import pandas as pd

def scraper(operating,loca,pages):
    # set driver path
    if operating == 'mac':
        # this are for m1 macbook configuration you have macbook m1 uncomment line no 13 and 14, use driver/chromedriverm1
        # options = webdriver.ChromeOptions()
        # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        chrome_driver_binary = "driver/chromedriver"
        # driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
        driver = webdriver.Chrome(chrome_driver_binary)
    elif operating == 'win':
        chrome_driver_binary = "driver/chromedriver.exe"
        driver = webdriver.Chrome(chrome_driver_binary)

    # Loading the url
    driver.get("https://food.grab.com/sg/en/")
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, "ant-input").click()
    time.sleep(5)
    location = driver.find_element(By.CLASS_NAME, "ant-input")

    # Input for the Location
    location.send_keys(loca)
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/ul/li[1]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="page-content"]/div[2]/div/button').click()
    time.sleep(5)

    name = []
    lat = []
    long = []

    # Collecting the api with required information from the landing paqe and cleaning the data
    for request in driver.requests:
        if request.response:
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type'],
            )
            if request.url == 'https://food.grab.com/sg/en/restaurants':
                body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                contents = str(body)
                contents = contents.split('photoHref')
                for i in contents:
                    try:
                        text = i
                        data = text.split(',')

                        restaurant = {}
                        for item in data:
                            if 'name' in item:
                                restaurant['name'] = item.split(':')[1].replace('"', '')
                            if 'latitude' in item:
                                restaurant['latitude'] = float(item.split(':')[1])
                            if 'longitude' in item:
                                restaurant['longitude'] = float(item.split(':')[1])

                        name.append(restaurant['name'])
                        lat.append(restaurant['latitude'])
                        long.append(restaurant['longitude'])
                    except:
                        pass

    # Scroll function used with another data cleaning method as api is changed
    for l in range(pages):
        # Get the height of the page
        height = driver.execute_script("return document.body.scrollHeight")

        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(10)

        for request in driver.requests:
            if request.response:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type'],
                )
                if request.url == 'https://portal.grab.com/foodweb/v2/search':
                    body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
                    contents = str(body)
                    contents = contents.split('photoHref')

                    for x in contents:
                        data = x.split(',')
                        for i in range(len(data)):
                            item = data[i].split(':')
                            for j in range(len(item)):
                                try:
                                    if 'name' in item[j]:
                                        name.append((item[j + 1]).split('"')[1])
                                    if 'latitude' in item[j]:
                                        lat.append((item[j + 1]))
                                    if 'longitude' in item[j]:
                                        long.append((item[j + 1])[:-1])
                                except:
                                    pass
        time.sleep(10)

        # Creating Dict with required data
        restro = {
        'Restrurant Name':name,
        'Latitude':lat,
        'Longitude':long
        }

        # Saving the data to CSV
        df = pd.DataFrame(restro)
        df.to_csv('data.csv')

if __name__ == "__main__":
    # enter your os 'mac' or 'win'
    operating = 'mac'
    # enter number of pages you want to scroll
    pages = 7
    # enter the location you want to scrape
    loca = 'Jurong East'

    scraper(operating,loca,pages)