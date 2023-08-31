import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# start counting time for scraper performance
start_time = time.time()

# three functions to process html components: int values and weather pictures
def parse_image(element, name_mapping):
    images = element.find_elements(By.TAG_NAME, 'img')
    if not images:
        return ''
    image = images[0]
    for indicator, name in name_mapping.items():
        if indicator in image.get_attribute('src'):
            return name
    return ''

def parse_int(element):
    try:
        return int(element.text)
    except ValueError:
        return ''

def parse_wind(element):
    result = element.text.strip().split()
    if len(result) < 2:
        return ['', '']
    return result

# function to process single row in weather table
def extract_line(data, date):
    # mappings from image names in html to human-readable names
    cloud_names = {
        'sun.png': 'Sun',
        'sunc.png': 'Sun/Clouds',
        'suncl.png': 'Mostly Clouds',
        'dull.png': 'Dull'
    }
    weather_names = {
        'rain.png': 'Rain',
        'snow.png': 'Snow',
        'storm.png': 'Storm'
    }

    day_wind = parse_wind(data[5])
    night_wind = parse_wind(data[10])

    # result as a dict, each cell is properly formatted with one of methods above
    return {
        'Date': date.strftime('%d.%m.%Y'),
        'D Temperature': parse_int(data[1]),
        'D Pressure': parse_int(data[2]),
        'D Cloudiness': parse_image(data[3], cloud_names),
        'D Weather Conditions': parse_image(data[4], weather_names),
        'D Wind Direction': day_wind[0],
        'D Wind Speed': day_wind[1],
        'N Temperature': parse_int(data[6]),
        'N Pressure': parse_int(data[7]),
        'N Cloudiness': parse_image(data[8], cloud_names),
        'N Weather Conditions': parse_image(data[9], weather_names),
        'N Wind Direction': night_wind[0],
        'N Wind Speed': night_wind[1]
    }

# function to process weather table
def parse(start_date, driver):
    table = driver.find_elements(By.TAG_NAME, 'tr')[2:]
    # table = response.css('tr')[2:]
    month = start_date.month
    year = start_date.year
    
    lines = []
    for i, row in enumerate(table):
        data = row.find_elements(By.TAG_NAME, 'td')
        day = i + 1
        date = datetime.datetime(year, month, day)
        result = extract_line(data, date)
        lines.append(result)
    return lines

# creating limiting parameter
limit_scrapping = True

# setting up selenium chrome driver
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# setting up list for storing results
storage = []

# setting city ID (Warsaw = 3196)
cityid = 3196

# setting start and finish date to crawl
startdate = datetime.datetime(1997, 4, 1) # april 1997
finishdate = datetime.datetime(2023, 8, 30) # august 2023


pickyear = startdate.year
pickmonth = startdate.month
scrapped_pages = 0

# creating a list of urls for scrapping
urls = []
while pickyear != finishdate.year or pickmonth != finishdate.month:
    url = f'https://gismeteo.ru/diary/{cityid}/{pickyear}/{pickmonth}'
    date = datetime.datetime(pickyear, pickmonth, 1)
    urls.append((date, url))
    
    # applying a limiting parameter
    scrapped_pages += 1
    if scrapped_pages == 100 and limit_scrapping:
        break

    pickmonth += 1
    if pickmonth == 13:
        pickmonth = 1
        pickyear += 1

for date, url in urls:
    driver.get(url)
    data = parse(date, driver)
    print(url)
    storage.extend(data)

wedata = pd.DataFrame(storage)
wedata.to_csv(f'diary_{cityid}.csv', encoding='utf-8', index=False)

# performance of the scraper
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Algorithm took {elapsed_time:.6f} seconds to run.")


